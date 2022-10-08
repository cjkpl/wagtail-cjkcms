import pytest
import unittest

from django.urls import reverse
from django.test import Client
from django.test.utils import override_settings

from wagtail.core.models import Site
from wagtail.images.tests.utils import Image, get_test_image_file

from cjkcms.models import LayoutSettings

# from cjkcms.tests.testapp.models import EventPage, EventIndexPage, EventOccurrence


@pytest.mark.django_db
class TestSiteURLs(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    # @TODO: this fails, even though in browser tests returns 404
    @override_settings(DEBUG=False)
    def test_404(self):
        response = self.client.get("/testing/404/page/")
        self.assertEqual(response.status_code, 404)

    def test_sitemap(self):
        response = self.client.get("/sitemap.xml")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/xml")

    def test_robots(self):
        response = self.client.get("/robots.txt")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "text/plain")

    def test_search(self):
        response = self.client.get(
            reverse("cjkcms_search"), {"s": "Test Search Query"}, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context["results"], None)

        response = self.client.get(
            reverse("cjkcms_search"),
            {
                "s": "keyword",
                "t": "t",
            },
            follow=False,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["results"], None)


@pytest.mark.django_db
class TestFavicon(unittest.TestCase):
    def test_404(self):
        client = Client()
        # Get the default site
        site = Site.objects.filter(is_default_site=True)[0]
        # Ensure the favicon is blank
        layout = LayoutSettings.for_site(site)
        layout.favicon = None
        layout.save()
        # Expect a 404
        response = client.get("/favicon.ico")
        self.assertEqual(response.status_code, 404)

    def test_301(self):
        client = Client()
        # Get the default site
        site = Site.objects.filter(is_default_site=True)[0]
        # Set a dummy favicon
        layout = LayoutSettings.for_site(site)
        img = Image.objects.create(
            title="Test image",
            file=get_test_image_file(),
        )
        layout.favicon = img
        layout.save()
        # Expect a 301 redirect
        response = client.get("/favicon.ico")
        self.assertEqual(response.status_code, 301)
