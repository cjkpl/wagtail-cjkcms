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
    ImageGalleryBlock,
    ModalBlock,
    NavDocumentLinkWithSubLinkBlock,
    NavExternalLinkWithSubLinkBlock,
    NavPageLinkWithSubLinkBlock,
    PriceListBlock,
    ReusableContentBlock,
)
from .layout_blocks import CardGridBlock, GridBlock, HeroBlock

# Collections of blocks commonly used together.

HTML_STREAMBLOCKS = [
    ("text", RichTextBlock(icon="fa-file-text-o")),
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
    ("image_gallery", ImageGalleryBlock()),
    ("modal", ModalBlock(HTML_STREAMBLOCKS)),
    ("pricelist", PriceListBlock()),
    ("reusable_content", ReusableContentBlock()),
]

NAVIGATION_STREAMBLOCKS = [
    ("page_link", NavPageLinkWithSubLinkBlock()),
    ("external_link", NavExternalLinkWithSubLinkBlock()),
    ("document_link", NavDocumentLinkWithSubLinkBlock()),
]

BASIC_LAYOUT_STREAMBLOCKS = [
    ("row", GridBlock(HTML_STREAMBLOCKS)),
    (
        "html",
        SearchableHTMLBlock(icon="code", form_classname="monospace", label=_("HTML")),
    ),
]

LAYOUT_STREAMBLOCKS = [
    (
        "hero",
        HeroBlock(
            [
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
                    SearchableHTMLBlock(
                        icon="code", form_classname="monospace", label=_("HTML")
                    ),
                ),
            ]
        ),
    ),
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
