import uuid
from unittest.mock import patch

from django.test import Client, TestCase
from wagtail.models import Page

from cjkcms.models import page_models
from cjkcms.models.cms_models import ArticlePage


def text_body(text):
    return [{"type": "text", "value": f"<p>{text}</p>", "id": str(uuid.uuid4())}]


class BodyPreviewTests(TestCase):
    """The body is rendered once for all uses of its preview."""

    def setUp(self):
        home_page = Page.objects.get(path="00010001")
        self.page = ArticlePage(
            title="Preview", slug="preview", body=text_body("First version")
        )
        home_page.add_child(instance=self.page)
        self.page.save_revision().publish()

    def count_previews(self):
        return patch.object(
            page_models,
            "get_richtext_preview",
            wraps=page_models.get_richtext_preview,
        )

    def test_article_without_description_renders_preview_once(self):
        with self.count_previews() as get_richtext_preview:
            response = Client().get(self.page.url)

        # The preview is the description in several meta tags.
        self.assertGreater(response.content.decode().count("First version"), 2)
        self.assertEqual(get_richtext_preview.call_count, 1)

    def test_preview_is_kept_per_instance(self):
        page = ArticlePage.objects.get(pk=self.page.pk)
        with self.count_previews() as get_richtext_preview:
            self.assertEqual(page.body_preview.strip(), "First version")
            self.assertEqual(page.seo_description.strip(), "First version")
            self.assertEqual(page.body_preview.strip(), "First version")
        self.assertEqual(get_richtext_preview.call_count, 1)

    def test_preview_follows_replaced_body(self):
        page = ArticlePage.objects.get(pk=self.page.pk)
        self.assertEqual(page.body_preview.strip(), "First version")

        page.body = text_body("Second version")
        self.assertEqual(page.body_preview.strip(), "Second version")

        page.save()
        page = ArticlePage.objects.get(pk=page.pk)
        self.assertEqual(page.body_preview.strip(), "Second version")
