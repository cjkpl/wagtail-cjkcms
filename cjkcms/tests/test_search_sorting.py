from datetime import timedelta
from unittest.mock import patch

import pytest
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from wagtail.models import Locale, Page
from wagtail.search import index as search_index

from cjkcms import views
from cjkcms.models.cms_models import ArticlePage


class EmptySearchResults:
    def count(self):
        return 0

    def __iter__(self):
        return iter(())


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

    def test_malformed_postgres_tsquery_payload_is_normalised(self):
        payload = (
            "('' & 'NkeD;DECLARE/**/@x/**/CHAR(9);SET/**/@x=0x303a303a35;"
            "WAITFOR/**/DELAY/**/@x')"
        )

        normalised_query = views._normalise_search_query_for_backend(payload)

        self.assertEqual(
            normalised_query,
            "NkeD DECLARE x CHAR 9 SET x 0x303a303a35 WAITFOR DELAY x",
        )

    def test_malformed_sqlite_style_payload_is_normalised(self):
        payload = (
            "('' & 'vtgT;SeleCt/**/LiKe(Char(65,66,67,68,69,70,71),"
            "UPpeR(HEx(RAnDomBlOb(500000000/2))))')"
        )

        normalised_query = views._normalise_search_query_for_backend(payload)

        self.assertEqual(
            normalised_query,
            "vtgT SeleCt LiKe Char 65 66 67 68 69 70 71 UPpeR HEx RAnDomBlOb 500000000 2",
        )

    def test_search_view_uses_normalised_query_for_backend(self):
        payload = (
            "('' & 'NkeD;DECLARE/**/@x/**/CHAR(9);SET/**/@x=0x303a303a35;"
            "WAITFOR/**/DELAY/**/@x')"
        )

        with patch(
            "cjkcms.views.search_model_backend", return_value=EmptySearchResults()
        ) as search_model_backend:
            response = self.client.get(
                reverse("cjkcms_search"),
                {"s": payload, "t": "cjkcms.articlepage"},
                follow=True,
            )

        self.assertEqual(response.status_code, 200)
        search_model_backend.assert_called_once()
        self.assertEqual(
            search_model_backend.call_args.args[1],
            "NkeD DECLARE x CHAR 9 SET x 0x303a303a35 WAITFOR DELAY x",
        )

    def test_search_view_skips_backend_for_punctuation_only_query(self):
        with patch("cjkcms.views.search_model_backend") as search_model_backend:
            response = self.client.get(
                reverse("cjkcms_search"),
                {"s": "('' & '')", "t": "cjkcms.articlepage"},
                follow=True,
            )

        self.assertEqual(response.status_code, 200)
        search_model_backend.assert_not_called()
