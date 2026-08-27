
from django.utils.html import escape
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    BlockElementHandler,
    InlineStyleElementHandler,
)
from wagtail.admin.rich_text.editors.draftail.features import (
    BlockFeature,
    InlineStyleFeature,
)
from wagtail.rich_text import LinkHandler


def create_control_dict(
    type_: str,
    description: str,
    label: str | None = None,
    icon: str | None = None,
    editor_style: str | None = None,
) -> dict[str, str]:
    """
    Helper function to create a control dictionary.
    """
    control = {"type": type_, "description": description}
    if label:
        control["label"] = label
    elif icon:
        control["icon"] = icon
    else:
        control["label"] = description
    if editor_style:
        control["style"] = editor_style
    return control


def register_inline_styling(
    features,
    feature_name: str,
    description: str,
    type_: str,
    tag: str = "span",
    format: str | None = None,
    editor_style: str | None = None,
    label: str | None = None,
    icon: str | None = None,
):
    """
    Registers an inline style feature in the Wagtail editor.
    """
    control = create_control_dict(type_, description, label, icon, editor_style)

    style_map = f"{tag} {format}" if format else {"element": tag}
    markup_map = f"{tag}[{format}]" if format else tag

    features.register_editor_plugin(
        "draftail", feature_name, InlineStyleFeature(control)
    )
    db_conversion = {
        "from_database_format": {markup_map: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: style_map}},
    }
    features.register_converter_rule("contentstate", feature_name, db_conversion)


def register_block_feature(
    features,
    feature_name: str,
    description: str,
    type_: str,
    css_class: str,
    element: str = "div",
    label: str | None = None,
    icon: str | None = None,
    editor_style: str | None = None,
):
    """
    Registers a block feature in the Wagtail editor.
    """
    control = create_control_dict(type_, description, label, icon, editor_style)
    control["element"] = element

    features.register_editor_plugin("draftail", feature_name, BlockFeature(control))
    features.register_converter_rule(
        "contentstate",
        feature_name,
        {
            "from_database_format": {
                f"{element}[class={css_class}]": BlockElementHandler(type_)
            },
            "to_database_format": {
                "block_map": {
                    type_: {"element": element, "props": {"class": css_class}}
                }
            },
        },
    )


class NewWindowExternalLinkHandler(LinkHandler):
    """
    A link handler for opening external links in a new window.
    """

    identifier = "external"

    @classmethod
    def expand_db_attributes(cls, attrs: dict[str, str]) -> str:
        href = attrs["href"]
        if href.endswith("?_blank"):
            href = href[:-7]
            return (
                f'<a href="{escape(href)}" target="_blank" rel="noopener noreferrer">'
            )
        return f'<a href="{escape(href)}">'
