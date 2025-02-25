"""
Blocks module entry point. Used to cleanly organize blocks into
individual files based on purpose, but provide them all as a
single `blocks` module.
"""

from django.utils.translation import gettext_lazy as _

from .html_blocks import (
    ButtonBlock,
    ImageBlock,
    ImageLinkBlock,
    DownloadBlock,
    EmbedVideoBlock,
    PageListBlock,
    PagePreviewBlock,
    QuoteBlock,
    RichTextBlock,
    TableBlock,
    SearchableHTMLBlock,
)
from .content_blocks import (  # noqa
    AccordionBlock,
    CardBlock,
    CarouselBlock,
    FilmStripBlock,
    ImageGalleryBlock,
    ModalBlock,
    NavDocumentLinkWithSubLinkBlock,
    NavExternalLinkWithSubLinkBlock,
    NavPageLinkWithSubLinkBlock,
    PriceListBlock,
    ReusableContentBlock,
    HighlightBlock,
)
from .content.events import PublicEventBlock, EventCalendarBlock
from .content.countdown import CountdownBlock
from .layout_blocks import CardGridBlock, GridBlock, HeroBlock
from cjkcms.settings import cms_settings

# Collections of blocks commonly used together.

HTML_STREAMBLOCKS = [
    (
        "text",
        RichTextBlock(
            icon="font",
            features=cms_settings.CJKCMS_RICHTEXT_FEATURES["full"],
        ),
    ),
    ("button", ButtonBlock()),
    ("image", ImageBlock()),
    ("image_link", ImageLinkBlock()),
    (
        "html",
        SearchableHTMLBlock(
            icon="code",
            form_classname="monospace",
            label=_("HTML"),
        ),
    ),
    ("download", DownloadBlock()),
    ("embed_video", EmbedVideoBlock()),
    ("quote", QuoteBlock()),
    ("table", TableBlock()),
    ("page_list", PageListBlock()),
    ("page_preview", PagePreviewBlock()),
]

CONTENT_STREAMBLOCKS = HTML_STREAMBLOCKS + [
    ("accordion", AccordionBlock()),
    ("card", CardBlock()),
    ("carousel", CarouselBlock()),
    ("filmstrip", FilmStripBlock()),
    ("image_gallery", ImageGalleryBlock()),
    ("modal", ModalBlock(HTML_STREAMBLOCKS)),
    ("pricelist", PriceListBlock()),
    ("reusable_content", ReusableContentBlock()),
    ("event_calendar", EventCalendarBlock()),
    ("highlight", HighlightBlock()),
    ("countdown", CountdownBlock()),
]

NAVIGATION_STREAMBLOCKS = [
    ("page_link", NavPageLinkWithSubLinkBlock()),
    ("external_link", NavExternalLinkWithSubLinkBlock()),
    ("document_link", NavDocumentLinkWithSubLinkBlock()),
]

PUBLIC_EVENT_STREAMBLOCKS = [
    ("event", PublicEventBlock()),
]

BASIC_LAYOUT_STREAMBLOCKS = [
    ("row", GridBlock(HTML_STREAMBLOCKS)),
    (
        "html",
        SearchableHTMLBlock(icon="code", form_classname="monospace", label=_("HTML")),
    ),
]

FLAT_LAYOUT_STREAMBLOCKS = [
    ("row", GridBlock(CONTENT_STREAMBLOCKS)),
    (
        "cardgrid",
        CardGridBlock(
            [
                ("card", CardBlock()),
            ]
        ),
    ),
    (
        "html",
        SearchableHTMLBlock(icon="code", form_classname="monospace", label=_("HTML")),
    ),
]

LAYOUT_STREAMBLOCKS = [
    ("hero", HeroBlock(FLAT_LAYOUT_STREAMBLOCKS)),
    *FLAT_LAYOUT_STREAMBLOCKS,
]


def replace_contentblocks(flat_layout_blocks, full_layout_blocks, new_content_blocks):
    """helper function to add new content blocks in projects,
    replacing the default content blocks in the layout blocks.

    Args:
        flat_layout_blocks (_type_): CJKCMS layout blocks which contains "row" of content blocks
        full_layout_blocks (_type_): CJKCMS outer layout with hero and flat layout blocks
        new_content_blocks (_type_): full set of new content blocks to replace the old ones

    Returns:
        full_layout_blocks: full layout blocks with new content blocks, readty to include
        in the project models' body fields
    """
    for i, item in enumerate(flat_layout_blocks):
        if item[0] == "row":
            # Replace each 'row' entry with new content blocks
            flat_layout_blocks[i] = (
                "row",
                GridBlock(new_content_blocks),
            )
    full_layout_blocks = [
        (
            "hero",
            HeroBlock(flat_layout_blocks),
        ),
        *flat_layout_blocks,
    ]
    return full_layout_blocks
