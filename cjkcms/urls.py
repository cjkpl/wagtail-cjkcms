from django.urls import include, path
from wagtail.contrib.sitemaps.views import sitemap
from cjkcms import search_urls as cjkcms_search_urls

# from .settings import cms_settings
from cjkcms.views import (
    favicon,
    robots,
)

urlpatterns = [
    # CMS custom URLs
    path("favicon.ico", favicon, name="cjkcms_favicon"),
    path("robots.txt", robots, name="cjkcms_robots"),
    path("sitemap.xml", sitemap, name="cjkcms_sitemap"),
    # Search
    path("search/", include(cjkcms_search_urls)),
]
