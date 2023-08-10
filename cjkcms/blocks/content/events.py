from cjkcms.blocks.base_blocks import BaseBlock
from wagtail import blocks
from django.utils.translation import gettext_lazy as _


class PublicEventBlock(BaseBlock):
    """
    Entry to form a List of public events
    """

    title = blocks.CharBlock(
        required=True,
        max_length=255,
        label=_("Title"),
    )

    location = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Location"),
        help_text=_("Country and city of the event"),
    )

    start_date = blocks.DateBlock(
        required=True,
        label=_("Start date"),
        help_text=_("Format: YYYY-MM-DD"),
    )

    end_date = blocks.DateBlock(
        required=False,
        label=_("End date"),
        help_text=_("Format: YYYY-MM-DD"),
    )

    description = blocks.RichTextBlock(
        features=["bold", "italic", "ol", "ul", "hr", "link", "document-link", "image"],
        label=_("Description"),
        help_text=_("Optional, short description of the event"),
        required=False,
    )

    url = blocks.URLBlock(
        max_length=255,
        label=_("Event website"),
        required=False,
    )

    hide_after_end_date = blocks.BooleanBlock(
        required=False,
        default=True,
        label=_("Hide after end date"),
        help_text=_("Hide this event after its end date"),
    )

    class Meta:
        template = "cjkcms/blocks/public_event_block.html"
        icon = "view"
        label = "Public Event"
        label_format = _("{title} (Event)")
