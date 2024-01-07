import unittest
from unittest.mock import Mock

from cjkcms.draftail import (
    register_block_feature,
    register_inline_styling,
    NewWindowExternalLinkHandler,
)
from cjkcms.draftail.draftail_extensions import create_control_dict


class TestCreateControlDict(unittest.TestCase):
    def test_create_control_dict_basic(self):
        control = create_control_dict("bold", "Bold")
        self.assertEqual(
            control, {"type": "bold", "description": "Bold", "label": "Bold"}
        )

    def test_create_control_dict_with_optional_args(self):
        control = create_control_dict(
            "italic", "Italic", label="Italic Style", editor_style="font-style:italic;"
        )
        self.assertEqual(
            control,
            {
                "type": "italic",
                "description": "Italic",
                "label": "Italic Style",
                "style": "font-style:italic;",
            },
        )


class TestRegisterFeatures(unittest.TestCase):
    def setUp(self):
        self.mock_features = Mock()

    def test_register_inline_styling(self):
        register_inline_styling(
            self.mock_features, "custom-style", "Custom Style", "CUSTOM", tag="span"
        )
        self.mock_features.register_editor_plugin.assert_called()
        self.mock_features.register_converter_rule.assert_called()

    def test_register_block_feature(self):
        register_block_feature(
            self.mock_features,
            "custom-block",
            "Custom Block",
            "CUSTOM-BLOCK",
            "custom-class",
        )
        self.mock_features.register_editor_plugin.assert_called()
        self.mock_features.register_converter_rule.assert_called()


class TestNewWindowExternalLinkHandler(unittest.TestCase):
    def test_expand_db_attributes_with_blank(self):
        result = NewWindowExternalLinkHandler.expand_db_attributes(
            {"href": "http://example.com?_blank"}
        )
        self.assertIn('target="_blank"', result)
        self.assertIn('rel="noopener noreferrer"', result)

    def test_expand_db_attributes_without_blank(self):
        result = NewWindowExternalLinkHandler.expand_db_attributes(
            {"href": "http://example.com"}
        )
        self.assertNotIn('target="_blank"', result)
        self.assertNotIn('rel="noopener noreferrer"', result)
