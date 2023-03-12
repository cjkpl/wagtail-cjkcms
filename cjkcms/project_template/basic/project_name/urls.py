from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from cjkcms import urls as cjkcms_urls


urlpatterns = [
    path("django-backend/", admin.site.urls),
    path("backend/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    # and add cjkcms urls
    path("", include(cjkcms_urls)),
    # default wagtail urls
    path("", include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
