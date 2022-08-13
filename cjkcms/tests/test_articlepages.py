from wagtail.tests.utils import WagtailPageTests
from cjkcms.models import (
    CjkcmsArticlePage,
    CjkcmsArticleIndexPage,
)
from wagtail.tests.utils.form_data import nested_form_data

from wagtail.core.models import Page
from cjkcms.models.cms_models import ArticlePage, ArticleIndexPage


class ArticlePageTests(WagtailPageTests):
    """Tests CjkCms Article Pages"""

    def test_cannot_create_cjkcms_article_page(self):
        # Get the HomePage
        home_page = Page.objects.get(path="00010001")

        # Assert that a CjkcmsArticlePage can NOT be made here, it's abstract
        self.assertCanNotCreateAt(
            home_page, CjkcmsArticlePage, nested_form_data({"title": "Article"})
        )

    def test_cannot_create_cjkcms_article_index_page(self):
        # Get the HomePage
        home_page = Page.objects.get(path="00010001")

        # Assert that a CjkcmsArticleIndexPage can NOT be made here, it's abstract
        self.assertCanNotCreateAt(
            home_page, CjkcmsArticleIndexPage, nested_form_data({"title": "Article"})
        )

    def test_can_create_article_page(self):
        # Get the HomePage
        home_page = Page.objects.get(path="00010001")

        body = [
            {
                "type": "embed_video",
                "value": {
                    "url": "https://youtu.be/AxLgTxBLsgI",
                },
                "id": "6ffa1b27-d884-4a9b-ba35-66140ff8a0ee",
            }
        ]

        article_page = ArticlePage(title="Test Article", body=body)

        home_page.add_child(instance=article_page)
        article_page.save_revision().publish()

        ap = ArticlePage.objects.get(slug="test-article")
        self.assertEqual(ap.title, "Test Article")

    def test_can_create_article_index_page(self):
        # Get the HomePage
        home_page = Page.objects.get(path="00010001")

        # Assert that a ArticleIndexPage can be made here
        self.assertCanCreateAt(
            home_page, ArticleIndexPage, nested_form_data({"title": "Article Index"})
        )
