from types import ModuleType
from unittest.mock import patch

from django.apps import AppConfig, apps
from django.contrib.staticfiles import finders
from wagtail import hooks

from cjkcms import __version__
from cjkcms.wagtail_hooks import character_counter_js


def test_character_counter_script_is_registered_and_available():
    assert character_counter_js in hooks.get_hooks("insert_editor_js")
    assert character_counter_js() == (
        f'<script src="/static/cjkcms/js/character-counter.js?v={__version__}"></script>'
    )
    assert finders.find("cjkcms/js/character-counter.js")


def test_character_counter_defers_to_standalone_app():
    module = ModuleType("wagtail_character_counter")
    module.__file__ = __file__
    config = AppConfig("wagtail_character_counter", module)
    # Use a different label, as sites can customize the legacy AppConfig.
    with patch.dict(apps.app_configs, {"legacy_counter": config}):
        assert character_counter_js() == ""

    # Removing the old app activates the bundled counter without other settings.
    assert "cjkcms/js/character-counter.js" in character_counter_js()
