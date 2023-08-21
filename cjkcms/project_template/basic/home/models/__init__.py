from .cms_models import (
    ProjectArticlePage,
    ProjectArticleIndexPage,
    ProjectWebPage,
)

from cjkcms.models import WebPage, ArticleIndexPage, ArticlePage

# disable CjkCMS' default page types - we'll use our own
WebPage.max_count = 0
ArticleIndexPage.max_count = 0
ArticlePage.max_count = 0

__all__ = ["ProjectWebPage", "ProjectArticleIndexPage", "ProjectArticlePage"]
