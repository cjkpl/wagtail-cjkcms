from django.urls import path

from cjkcms.views import search

urlpatterns = [
    path("", search, name="cjkcms_search"),
]
