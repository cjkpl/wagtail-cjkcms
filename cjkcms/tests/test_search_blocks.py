import pytest

from wagtail.core.models import Page
from django.urls import reverse
from django.test import Client, TestCase

from cjkcms.models.cms_models import ArticlePage


@pytest.mark.django_db
class TestSearchBlocks(TestCase):
    """
    CjkCMS content blocks should be searchable.
    For each content block, create a page with that content block and some text,
    confirm that the search returns the page.
    """

    block_richtext = [
        {
            "type": "text",
            "value": '<p data-block-key="o94f7"> When daisies pied and violets blue</p>',
            "id": "bbfc2acb-79b3-47a6-b974-2a6e4523c94b",
        }
    ]

    block_button_link = [
        {
            "type": "button",
            "value": {
                "settings": {},
                "page_link": None,
                "doc_link": None,
                "other_link": "http://youtube.com",
                "button_title": "My buttony button, not Benjamin",
                "button_style": "btn-primary",
                "button_size": "",
                "visible_for": "all",
            },
            "id": "3f02e0d5-5b99-4e43-821d-549af74b3014",
        }
    ]

    block_html = [
        {
            "type": "html",
            "value": "<h1>Hi from HTML</h1>",
            "id": "d07fc66f-c94c-4ee8-a113-0c17ed2220e5",
        }
    ]

    block_quote = [
        {
            "type": "quote",
            "value": {
                "settings": {
                    "custom_template": "",
                    "custom_css_class": "",
                    "custom_id": "",
                },
                "text": "Quotably interesting",
                "author": "By Mr Nobody",
            },
            "id": "a586b8eb-3af4-4e8a-9f12-c6ec582930bf",
        }
    ]

    def setUp(self):
        self.client = Client()
        self.create_article_page()

    def create_article_page(self):
        # Get the HomePage
        home_page = Page.objects.get(path="00010001")

        article_page = ArticlePage(title="Test Article", body=None)

        home_page.add_child(instance=article_page)
        article_page.save_revision().publish()

    def set_article_body(self, content) -> None:
        article_page = ArticlePage.objects.get(title="Test Article")
        article_page.body = content
        article_page.save_revision().publish()

    def test_page_type_in_search_results(self):
        response = self.client.get(
            reverse("cjkcms_search"), {"s": "doesn't matter"}, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["pagetypes"][0].__name__, "ArticlePage")

    def test_search_richtext(self):
        self.set_article_body(self.block_richtext)

        response = self.client.get(
            reverse("cjkcms_search"), {"s": "not-there"}, follow=True
        )

        self.assertEqual(response.context["results"].count(), 0)

        response = self.client.get(
            reverse("cjkcms_search"), {"s": "daisies"}, follow=True
        )

        self.assertEqual(response.context["results"].count(), 1)

    def test_search_button(self):
        self.set_article_body(self.block_button_link)

        response = self.client.get(
            reverse("cjkcms_search"), {"s": "daisies"}, follow=True
        )

        self.assertEqual(response.context["results"].count(), 0)

        response = self.client.get(
            reverse("cjkcms_search"), {"s": "Benjamin"}, follow=True
        )

        self.assertEqual(response.context["results"].count(), 1)

    def test_search_html(self):
        self.set_article_body(self.block_html)

        response = self.client.get(
            reverse("cjkcms_search"), {"s": "can't see me"}, follow=True
        )

        self.assertEqual(response.context["results"].count(), 0)

        response = self.client.get(
            reverse("cjkcms_search"), {"s": "from HTML"}, follow=True
        )

        self.assertEqual(response.context["results"].count(), 1)

    def test_search_quote(self):
        self.set_article_body(self.block_quote)

        response = self.client.get(
            reverse("cjkcms_search"), {"s": "from HTML"}, follow=True
        )

        self.assertEqual(response.context["results"].count(), 0)

        response = self.client.get(
            reverse("cjkcms_search"), {"s": "quotably"}, follow=True
        )

        self.assertEqual(response.context["results"].count(), 1)

        response = self.client.get(
            reverse("cjkcms_search"), {"s": "Nobody"}, follow=True
        )

        self.assertEqual(response.context["results"].count(), 1)
