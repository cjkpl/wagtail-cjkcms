from cjkcms.blocks.base_blocks import BaseBlock
from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from django.utils.translation import gettext_lazy as _


class IsontechPresentationBlock(BaseBlock):
    """
    Isontech-tailored presentation block
    """

    title = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Title"),
    )

    start_time = blocks.TimeBlock(
        required=False,
        label=_("Start time"),
        help_text=_("Format: HH:MM, local time"),
    )

    end_time = blocks.TimeBlock(
        required=False,
        label=_("End time"),
        help_text=_("Format: HH:MM, local time"),
    )

    company = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Company"),
    )

    presenter = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Presenter"),
        help_text=_("Firstname & Lastname"),
    )

    description = blocks.RichTextBlock(
        features=["bold", "italic", "ol", "ul", "hr", "link", "document-link", "image"],
        label=_("Description"),
        help_text=_("Optional, short description of the presentation"),
        required=False,
    )

    image = ImageChooserBlock(
        required=False,
        max_length=255,
        label=_("Image"),
        help_text=_("Logo or image"),
    )

    document = DocumentChooserBlock(
        required=False,
        label=_("Presentation PDF"),
    )

    video_id = blocks.CharBlock(
        max_length=255,
        label=_("YouTube video ID"),
        required=False,
        help_text="Insert YouTube video URL here",
    )

    class Meta:
        # note - in this example we are not adding any html block,
        # you need to add one before you can display your new block
        template = "home/blocks/isontech_presentation.html"
        icon = "view"
        label = "ISoNTech Presentation"
        label_format = _("{title} (ISoNTech Presentation)")


ISONTECH_PRESENTATION_STREAMBLOCKS = [
    ("isontech_presentation", IsontechPresentationBlock()),
]
