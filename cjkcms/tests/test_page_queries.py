from django.db import connection
from django.test import Client, TestCase
from django.test.utils import CaptureQueriesContext
from wagtail.images.tests.utils import Image, get_test_image_file
from wagtail.models import Page, Site

from cjkcms.models import LayoutSettings
from cjkcms.models.cms_models import WebPage


def count_queries(queries, table):
    return sum(f'FROM "{table}"' in query["sql"] for query in queries.captured_queries)


class PageSiteLookupTests(TestCase):
    """Site and layout settings are looked up once per page instance."""

    def setUp(self):
        self.home_page = Page.objects.get(path="00010001")
        page = WebPage(title="Query page", slug="query-page")
        self.home_page.add_child(instance=page)
        page.save_revision().publish()
        # Use a new instance, as the one above has been through publishing.
        self.page = WebPage.objects.get(pk=page.pk)
        self.site = Site.objects.get(is_default_site=True)

    def test_get_site_queries_once(self):
        with CaptureQueriesContext(connection) as queries:
            sites = [self.page.get_site() for _ in range(3)]
        self.assertEqual(sites, [self.site] * 3)
        self.assertEqual(count_queries(queries, "wagtailcore_site"), 1)

    def test_get_site_is_per_instance(self):
        self.page.get_site()
        other = WebPage.objects.get(pk=self.page.pk)
        with CaptureQueriesContext(connection) as queries:
            self.assertEqual(other.get_site(), self.site)
        self.assertEqual(count_queries(queries, "wagtailcore_site"), 1)

    def test_get_site_follows_page_moved_to_another_site(self):
        other_root = Page(title="Other site", slug="other-site")
        Page.objects.get(path="0001").add_child(instance=other_root)
        other_site = Site.objects.create(
            hostname="other.example.com", root_page=other_root, site_name="Other"
        )
        self.assertEqual(self.page.get_site(), self.site)

        self.page.move(other_root, pos="last-child")
        self.page.refresh_from_db()

        self.assertEqual(self.page.get_site(), other_site)

    def test_get_site_of_unroutable_page(self):
        page = WebPage(title="Not in a tree")
        self.assertIsNone(page.get_site())
        with self.assertRaises(LayoutSettings.DoesNotExist):
            page.get_layout_settings()

    def test_seo_images_load_layout_settings_once(self):
        logo = Image.objects.create(title="Logo", file=get_test_image_file())
        layout = LayoutSettings.for_site(self.site)
        layout.logo = logo
        layout.save()

        with CaptureQueriesContext(connection) as queries:
            self.assertIsNone(self.page.default_seo_image)
            self.assertEqual(self.page.seo_logo, logo)
            self.assertEqual(self.page.seo_image, logo)
            self.assertEqual(self.page.seo_image, logo)
        self.assertEqual(count_queries(queries, "cjkcms_layoutsettings"), 1)
        self.assertEqual(count_queries(queries, "wagtailcore_site"), 1)

    def test_layout_settings_are_fresh_for_new_page_instance(self):
        self.assertIsNone(self.page.default_seo_image)
        image = Image.objects.create(title="Default", file=get_test_image_file())
        layout = LayoutSettings.for_site(self.site)
        layout.default_seo_image = image
        layout.save()

        page = WebPage.objects.get(pk=self.page.pk)
        self.assertEqual(page.default_seo_image, image)

    def test_rendering_page_does_not_repeat_lookups(self):
        client = Client()
        client.get(self.page.url)
        with CaptureQueriesContext(connection) as queries:
            response = client.get(self.page.url)
        self.assertEqual(response.status_code, 200)
        # One lookup to route the request and one for the page's own site.
        self.assertLessEqual(count_queries(queries, "wagtailcore_site"), 2)
        # One for the template context and one for the page's SEO properties.
        self.assertLessEqual(count_queries(queries, "cjkcms_layoutsettings"), 2)
