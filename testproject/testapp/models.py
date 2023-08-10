from cjkcms.blocks.content.events import PublicEventBlock
from cjkcms.blocks import LAYOUT_STREAMBLOCKS
from cjkcms.blocks.layout_blocks import (
    GridBlock,
)
from cjkcms.models import (
    CjkcmsArticlePage,
    CjkcmsArticleIndexPage,
    CjkcmsWebPage,
)
from cjkcms.fields import CjkcmsStreamField


# add your own content block
PROJECT_CONTENT_STREAMBLOCKS = [
    ("public_event", PublicEventBlock()),
]

PROJECT_LAYOUT_STREAMBLOCKS = [
    # ("custom_block", CustomBlock()),
] + LAYOUT_STREAMBLOCKS

for i, item in enumerate(PROJECT_LAYOUT_STREAMBLOCKS):
    if item[0] == "row":
        # Replace each 'row' entry with new content blocks
        PROJECT_LAYOUT_STREAMBLOCKS[i] = (
            "row",
            GridBlock(PROJECT_CONTENT_STREAMBLOCKS),
        )


class ProjectArticlePage(CjkcmsArticlePage):
    body = CjkcmsStreamField(
        PROJECT_CONTENT_STREAMBLOCKS, null=True, blank=True, use_json_field=True
    )
    template = "cjkcms/pages/article_page.html"


class ProjectArticleIndexPage(CjkcmsArticleIndexPage):
    body = CjkcmsStreamField(
        PROJECT_LAYOUT_STREAMBLOCKS, null=True, blank=True, use_json_field=True
    )
    template = "cjkcms/pages/article_index_page.html"


class ProjectWebPage(CjkcmsWebPage):
    body = CjkcmsStreamField(
        PROJECT_LAYOUT_STREAMBLOCKS, null=True, blank=True, use_json_field=True
    )
    template = "cjkcms/pages/web_page.html"
