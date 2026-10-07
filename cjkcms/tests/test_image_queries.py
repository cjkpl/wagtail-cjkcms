import uuid

from django.db import connection
from django.test import Client, TestCase, override_settings
from django.test.utils import CaptureQueriesContext
from wagtail.images.tests.utils import Image, get_test_image_file
from wagtail.models import Collection, Page, Site

from cjkcms.models import LayoutSettings
from cjkcms.models.cms_models import ArticlePage, WebPage
from cjkcms.templatetags.cjkcms_tags import get_pictures


def rendition_queries(queries):
    return [
        query["sql"]
        for query in queries.captured_queries
        if 'FROM "wagtailimages_rendition"' in query["sql"]
    ]


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
)
class ImageRenditionQueryTests(TestCase):
    """Renditions of several images are loaded together, not one by one."""

    def setUp(self):
        self.home_page = Page.objects.get(path="00010001")
        self.client = Client()

    def render_twice(self, page):
        # The first request creates the renditions, the second one reads them.
        self.assertEqual(self.client.get(page.url).status_code, 200)
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(page.url)
        return response, queries

    def create_gallery(self, images=3):
        collection = Collection.get_first_root_node().add_child(name="Gallery")
        for number in range(images):
            Image.objects.create(
                title=f"Picture {number}",
                file=get_test_image_file(filename=f"picture{number}.png"),
                collection=collection,
            )
        return collection

    def test_gallery_loads_renditions_with_one_query(self):
        collection = self.create_gallery()
        body = [
            {
                "type": "image_gallery",
                "value": {"collection": collection.id, "tag": None, "settings": {}},
                "id": str(uuid.uuid4()),
            }
        ]
        # Without a description the article renders its body again for each
        # meta tag, which would repeat the queries counted below.
        page = ArticlePage(
            title="Gallery", slug="gallery", body=body, search_description="Gallery"
        )
        self.home_page.add_child(instance=page)
        page.save_revision().publish()

        response, queries = self.render_twice(page)

        self.assertEqual(response.content.decode().count('class="thumbnail'), 3)
        self.assertEqual(len(rendition_queries(queries)), 1)

    def test_get_pictures_filters_by_collection(self):
        collection = self.create_gallery(images=2)
        Image.objects.create(title="Elsewhere", file=get_test_image_file())

        self.assertEqual(get_pictures(collection.id).count(), 2)
        self.assertEqual(get_pictures(collection.id, renditions="").count(), 2)
        # A collection which was deleted has no pictures.
        self.assertEqual(get_pictures(collection.id + 1000).count(), 0)

    def test_favicon_loads_renditions_with_one_query(self):
        layout = LayoutSettings.for_site(Site.objects.get(is_default_site=True))
        layout.favicon = Image.objects.create(
            title="Favicon", file=get_test_image_file(filename="favicon.png")
        )
        layout.save()
        page = WebPage(title="Favicon", slug="favicon-page")
        self.home_page.add_child(instance=page)
        page.save_revision().publish()

        response, queries = self.render_twice(page)

        html = response.content.decode()
        self.assertEqual(html.count('rel="apple-touch-icon"'), 5)
        for size in ("120x120", "180x180", "152x152", "167x167"):
            self.assertIn(f"fill-{size}.format-png", html)
        self.assertEqual(len(rendition_queries(queries)), 1)

    def test_page_without_favicon(self):
        page = WebPage(title="No favicon", slug="no-favicon")
        self.home_page.add_child(instance=page)
        page.save_revision().publish()

        response, queries = self.render_twice(page)

        self.assertNotContains(response, "apple-touch-icon")
        self.assertEqual(rendition_queries(queries), [])
