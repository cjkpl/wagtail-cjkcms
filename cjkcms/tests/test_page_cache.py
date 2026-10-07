from django.core.cache import caches
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from wagtail.models import Page, Site

from cjkcms.models import LayoutSettings
from cjkcms.models.cms_models import WebPage

CACHE_MIDDLEWARE = [
    "wagtailcache.cache.UpdateCacheMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "wagtailcache.cache.FetchFromCacheMiddleware",
]
LOCMEM_CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}
}


@override_settings(
    MIDDLEWARE=CACHE_MIDDLEWARE, CACHES=LOCMEM_CACHES, WAGTAIL_CACHE=True
)
class NavbarSearchPageCacheTests(TestCase):
    """The navbar search form must not prevent pages from being cached."""

    SEARCH_FORMATS = ("box", "box-button", "button-popup")

    def setUp(self):
        caches["default"].clear()
        home_page = Page.objects.get(path="00010001")
        self.page = WebPage(title="Cached page", slug="cached-page")
        home_page.add_child(instance=self.page)
        self.page.save_revision().publish()
        self.url = self.page.url

    def set_search_format(self, search_format):
        layout = LayoutSettings.for_site(Site.objects.get(is_default_site=True))
        layout.navbar_search = True
        layout.search_format = search_format
        layout.save()
        caches["default"].clear()

    def cache_status(self, client=None):
        response = (client or Client()).get(self.url)
        self.assertEqual(response.status_code, 200)
        return response.headers["X-Wagtail-Cache"]

    def test_search_form_has_no_csrf_token(self):
        for search_format in self.SEARCH_FORMATS:
            with self.subTest(search_format=search_format):
                self.set_search_format(search_format)
                response = Client().get(self.url)
                self.assertContains(response, reverse("cjkcms_search"))
                self.assertNotContains(response, "csrfmiddlewaretoken")
                self.assertNotIn("csrftoken", response.cookies)

    def test_page_is_cached_for_new_visitors(self):
        for search_format in self.SEARCH_FORMATS:
            with self.subTest(search_format=search_format):
                self.set_search_format(search_format)
                # Each request comes from a new visitor without any cookies.
                self.assertEqual(self.cache_status(), "miss")
                self.assertEqual(self.cache_status(), "hit")
                self.assertEqual(self.cache_status(), "hit")

    def test_returning_visitors_share_cached_page(self):
        self.set_search_format("box")
        first, second = Client(), Client()
        self.assertEqual(self.cache_status(first), "miss")
        self.assertEqual(self.cache_status(first), "hit")
        self.assertEqual(self.cache_status(second), "hit")

    def test_search_works_without_csrf_token(self):
        response = Client().get(reverse("cjkcms_search"), {"s": "cached"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].is_valid())
