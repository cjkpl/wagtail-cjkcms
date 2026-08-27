from cjkcms.models import ArticleIndexPage, ArticlePage, WebPage

from .cms_models import (
    ProjectArticleIndexPage,
    ProjectArticlePage,
    ProjectWebPage,
)

# disable CjkCMS' default page types - we'll use our own
WebPage.max_count = 0
ArticleIndexPage.max_count = 0
ArticlePage.max_count = 0

__all__ = ["ProjectArticleIndexPage", "ProjectArticlePage", "ProjectWebPage"]
