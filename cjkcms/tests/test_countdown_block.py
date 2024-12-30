import pytest
from django.test import Client, TestCase, override_settings
from wagtail.models import Page
from cjkcms.models.cms_models import ArticlePage
from datetime import datetime, timedelta, timezone


@override_settings(
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
)
@pytest.mark.django_db
class TestCountdownBlock(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_article_page()

    def create_article_page(self):
        home_page = Page.objects.get(path="00010001")
        article_page = ArticlePage(title="Test Article", body=None)
        home_page.add_child(instance=article_page)
        article_page.save_revision().publish()

    def set_article_body(self, content) -> None:
        article_page = ArticlePage.objects.get(title="Test Article")
        article_page.body = content
        article_page.save_revision().publish()

    def test_css_theme_title(self):
        block_content = [
            {
                "type": "countdown",
                "value": {
                    "title": "Counter Title",
                    "theme": "losange",
                    "settings": {"custom_css_class": "my-custom-class"},
                    "start_date": "2029-01-01 00:00",
                },
                "id": "countdown-block",
            }
        ]
        self.set_article_body(block_content)
        response = self.client.get("/test-article/")
        self.assertContains(response, "my-custom-class")
        self.assertNotContains(response, "my-other-class")
        self.assertContains(response, "losange")
        self.assertContains(response, "Counter Title")
        self.assertNotContains(response, "<a href=")

    def test_url(self):
        block_content = [
            {
                "type": "countdown",
                "value": {
                    "theme": "light",
                    "url": "https://example.com",
                    "start_date": "2029-01-01 00:00",
                    "timezone": "UTC",
                },
                "id": "countdown-block2",
            }
        ]
        self.set_article_body(block_content)
        response = self.client.get("/test-article/")
        self.assertContains(response, '<a href="https://example.com"')

    def test_time(self):
        # generate start date that is one in the future

        # Get the current UTC time
        current_utc_time = datetime.now(timezone.utc)
        # Add one minute to the current UTC time
        one_minute_ahead = current_utc_time + timedelta(minutes=1)
        # Remove timezone info from the one_minute_ahead datetime
        one_minute_ahead_naive = one_minute_ahead.replace(tzinfo=None)

        block_content = [
            {
                "type": "countdown",
                "value": {
                    "theme": "light",
                    "start_date": one_minute_ahead_naive.strftime("%Y-%m-%d %H:%M"),
                    "timezone": "UTC",
                },
                "id": "countdown-block3",
            }
        ]
        self.set_article_body(block_content)
        response = self.client.get("/test-article/")
        self.assertContains(response, "year: " + str(one_minute_ahead.year))
        self.assertContains(response, "month: " + str(one_minute_ahead.month))
        self.assertContains(response, "day: " + str(one_minute_ahead.day))
        self.assertContains(response, "hours: " + str(one_minute_ahead.hour))
        self.assertContains(response, "minutes: " + str(one_minute_ahead.minute))
