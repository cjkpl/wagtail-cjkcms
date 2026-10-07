import re

from django.test import Client, TestCase, override_settings
from wagtail.models import Page, Site

from cjkcms.models import LayoutSettings
from cjkcms.models.cms_models import WebPage
from cjkcms.settings import cms_settings
from cjkcms.templatetags.cjkcms_tags import asset_integrity

FONT_AWESOME_URL = (
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"
)


def tag_for(html, url):
    """Returns the <link> or <script> tag which loads the url."""
    return re.search(r"<(?:link|script)\b[^>]*" + re.escape(url) + "[^>]*>", html)[0]


class AssetIntegrityTests(TestCase):
    def setUp(self):
        home_page = Page.objects.get(path="00010001")
        self.page = WebPage(title="Assets", slug="assets")
        home_page.add_child(instance=self.page)
        self.page.save_revision().publish()
        self.layout = LayoutSettings.for_site(Site.objects.get(is_default_site=True))

    def render(self, **layout):
        for name, value in layout.items():
            setattr(self.layout, name, value)
        self.layout.save()
        return Client().get(self.page.url).content.decode()

    def test_every_cdn_theme_file_has_a_hash(self):
        urls = {
            url
            for files in cms_settings.CJKCMS_THEME_FILES.values()
            for url in files
            if url.startswith("https")
        }
        urls.add(FONT_AWESOME_URL)
        self.assertEqual(urls, set(cms_settings.CJKCMS_ASSET_INTEGRITY))
        for integrity in cms_settings.CJKCMS_ASSET_INTEGRITY.values():
            self.assertRegex(integrity, r"^sha384-[A-Za-z0-9+/]{64}$")

    def test_tag_returns_nothing_for_unknown_url(self):
        self.assertEqual(asset_integrity("https://example.com/theme.css"), "")
        self.assertEqual(asset_integrity("vendor/mdb/css/mdb.min.css"), "")

    def test_cdn_themes_are_loaded_with_integrity(self):
        for theme in ("bootstrap5", "mdb", "bootswatch.flatly"):
            with self.subTest(theme=theme):
                html = self.render(frontend_theme=theme)
                for url in cms_settings.CJKCMS_THEME_FILES[theme]:
                    tag = tag_for(html, url)
                    integrity = cms_settings.CJKCMS_ASSET_INTEGRITY[url]
                    self.assertIn(f'integrity="{integrity}"', tag)
                    self.assertIn('crossorigin="anonymous"', tag)

    def test_font_awesome_is_loaded_with_integrity(self):
        html = self.render(awesome_cdn=True)
        integrity = cms_settings.CJKCMS_ASSET_INTEGRITY[FONT_AWESOME_URL]
        self.assertIn(f'integrity="{integrity}"', tag_for(html, FONT_AWESOME_URL))

    def test_local_theme_has_no_integrity(self):
        html = self.render(frontend_theme="mdb.light")
        for path in cms_settings.CJKCMS_THEME_FILES["mdb.light"]:
            self.assertNotIn("integrity", tag_for(html, f"/static/{path}"))

    def test_project_theme_urls_have_no_integrity(self):
        theme_files = {
            "bootstrap5": [
                "https://cdn.example.com/bootstrap.css",
                "https://cdn.example.com/bootstrap.js",
            ]
        }
        with override_settings(CJKCMS_THEME_FILES=theme_files):
            html = self.render(frontend_theme="bootstrap5")
        for url in theme_files["bootstrap5"]:
            self.assertNotIn("integrity", tag_for(html, url))

    def test_integrity_can_be_switched_off(self):
        with override_settings(CJKCMS_ASSET_INTEGRITY={}):
            html = self.render(frontend_theme="bootstrap5")
        for url in cms_settings.CJKCMS_THEME_FILES["bootstrap5"]:
            self.assertNotIn("integrity", tag_for(html, url))
