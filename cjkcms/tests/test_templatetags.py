import re

from django.template import engines
from django.test import TestCase
from wagtail.core.models import Site
from cjkcms.models import AdobeApiSettings


django_engine = engines["django"]
html_id_re = re.compile(r"^[A-Za-z][A-Za-z0-9_:.-]*$")

version_re = re.compile(
    r"^(\d+!)?(\d+)(\.\d+)+([\.\-\_])?((a(lpha)?|b(eta)?|c|r(c|ev)?|pre(view)?)\d*)?(\.?(post|dev)\d*)?$"  # noqa: E501
)


class TemplateTagTests(TestCase):
    def test_cjkcms_generate_random_id(self):
        count = 1000
        t = django_engine.from_string(
            "{% load cjkcms_tags %}{% generate_random_id as rid %}{{rid}}"
        )

        ids = set([])
        for _ in range(count):
            ids.add(t.render(None))
        self.assertEqual(len(ids), count)
        for i, value in enumerate(ids, start=1):
            self.assertTrue(
                html_id_re.match(value),
                'ID #%s "%s" did not match regex %r' % (i, value, html_id_re),
            )

    def test_cjkcms_version(self):
        rt = django_engine.from_string(
            "{% load cjkcms_tags %}{% cjkcms_version %}"
        ).render(None)
        self.assertTrue(
            version_re.match(rt),
            "App Version format incorrect: %r" % version_re,
        )

    def test_django_settings_filter(self):
        rt = django_engine.from_string(
            "{% load cjkcms_tags %}{{ 'APPEND_SLASH'|django_settings  }}"
        ).render(None)
        self.assertIn(
            rt,
            ["True", "False"],
            f"Django setting APPEND_SLASH is neither True nor False, instead is {rt}",
        )

    def test_map_to_bootstrap_alert_filter(self):
        rt = django_engine.from_string(
            "{% load cjkcms_tags %}{{ 'error'|map_to_bootstrap_alert }}"
        ).render(None)
        self.assertEqual(
            rt, "danger", "map_to_bootstrap_alert for 'error' did not return 'danger'"
        )

    def test_brand_logo_long_tag(self):
        rt = django_engine.from_string(
            "{% load cjkcms_tags %}{% brand_logo_long %}"
        ).render(None)
        self.assertIn(
            rt[-4:],
            [".png", ".jpg", ".webp", ".svg"],
            f"Django setting BRAND_LOGO_LONG does not seem to return one of [png,jpg,webp,svg]: {rt}",  # noqa: E501
        )

    def test_brand_logo_square_tag(self):
        rt = django_engine.from_string(
            "{% load cjkcms_tags %}{% brand_logo_square %}"
        ).render(None)
        self.assertIn(
            rt[-4:],
            [".png", ".jpg", ".webp", ".svg"],
            f"Django setting BRAND_LOGO_LONG does not seem to return one of [png,jpg,webp,svg]: {rt}",  # noqa: E501
        )

    def test_AdobeApiKeyInTemplate(self):
        site = Site.objects.filter(is_default_site=True)[0]
        adobe_api_key = AdobeApiSettings.for_site(site=site)
        adobe_api_key.adobe_embed_id = "test_key"
        adobe_api_key.save()

        rt = django_engine.from_string(
            "{% load wagtailsettings_tags %}{% get_settings use_default_site=True %}{{ settings.cjkcms.AdobeApiSettings.adobe_embed_id }}"  # noqa: E501
        ).render(None)
        self.assertEqual(
            rt, "test_key", "Adobe API key not returned in template context"
        )
