from cjkcms.settings import cms_settings
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template.loader import get_template
from django.test import TestCase
import pytest

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

    @pytest.mark.skip(reason="missing dependencies")
    def test_cardblock_templates(self):
        """Check if all declared template files are accessible."""

        templates = cms_settings.CJKCMS_FRONTEND_TEMPLATES_BLOCKS["cardblock"]

        for tpl in templates:
            # self.assertIsNone(abs_path, f"{logo} not found.")
            try:
                get_template(tpl[0])
            except TemplateDoesNotExist as e:
                self.fail(f"Template not found: {str(e)}")
