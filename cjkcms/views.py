from cjkcms.forms import SearchForm
from cjkcms.models import (
    GeneralSettings,
    LayoutSettings,
)

from django.http import Http404, HttpResponsePermanentRedirect
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from wagtail.models import Page, get_page_models

# from coderedcms.importexport import convert_csv_to_json, import_pages, ImportPagesFromCSVFileForm
from cjkcms.templatetags.cjkcms_tags import get_name_of_class

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.http import JsonResponse
import django
from wagtail import __version__ as wagtail_version
from cjkcms import __version__ as cjkcms_version
import sys


def search(request):
    """
    Searches pages across the entire site.
    """
    search_form = SearchForm(request.GET)
    pagetypes = []
    results = None
    results_paginated = None

    if search_form.is_valid():
        search_query = search_form.cleaned_data["s"]
        search_model = search_form.cleaned_data["t"]

        # get all page models
        pagemodels = sorted(get_page_models(), key=get_name_of_class)
        # filter based on is search_filterable
        for model in pagemodels:
            if hasattr(model, "search_filterable") and model.search_filterable:
                pagetypes.append(model)

        results = Page.objects.live()
        if search_model:
            try:
                # If provided a model name, try to get it
                model = ContentType.objects.get(model=search_model).model_class()
                results = results.type(model)
            except ContentType.DoesNotExist:
                # Maintain existing behavior of only returning objects if the page type is real
                results = None

        # get and paginate results
        if results:
            results = results.search(search_query)
            paginator = Paginator(
                results, GeneralSettings.for_request(request).search_num_results
            )
            page = request.GET.get("p", 1)
            try:
                results_paginated = paginator.page(page)
            except PageNotAnInteger:
                results_paginated = paginator.page(1)
            except EmptyPage:
                results_paginated = paginator.page(1)
            except InvalidPage:
                results_paginated = paginator.page(1)

    # Render template
    return render(
        request,
        "cjkcms/pages/search.html",
        {
            "request": request,
            "pagetypes": pagetypes,
            "form": search_form,
            "results": results,
            "results_paginated": results_paginated,
        },
    )


def favicon(request):
    if icon := LayoutSettings.for_request(request).favicon:
        return HttpResponsePermanentRedirect(icon.get_rendition("original").url)
    raise Http404()


def robots(request):
    return render(request, "cjkcms/robots.txt", content_type="text/plain")


class VersionView(APIView):

    def get(self, request, token):
        monitor_token = settings.CJKCMS_VERSION_MONITOR_TOKEN
        allowed_domains = settings.CJKCMS_VERSION_MONITOR_ALLOWED_DOMAINS

        host = request.META.get("HTTP_HOST")

        token_ok = len(token) < 12 or token != monitor_token
        domain_ok = allowed_domains = ["*"] or host in allowed_domains

        # minimum required token length is 12 characters
        # this also prevents sites from reporting when default
        # empty token has not been replaced in local config with a proper one

        if token_ok and domain_ok:
            return JsonResponse(
                {"error": "Forbidden."}, status=status.HTTP_403_FORBIDDEN
            )

        data = {
            "python": sys.version,
            "django": django.get_version(),
            "wagtail": wagtail_version,
            "cjkcms": cjkcms_version,
        }
        return Response(data)
