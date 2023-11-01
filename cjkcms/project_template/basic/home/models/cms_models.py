"""
Three main creatable page types used in Cjk CMS.
"""
from django.utils.translation import gettext_lazy as _
from cjkcms.models import (
    CjkcmsArticlePage,
    CjkcmsArticleIndexPage,
    CjkcmsWebPage,
)
from cjkcms.fields import CjkcmsStreamField
from cjkcms.blocks import LAYOUT_STREAMBLOCKS, CONTENT_STREAMBLOCKS
from cjkcms.blocks.layout_blocks import GridBlock
from home.blocks import (
    PROJECT_CONTENT_STREAMBLOCKS,
    PROJECT_LAYOUT_STREAMBLOCKS,
)

# add here custom blocks from other apps used in your project,
# so that they all can be part of the BODY of Web and Article pages.

ALL_CONTENT_STREAMBLOCKS = CONTENT_STREAMBLOCKS + PROJECT_CONTENT_STREAMBLOCKS

ALL_LAYOUT_STREAMBLOCKS = LAYOUT_STREAMBLOCKS + PROJECT_LAYOUT_STREAMBLOCKS

for i, item in enumerate(ALL_LAYOUT_STREAMBLOCKS):
    if item[0] == "row":
        # Replace each 'row' entry with new content blocks
        ALL_LAYOUT_STREAMBLOCKS[i] = (
            "row",
            GridBlock(ALL_CONTENT_STREAMBLOCKS),
        )


class ProjectArticlePage(CjkcmsArticlePage):
    """
    {{ uf_project }} Article, suitable for news or blog content.
    """

    class Meta:
        verbose_name = _("{{ uf_project }} Article")
        ordering = ["-first_published_at"]

    # Uncomment to only allow this page to be created beneath
    # an ArticleIndexPage, or ProjectArticleIndexPage
    # parent_page_types = ['website.ArticleIndexPage']

    # Override to CjkcmsStreamField to get rid of migration issues
    # when modifying CONTENT_STREAMBLOCKS.
    body = CjkcmsStreamField(
        ALL_CONTENT_STREAMBLOCKS, null=True, blank=True, use_json_field=True
    )

    # use cjkcms template by default
    template = "cjkcms/pages/article_page.html"
    search_template = "cjkcms/pages/article_page.search.html"
    search_filterable = True


class ProjectArticleIndexPage(CjkcmsArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """

    # Override to CjkcmsStreamField to get rid of migration issues
    # when modifying LAYOUT_STREAMBLOCKS.
    body = CjkcmsStreamField(
        ALL_LAYOUT_STREAMBLOCKS, null=True, blank=True, use_json_field=True
    )

    class Meta:
        verbose_name = _("{{ uf_project }} Article Landing Page")

    index_order_by_default = ""

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "home.ProjectArticlePage"

    # Only allow ArticlePages beneath this page.
    subpage_types = ["home.ProjectArticlePage", "cjkcms.ArticlePage"]

    # use cjkcms template by default
    template = "cjkcms/pages/article_index_page.html"


class ProjectWebPage(CjkcmsWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    """

    # Override to CjkcmsStreamField to get rid of migration issues
    # when modifying LAYOUT_STREAMBLOCKS.
    body = CjkcmsStreamField(
        ALL_LAYOUT_STREAMBLOCKS, null=True, blank=True, use_json_field=True
    )

    class Meta:
        verbose_name = _("{{ uf_project }} Web Page")

    # use cjkcms template by default
    template = "cjkcms/pages/web_page.html"
