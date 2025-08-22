from django.utils.translation import gettext_lazy as _
from wagtail import blocks

from cjkcms.blocks.base_blocks import BaseBlock


class StepItemBlock(blocks.StructBlock):
    """A single step: icon and title (caption)."""

    icon = blocks.CharBlock(required=True, label=_("Icon"))
    title = blocks.CharBlock(required=True, max_length=255, label=_("Title"))
    is_active = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_("Active"),
        help_text=_("If active, the step will be highlighted."),
    )

    class Meta:
        icon = "minus"
        label = _("Step Item")
        label_format = _("Step: {title}")


class StepsColorSettingsBlock(blocks.StructBlock):
    """
    Color settings for the steps block.
    """

    icon_color = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Icon color"),
    )
    icon_border_color = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Icon border color"),
    )
    icon_background_color = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Icon background color"),
    )

    active_icon_color = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Active icon color"),
    )
    active_icon_border_color = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Active icon border color"),
    )
    active_icon_background_color = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Active icon background color"),
    )

    line_color = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Connector line color"),
    )


class StepsBlock(BaseBlock):
    """Horizontal steps with connecting line."""

    items = blocks.ListBlock(StepItemBlock(), label=_("Steps"))
    color_settings = StepsColorSettingsBlock(
        required=False,
        label=_("Color settings"),
        help_text=_("Hex/RGBA/CSS color. Leave blank to use default styles."),
    )

    class Meta:
        icon = "list-ol"
        label = _("Steps")
        label_format = _("Steps: {items}")
        template = "cjkcms/blocks/steps_block.html"
