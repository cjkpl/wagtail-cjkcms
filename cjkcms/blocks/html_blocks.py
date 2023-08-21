"""
HTML blocks are simple blocks used to represent common HTML elements,
with additional styling and attributes.

HTML blocks should NOT contain more sub-blocks or sub-streamfields.
They must be safe to nest within more robust "content blocks" without
creating recursion.
"""
import logging

from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.table_block.blocks import TableBlock as WagtailTableBlock
from wagtail import blocks
from wagtail.rich_text import get_text_for_indexing
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

from .base_blocks import (
    BaseBlock,
    BaseLinkBlock,
    ButtonMixin,
    CjkcmsAdvTrackingSettings,
    ClassifierTermChooserBlock,
    LinkStructValue,
)

logger = logging.getLogger("cjkcms")


class ButtonBlock(ButtonMixin, BaseLinkBlock):
    """
    A link styled as a button.
    """

    class Meta:
        template = "cjkcms/blocks/button_block.html"
        icon = "hand-pointer-o"
        label = _("Button Link")
        label_format = "{button_title} (Button Link)"
        value_class = LinkStructValue


class DownloadBlock(ButtonMixin, BaseBlock):
    """
    Link to a file that can be downloaded.
    """

    automatic_download = blocks.BooleanBlock(
        required=False,
        label=_("Auto download"),
    )
    downloadable_file = DocumentChooserBlock(
        required=False,
        label=_("Document link"),
    )

    advsettings_class = CjkcmsAdvTrackingSettings

    class Meta:
        template = "cjkcms/blocks/download_block.html"
        icon = "download"
        label = _("Download")


class EmbedVideoBlock(BaseBlock):
    """
    Embedded media using stock wagtail functionality.
    """

    url = EmbedBlock(
        required=True,
        label=_("URL"),
        help_text=_("Link to a YouTube/Vimeo video, tweet, facebook post, etc."),
    )

    class Meta:
        template = "cjkcms/blocks/embed_video_block.html"
        icon = "media"
        label = _("Embed Media")


class H1Block(BaseBlock):
    """
    An <h1> heading.
    """

    text = blocks.CharBlock(
        max_length=255,
        label=_("Text"),
    )

    class Meta:
        template = "cjkcms/blocks/h1_block.html"
        icon = "header"
        label = _("Heading 1")


class H2Block(BaseBlock):
    """
    An <h2> heading.
    """

    text = blocks.CharBlock(
        max_length=255,
        label=_("Text"),
    )

    class Meta:
        template = "cjkcms/blocks/h2_block.html"
        icon = "header"
        label = _("Heading 2")


class H3Block(BaseBlock):
    """
    An <h3> heading.
    """

    text = blocks.CharBlock(
        max_length=255,
        label=_("Text"),
    )

    class Meta:
        template = "cjkcms/blocks/h3_block.html"
        icon = "header"
        label = _("Heading 3")


class TableBlock(BaseBlock):
    table = WagtailTableBlock()

    class Meta:
        template = "cjkcms/blocks/table_block.html"
        icon = "table"
        label = _("Table")


class ImageBlock(BaseBlock):
    """
    An <img>, by default styled responsively to fill its container.
    """

    image = ImageChooserBlock(
        label=_("Image"),
    )

    class Meta:
        template = "cjkcms/blocks/image_block.html"
        icon = "image"
        label = _("Image")
        label_format = "Image: {image}"


class ImageLinkBlock(BaseLinkBlock):
    """
    An &lt;a&gt; with an image inside it, instead of text.
    """

    image = ImageChooserBlock(
        label=_("Image"),
    )
    alt_text = blocks.CharBlock(
        max_length=255,
        required=True,
        help_text=_("Alternate text to show if the image doesn’t load"),
    )

    class Meta:
        template = "cjkcms/blocks/image_link_block.html"
        icon = "image"
        label = _("Image Link")
        value_class = LinkStructValue
        label_format = "Image link: {image}"


class PageListBlock(BaseBlock):
    """
    Renders a preview of selected pages.
    """

    # default miniview template, overridden by individual page models
    miniview_template = "cjkcms/pages/page.mini.html"

    indexed_by = blocks.PageChooserBlock(
        required=False,
        label=_("Parent page"),
        help_text=_(
            "Preview of pages that are children of the selected page (default to own parent). Uses ordering specified in the page’s LAYOUT tab."  # noqa
        ),
    )
    classified_by = ClassifierTermChooserBlock(
        required=False,
        label=_("Classified as"),
        help_text=_("Only show pages that are classified with this term."),
    )

    # DEPRECATED - replaced with mini-views
    show_preview = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_("Show body preview"),
    )
    show_dates = blocks.BooleanBlock(
        required=False,
        default=True,
        label=_("Show publish dates"),
    )

    show_authors = blocks.BooleanBlock(
        required=False,
        default=True,
        label=_("Show authors"),
    )

    show_covers = blocks.BooleanBlock(
        required=False,
        default=True,
        label=_("Show cover images"),
        help_text=_("Show cover images"),
    )

    show_navigation = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_("Show navigation"),
        help_text=_("Show prev / next navigation buttons"),
    )

    num_posts = blocks.IntegerBlock(
        default=10,
        label=_("Number of pages to show"),
    )

    title = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Title"),
    )

    class Meta:
        template = "cjkcms/blocks/pagelist_block.html"
        icon = "list-ul"
        label = _("Latest Pages")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        if not parent_context:
            return context

        try:
            current_page = parent_context["page"]
        except KeyError:  # e.g. in search results
            return context

        if value["indexed_by"]:
            indexer = value["indexed_by"].specific
        else:
            indexer = current_page.get_parent().specific

        # try to use the CjkcmsPage `get_index_children()`,
        # but fall back to get_children if this is a non-CjkcmsPage
        if hasattr(indexer, "get_index_children"):
            pages = indexer.get_index_children().live()
            if value["classified_by"]:
                try:
                    pages = pages.filter(classifier_terms=value["classified_by"])
                except AttributeError:
                    # `pages` is not a queryset, or is not a queryset of CjkcmsPage.
                    logger.warning(
                        "Tried to filter by ClassifierTerm in PageListBlock, but <%s.%s ('%s')>.get_index_children()  # noqadid not return a queryset or is not a queryset of CjkcmsPage models.",  # noqa
                        indexer._meta.app_label,
                        indexer.__class__.__name__,
                        indexer.title,
                    )
        else:
            pages = indexer.get_children().live()

        pages_limited = pages[: value["num_posts"]]

        context["current_page"] = current_page

        # current_index = list(pages_limited.values_list("id", flat=True)).index(
        #     current_page.id
        # )
        # print(current_index)
        previous_page = None
        next_page = None
        current_index = -2

        page_count = len(list(pages_limited))
        for index, item in enumerate(pages_limited):
            if item.id == current_page.id:
                current_index = index

        for index, item in enumerate(pages_limited):
            if (index == current_index - 1) and (index >= 0):
                previous_page = item
            if (index == current_index + 1) and (index < page_count):
                next_page = item

        context["previous_page"] = previous_page
        context["next_page"] = next_page
        context["pages"] = pages_limited
        context["miniview_template"] = self.miniview_template
        return context


class PagePreviewBlock(BaseBlock):
    """
    Renders a preview of a specific page.
    """

    page = blocks.PageChooserBlock(
        required=True,
        label=_("Page to preview"),
        help_text=_("Show a mini preview of the selected page."),
    )

    class Meta:
        template = "cjkcms/blocks/pagepreview_block.html"
        icon = "doc-empty-inverse"
        label = _("Page Preview")


class QuoteBlock(BaseBlock):
    """
    A <blockquote>.
    """

    text = blocks.TextBlock(
        required=True,
        rows=4,
        label=_("Quote Text"),
    )
    author = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Author"),
    )

    class Meta:
        template = "cjkcms/blocks/quote_block.html"
        icon = "openquote"
        label = _("Quote")


class RichTextBlock(blocks.RichTextBlock):
    class Meta:
        template = "cjkcms/blocks/rich_text_block.html"


class SearchableHTMLBlock(blocks.RawHTMLBlock):
    """RawHTMLBlock extended with basic search support"""

    def get_searchable_content(self, value):
        # Strip HTML tags to prevent search backend from indexing them
        source = force_str(value)
        return [get_text_for_indexing(source)]
