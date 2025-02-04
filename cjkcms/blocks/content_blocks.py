"""
Content blocks are for building complex, nested HTML structures that usually
contain sub-blocks, and may require javascript to function properly.
"""

from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from .base_blocks import (
    BaseBlock,
    BaseLayoutBlock,
    ButtonMixin,
    CollectionChooserBlock,
    TagChooserBlock,
)
from .html_blocks import ButtonBlock
from cjkcms.settings import cms_settings


class AccordionBlock(BaseBlock):
    """
    Allows selecting an accordion snippet
    """

    accordion = SnippetChooserBlock("cjkcms.Accordion")

    class Meta:
        template = "cjkcms/blocks/accordion_block.html"
        icon = "bars"
        label = _("Accordion")
        label_format = _("Accordion")


class CardBlock(BaseBlock):
    """
    A component of information with image, text, and buttons.
    """

    image = ImageChooserBlock(
        required=False,
        max_length=255,
        label=_("Image"),
    )
    title = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Title"),
    )
    subtitle = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Subtitle"),
    )
    description = blocks.RichTextBlock(
        features=cms_settings.CJKCMS_RICHTEXT_FEATURES["default"],
        label=_("Body"),
    )
    links = blocks.StreamBlock(
        [("Links", ButtonBlock())],
        blank=True,
        required=False,
        label=_("Links"),
    )

    class Meta:
        template = "cjkcms/blocks/card_foot.html"
        icon = "list-alt"
        label = _("Card")
        label_format = _("{title} (Card)")

    def get_template(self, context=None):
        """Return the default_card_template declared in parent CardGrid,
        otherwise use the default template."""

        if (
            context
            and hasattr(context["self"], "__iter__")
            and "default_card_template" in context["self"]
            and context["self"]["default_card_template"]
        ):
            return context["self"]["default_card_template"]
        else:
            return super().get_template()


class CarouselBlock(BaseBlock):
    """
    Enables choosing a Carousel snippet.
    """

    carousel = SnippetChooserBlock("cjkcms.Carousel")

    class Meta:
        icon = "image"
        label = _("Carousel")
        label_format = _("Carousel")
        template = "cjkcms/blocks/carousel_block.html"


class FilmStripBlock(BaseBlock):
    """
    Enables choosing a Film Strip Snippet.
    """

    film_strip = SnippetChooserBlock("cjkcms.FilmStrip")

    class Meta:
        icon = "image"
        label = _("Film Strip")
        template = "cjkcms/blocks/film_strip_block.html"


class ImageGalleryBlock(BaseBlock):
    """
    Show a collection of images with interactive previews that expand to
    full size images in a modal.
    """

    collection = CollectionChooserBlock(
        required=True,
        label=_("Image Collection"),
    )

    tag = TagChooserBlock(
        required=False,
        label=_("Limit to tag"),
    )

    class Meta:
        template = "cjkcms/blocks/image_gallery_block.html"
        icon = "image"
        label = _("Image Gallery")
        label_format = _("Image Gallery")


class ModalBlock(ButtonMixin, BaseLayoutBlock):
    """
    Renders a button that then opens a popup/modal with content.
    """

    header = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Modal heading"),
    )
    content = blocks.StreamBlock(
        [],
        label=_("Modal content"),
    )
    footer = blocks.StreamBlock(
        [
            (
                "text",
                blocks.CharBlock(
                    icon="file-text-o", max_length=255, label=_("Simple Text")
                ),
            ),  # noqa
            ("button", ButtonBlock()),
        ],
        required=False,
        label=_("Modal footer"),
    )

    class Meta:
        template = "cjkcms/blocks/modal_block.html"
        icon = "window-maximize"
        label = _("Modal")
        label_format = _("Modal")


class NavBaseLinkBlock(BaseBlock):
    display_text = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Display text"),
    )
    image = ImageChooserBlock(
        required=False,
        label=_("Image"),
    )


class NavExternalLinkBlock(NavBaseLinkBlock):
    """
    External link.
    """

    link = blocks.CharBlock(
        required=False,
        label=_("URL"),
    )

    class Meta:
        template = "cjkcms/blocks/external_link_block.html"
        label = _("External Link")
        label_format = "{display_text} (External Link)"


class NavPageLinkBlock(NavBaseLinkBlock):
    """
    Page link.
    """

    page = blocks.PageChooserBlock(
        label=_("Page"),
    )

    class Meta:
        template = "cjkcms/blocks/page_link_block.html"
        label = _("Page Link")
        label_format = "(Page Link)"


class NavDocumentLinkBlock(NavBaseLinkBlock):
    """
    Document link.
    """

    document = DocumentChooserBlock(
        label=_("Document"),
    )

    class Meta:
        template = "cjkcms/blocks/document_link_block.html"
        label = _("Document Link")
        label_format = "{display_text} (Document Link)"


class NavSubLinkBlock(BaseBlock):
    """
    Streamblock for rendering nested sub-links.
    """

    sub_links = blocks.StreamBlock(
        [
            ("page_link", NavPageLinkBlock()),
            ("external_link", NavExternalLinkBlock()),
            ("document_link", NavDocumentLinkBlock()),
        ],
        required=False,
        label=_("Sub-links"),
    )


class NavExternalLinkWithSubLinkBlock(NavSubLinkBlock, NavExternalLinkBlock):
    """
    External link with option for sub-links.
    """

    class Meta:
        label = _("External link with sub-links")
        label_format = "{link} (External link with sub-links)"


class NavPageLinkWithSubLinkBlock(NavSubLinkBlock, NavPageLinkBlock):
    """
    Page link with option for sub-links or showing child pages.
    """

    show_child_links = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_("Show child pages"),
        help_text=_(
            "Automatically show a link to the Page’s child pages as a dropdown menu."
        ),
    )

    class Meta:
        label = _("Page link with sub-links")
        label_format = "{page} (Page link with sub-links)"


class NavDocumentLinkWithSubLinkBlock(NavSubLinkBlock, NavDocumentLinkBlock):
    """
    Document link with option for sub-links.
    """

    class Meta:
        label = _("Document link with sub-links")
        label_format = "{document} (Document link with sub-links)"


class PriceListItemBlock(BaseBlock):
    """
    Represents one item in a PriceListBlock, such as an entree in a restaurant menu.
    """

    image = ImageChooserBlock(
        required=False,
        label=_("Image"),
    )
    name = blocks.CharBlock(
        required=True,
        max_length=255,
        label=_("Name"),
    )
    description = blocks.RichTextBlock(
        required=False,
        rows=4,
        label=_("Description"),
    )
    price = blocks.CharBlock(
        required=True,
        label=_("Price"),
        help_text=_("Any text here. Include currency sign if desired."),
    )

    class Meta:
        template = "cjkcms/blocks/pricelistitem_block.html"
        icon = "usd"
        label = _("Price List Item")
        label_format = _("Price List Item")


class PriceListBlock(BaseBlock):
    """
    A price list, such as a menu for a restaurant.
    """

    heading = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Heading"),
    )
    items = blocks.StreamBlock(
        [
            ("item", PriceListItemBlock()),
        ],
        label=_("Items"),
    )

    class Meta:
        template = "cjkcms/blocks/pricelist_block.html"
        icon = "usd"
        label = _("Price List")


class ReusableContentBlock(BaseBlock):
    """
    Enables choosing a ResusableContent snippet.
    """

    content = SnippetChooserBlock("cjkcms.ReusableContent")

    class Meta:
        icon = "recycle"
        label = _("Reusable Content")
        template = "cjkcms/blocks/reusable_content_block.html"
        label_format = "{content} (Reusable Content)"


class HighlightBlock(BaseBlock):
    """
    Block that highlights a piece of text
    """

    text = blocks.RichTextBlock(
        features=cms_settings.CJKCMS_RICHTEXT_FEATURES["default"],
        label=_("Text"),
    )

    background_color = blocks.ChoiceBlock(
        choices=cms_settings.CJKCMS_HIGHLIGHT_COLORS,
        default=cms_settings.CJKCMS_HIGHLIGHT_DEFAULT_COLOR,
        required=False,
        label=_("Background Color"),
    )

    border_color = blocks.ChoiceBlock(
        choices=cms_settings.CJKCMS_HIGHLIGHT_COLORS,
        default=cms_settings.CJKCMS_HIGHLIGHT_DEFAULT_COLOR,
        required=False,
        label=_("Border Color"),
    )

    text_color = blocks.ChoiceBlock(
        choices=cms_settings.CJKCMS_HIGHLIGHT_COLORS,
        default="dark",
        required=False,
        label=_("Text Color"),
    )

    icon = blocks.ChoiceBlock(
        choices=cms_settings.FONT_AWESOME_ICONS,
        default=cms_settings.FONT_AWESOME_ICONS_DEFAULT,
        required=False,
        label=_("Icon"),
    )

    class Meta:
        icon = "thumbtack"
        label = _("Highlight")
        label_format = _("Highlight")
        template = "cjkcms/blocks/highlight_block.html"
