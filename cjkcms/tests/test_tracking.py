from django.test import Client, TestCase, override_settings
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


class GoogleTagManagerTests(TestCase):
    GTM_SCRIPT = "https://www.googletagmanager.com/gtm.js"
    GTM_NOSCRIPT = "https://www.googletagmanager.com/ns.html?id=GTM-TEST123"

    def setUp(self):
        home_page = Page.objects.get(path="00010001")
        self.page = WebPage(title="Tagged", slug="tagged")
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

    def test_off_by_default_even_with_id(self):
        html = self.render(gtm_id="GTM-TEST123")

        self.assertNotIn("googletagmanager.com", html)
        self.assertNotIn("GTM-TEST123", html)

    @override_settings(CJKCMS_GTM_ENABLED=True)
    def test_enabled_without_id_renders_nothing(self):
        self.assertNotIn("googletagmanager.com", self.render(gtm_id=""))

    @override_settings(CJKCMS_GTM_ENABLED=True)
    def test_enabled_with_id(self):
        html = self.render(gtm_id="GTM-TEST123")
        head, body = html.split("</head>")

        self.assertEqual(head.count(self.GTM_SCRIPT), 1)
        # The ID is escaped for JavaScript, where \u002D is a hyphen.
        self.assertIn("'dataLayer','GTM\\u002DTEST123');", head)
        self.assertIn("<script>", head.split("<!-- Google Tag Manager -->")[1])
        self.assertEqual(body.count(self.GTM_NOSCRIPT), 1)

    @override_settings(CJKCMS_GTM_ENABLED=True)
    def test_waits_for_cookie_consent(self):
        html = self.render(gtm_id="GTM-TEST123", cookie_consent=True)

        self.assertIn(
            '<script type="text/plain" data-cookiecategory="analytics">',
            html.split("<!-- Google Tag Manager -->")[1],
        )
        # The noscript iframe would load without consent.
        self.assertNotIn("ns.html", html)

    @override_settings(CJKCMS_GTM_ENABLED=True)
    def test_id_is_escaped(self):
        html = self.render(gtm_id="GTM-X');alert(1);//")

        self.assertNotIn("alert(1);//');", html)
        self.assertIn("\\u0027", html)

