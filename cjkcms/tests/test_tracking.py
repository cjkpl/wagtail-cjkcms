from django.test import Client, TestCase
from wagtail.models import Page, Site

from cjkcms.models import AnalyticsSettings
from cjkcms.models.cms_models import WebPage


class GoogleAnalyticsTrackingTests(TestCase):
    def setUp(self):
        home_page = Page.objects.get(path="00010001")
        self.page = WebPage(title="Tracked", slug="tracked")
        home_page.add_child(instance=self.page)
        self.page.save_revision().publish()
        self.analytics = AnalyticsSettings.for_site(
            Site.objects.get(is_default_site=True)
        )

    def render(self, **settings):
        for name, value in settings.items():
            setattr(self.analytics, name, value)
        self.analytics.save()
        return Client().get(self.page.url).content.decode()

    def test_no_tracking_without_id(self):
        html = self.render()
        self.assertNotIn("gtag(", html)
        self.assertNotIn("googletagmanager.com", html)

    def test_property_is_configured_once(self):
        html = self.render(g4_tracking_id="G-TEST123")

        self.assertIn("https://www.googletagmanager.com/gtag/js?id=G-TEST123", html)
        self.assertEqual(html.count("gtag('config', 'G-TEST123');"), 1)
        # No second, empty property is configured.
        self.assertEqual(html.count("gtag('config'"), 1)
        self.assertEqual(html.count("gtag('js'"), 1)

    def test_button_click_tracking_flag(self):
        html = self.render(g4_tracking_id="G-TEST123", ga_track_button_clicks=False)
        self.assertIn("cms_track_clicks = false;", html)

        html = self.render(ga_track_button_clicks=True)
        self.assertIn("cms_track_clicks = true;", html)
