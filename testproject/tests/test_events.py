import pytest
from django.test import Client, TestCase, override_settings
from wagtail.models import Page

from cjkcms.blocks import CONTENT_STREAMBLOCKS
from cjkcms.blocks.content.events import PublicEventBlock
from testapp.models import ProjectArticlePage

# Redefine ArticlePage adding the new content blocks for bulic event
PROJECT_CONTENT_STREAMBLOCKS = CONTENT_STREAMBLOCKS + [
    ("public_event", PublicEventBlock()),
]


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
@pytest.mark.django_db
class TestEventBlocks(TestCase):
    """
    The Public Event block is not added to any project blocks by default -
    on purpose. Projects that want to use it, should add it e.g. to their own
    PROJECT_CONTENT_BLOCKS. This setup shows how to write tests for blocks defined
    in external applications, adding them to test pages on the fly.
    """

    block_public_event = [
        {
            "type": "public_event",
            "value": {
                "settings": {
                    "custom_template": "",
                    "custom_css_class": "",
                    "custom_id": "",
                },
                "title": "New Year",
                "start_date": "2029-12-31",
                "url": "https://en.wikipedia.org/wiki/New_Year%27s_Eve",
            },
            "id": "a586b8eb-3af4-4e8a-9f12-c6ec582930bg",
        }
    ]

    def setUp(self):
        self.client = Client()

        # Get the HomePage
        home_page = Page.objects.get(path="00010001")

        article_page = ProjectArticlePage(
            title="Test Article", body=self.block_public_event
        )

        home_page.add_child(instance=article_page)
        article_page.save_revision().publish()

    def test_event_shown(self):
        ap = ProjectArticlePage.objects.get(slug="test-article")

        self.assertEqual(ap.title, "Test Article")

        response = self.client.get("/test-article/")
        self.assertEqual(response.status_code, 200)

        print(response.content)
        self.assertContains(response, "New Year")
