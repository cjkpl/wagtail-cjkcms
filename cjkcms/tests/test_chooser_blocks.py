import uuid

from django.test import Client, TestCase, override_settings
from taggit.models import Tag
from wagtail.images.tests.utils import Image, get_test_image_file
from wagtail.models import Collection, Page

from cjkcms.blocks.base_blocks import CollectionChooserBlock, TagChooserBlock
from cjkcms.models.cms_models import ArticlePage


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
)
class DeletedChoiceTests(TestCase):
    """Blocks keep working after the collection or tag they point to is deleted."""

    def setUp(self):
        self.collection = Collection.get_first_root_node().add_child(name="Gallery")
        self.tag = Tag.objects.create(name="featured")
        for title, tags in (("Tagged", [self.tag]), ("Untagged", [])):
            image = Image.objects.create(
                title=title,
                file=get_test_image_file(filename=f"{title}.png"),
                collection=self.collection,
            )
            image.tags.add(*tags)

    def create_gallery_page(self, slug):
        body = [
            {
                "type": "image_gallery",
                "value": {
                    "collection": self.collection.pk,
                    "tag": self.tag.pk,
                    "settings": {},
                },
                "id": str(uuid.uuid4()),
            }
        ]
        page = ArticlePage(title=slug, slug=slug, body=body, search_description=slug)
        Page.objects.get(path="00010001").add_child(instance=page)
        page.save_revision().publish()
        return page

    def thumbnails(self, page):
        response = Client().get(page.url)
        self.assertEqual(response.status_code, 200)
        return response.content.decode().count('class="thumbnail')

    def test_blocks_return_existing_choice(self):
        self.assertEqual(
            CollectionChooserBlock().to_python(self.collection.pk), self.collection
        )
        self.assertEqual(TagChooserBlock().to_python(self.tag.pk), self.tag)

    def test_blocks_return_none_for_deleted_choice(self):
        self.assertIsNone(CollectionChooserBlock().to_python(self.collection.pk + 1000))
        self.assertIsNone(TagChooserBlock().to_python(self.tag.pk + 1000))

    def test_gallery_renders_chosen_pictures(self):
        self.assertEqual(self.thumbnails(self.create_gallery_page("gallery")), 1)

    def test_gallery_with_deleted_tag_shows_collection(self):
        page = self.create_gallery_page("no-tag")
        self.tag.delete()
        self.assertEqual(self.thumbnails(page), 2)

    def test_gallery_with_deleted_collection_is_empty(self):
        page = self.create_gallery_page("no-collection")
        Image.objects.all().delete()
        self.collection.delete()
        self.assertEqual(self.thumbnails(page), 0)
