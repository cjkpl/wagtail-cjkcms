import pytest
from datetime import timedelta

from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from wagtail.models import Locale, Page
from wagtail.search import index as search_index

from cjkcms.models.cms_models import ArticlePage


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
class TestSearchSorting(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_page = Page.objects.get(path="00010001")
        self.locale = Locale.get_default()
        self._create_articles()

    def _publish_page(self, page):
        self.home_page.add_child(instance=page)
        page.save_revision().publish()
        search_index.insert_or_update_object(page)

    def _create_articles(self):
        now = timezone.now()
        older_time = now - timedelta(days=3)
        newer_time = now - timedelta(days=1)

        older = ArticlePage(
            title="Alpha Article",
            seo_title="Alpha Article",
            locale_id=self.locale.id,
        )
        newer = ArticlePage(
            title="Beta Article",
            seo_title="Beta Article",
            locale_id=self.locale.id,
        )

        self._publish_page(older)
        self._publish_page(newer)

        # Set explicit timestamps to keep ordering deterministic in tests
        ArticlePage.objects.filter(id=older.id).update(
            first_published_at=older_time,
            last_published_at=older_time,
            latest_revision_created_at=older_time,
        )
        ArticlePage.objects.filter(id=newer.id).update(
            first_published_at=newer_time,
            last_published_at=newer_time,
            latest_revision_created_at=newer_time,
        )

        # Refresh from DB for comparisons
        self.older_page = ArticlePage.objects.get(id=older.id)
        self.newer_page = ArticlePage.objects.get(id=newer.id)

    def test_sort_by_created_ascending(self):
        response = self.client.get(
            reverse("cjkcms_search"),
            {"s": "Article", "sort": "created_asc"},
            follow=True,
        )

        titles = [p.title for p in response.context["results_paginated"].object_list]
        self.assertEqual(titles, ["Alpha Article", "Beta Article"])

    def test_sort_by_created_descending(self):
        response = self.client.get(
            reverse("cjkcms_search"),
            {"s": "Article", "sort": "created_desc"},
            follow=True,
        )

        titles = [p.title for p in response.context["results_paginated"].object_list]
        self.assertEqual(titles, ["Beta Article", "Alpha Article"])

    def test_sort_by_updated_descending(self):
        response = self.client.get(
            reverse("cjkcms_search"),
            {"s": "Article", "sort": "updated_desc"},
            follow=True,
        )

        titles = [p.title for p in response.context["results_paginated"].object_list]
        self.assertEqual(titles, ["Beta Article", "Alpha Article"])

    def test_sort_by_title_descending(self):
        response = self.client.get(
            reverse("cjkcms_search"),
            {"s": "Article", "sort": "title_desc"},
            follow=True,
        )

        titles = [p.title for p in response.context["results_paginated"].object_list]
        self.assertEqual(titles, ["Beta Article", "Alpha Article"])
