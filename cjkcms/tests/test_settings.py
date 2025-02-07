from cjkcms.models.wagtailsettings_models import AdobeApiSettings
from cjkcms.settings import cms_settings
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from django.test import TestCase
from wagtail.models import Site

# import TemplateDoesNotExist
from django.template import TemplateDoesNotExist

# Test the settings.py file and all templates and static files defined.


class SettingsTests(TestCase):
    def test_brand_logos(self):
        """Check if default brand logos are available."""

        logos = [
            cms_settings.CJKCMS_BRAND_LOGO_LONG,
            cms_settings.CJKCMS_BRAND_LOGO_SQUARE,
        ]

        for logo in logos:
            abs_path = finders.find(logo)
            # self.assertIsNone(abs_path, f"{logo} not found.")
            self.assertTrue(str(abs_path).endswith(logo), f"{logo} not found.")

    def _check_templates(self, templates, skip_empty=False, check_advanced=False):
        """Check if all declared template files specified in the `templates` list
        are accessible and execute without error. Used to check individual
        sections in settings.py. Skip empty templates if `skip_empty` is True.
        Check advanced settings features optionally (custom_id, custom_css_class)"""

        for tpl in templates:
            if skip_empty and not tpl[0]:
                continue
            try:
                tpl = get_template(tpl[0])
                # if check_advanced, ensure that strings {{self.settings.custom_css_class}}
                # and {{self.settings.custom_id}} are present in template source
                if check_advanced:
                    self.assertIn("{{self.settings.custom_css_class}}", tpl.template.source)
                    self.assertIn("{{self.settings.custom_id}}", tpl.template.source)

            except TemplateDoesNotExist as e:
                self.fail(f"Template not found: {str(e)}")

    def test_cardblock_templates(self):
        templates = cms_settings.CJKCMS_FRONTEND_TEMPLATES_BLOCKS["cardblock"]
        self._check_templates(templates, check_advanced=True)

    def test_cardgridblock_templates(self):
        templates = cms_settings.CJKCMS_FRONTEND_TEMPLATES_BLOCKS["cardgridblock"]
        self._check_templates(templates, check_advanced=True)

    def test_pagelistblock_templates(self):
        templates = cms_settings.CJKCMS_FRONTEND_TEMPLATES_BLOCKS["pagelistblock"]
        self._check_templates(templates, check_advanced=True)

    def test_pagepreviewblock_templates(self):
        templates = cms_settings.CJKCMS_FRONTEND_TEMPLATES_BLOCKS["pagepreviewblock"]
        self._check_templates(templates)

    def test_quoteblock_templates(self):
        templates = cms_settings.CJKCMS_FRONTEND_TEMPLATES_BLOCKS["quoteblock"]
        self._check_templates(templates, check_advanced=True)

    def test_frontend_template_pages_templates(self):
        templates = cms_settings.CJKCMS_FRONTEND_TEMPLATES_PAGES["*"]
        self._check_templates(templates, skip_empty=True)

    def test_AdobeApiKey(self):
        site = Site.objects.filter(is_default_site=True)[0]
        adobe_api_key = AdobeApiSettings.for_site(site=site)
        adobe_api_key.adobe_embed_id = "test_key"
        adobe_api_key.save()

        adobe_api_key = AdobeApiSettings.for_site(site=site)
        """Check if the Adobe API Key is set."""
        self.assertEqual(adobe_api_key.adobe_embed_id, "test_key")
