from cjkcms.models import (
    CjkcmsArticlePage,
    CjkcmsArticleIndexPage,
    CjkcmsWebPage,
)


class ProjectArticlePage(CjkcmsArticlePage):
    template = "cjkcms/pages/article_page.html"
    search_template = "cjkcms/pages/article_page.search.html"


class ProjectArticleIndexPage(CjkcmsArticleIndexPage):
    template = "cjkcms/pages/article_index_page.html"


class ProjectWebPage(CjkcmsWebPage):
    # use cjkcms template by default
    template = "cjkcms/pages/web_page.html"
