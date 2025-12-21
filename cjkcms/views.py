from collections import OrderedDict
import contextlib
from datetime import date, datetime
from typing import Any

from django.apps import apps
from django.core.paginator import EmptyPage, InvalidPage, PageNotAnInteger, Paginator
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.utils import timezone, translation
from wagtail.models import Page
from wagtail.search import index
from wagtail.search.backends import get_search_backend

from cjkcms.forms import SearchForm
from cjkcms.models import (
    GeneralSettings,
    LayoutSettings,
)

from wagtail.models import Locale


# Lists of common datetime attributes used for sorting pages and other models.
UPDATED_FIELD_NAMES = (
    "latest_revision_created_at",
    "last_published_at",
    "updated_at",
    "last_updated",
    "modified",
    "modified_at",
)
CREATED_FIELD_NAMES = (
    "first_published_at",
    "created_at",
    "created",
    "published_at",
    "pub_date",
)


def search_model_backend(model, search_query, current_locale):
    """
    Helper function to search a specific model with the search backend.

    Parameters:
    - model: The model to search.
    - search_query: The query string to search for.
    - current_locale: The current locale for filtering pages.

    Returns:
    - list: Search results for the model.
    """
    backend = get_search_backend()
    if issubclass(model, Page):
        # Search only live and public pages for models that are Page subclasses
        queryset = model.objects.live().public()
        if current_locale:
            queryset = queryset.filter(locale=current_locale)
        return backend.search(search_query, queryset)
    else:
        # Search normally for non-page models
        return backend.search(search_query, model)


def _model_identifier(model):
    return f"{model._meta.app_label}.{model._meta.model_name}"


def _get_request_locale(request):
    language_code = getattr(request, "LANGUAGE_CODE", None) or translation.get_language()
    if language_code:
        normalized = language_code.split("-")[0]
        with contextlib.suppress(Locale.DoesNotExist):
            return Locale.objects.get(language_code=normalized)
    with contextlib.suppress(Locale.DoesNotExist):
        return Locale.get_active()
    with contextlib.suppress(Locale.DoesNotExist):
        return Locale.get_default()
    return Locale.objects.first()


def _value_from_attrs(obj: Any, attrs: tuple[str, ...]):
    """
    Returns the first non-empty attribute found on obj from attrs.
    """
    for attr in attrs:
        value = getattr(obj, attr, None)
        if callable(value):
            with contextlib.suppress(TypeError):
                value = value()
        if value:
            return value
    return None


def _coerce_datetime(value: Any):
    """
    Convert date/datetime values to timezone-aware datetime for comparisons.
    """
    if isinstance(value, date) and not isinstance(value, datetime):
        value = datetime.combine(value, datetime.min.time())
    if isinstance(value, datetime):
        if timezone.is_naive(value):
            value = timezone.make_aware(value, timezone.get_current_timezone())
        return value
    return None


def _timestamp_key(obj: Any, attrs: tuple[str, ...], missing_high: bool):
    """
    Build a timestamp key for sorting; missing values are pushed to the end.
    """
    value = _value_from_attrs(obj, attrs)
    dt_value = _coerce_datetime(value)
    if dt_value:
        return dt_value.timestamp()
    return float("inf") if missing_high else float("-inf")


def _title_key(obj: Any):
    """
    Build a lowercase title-like key for alpha sorts.
    """
    value = _value_from_attrs(obj, ("title", "name"))
    return str(value).lower() if value else ""


def search(request):
    """
    Searches pages across the entire site.

    Parameters:
    request (HttpRequest): The HTTP request object containing GET parameters for the search.

    Returns:
    HttpResponse: The rendered search results page.
    """

    search_form = SearchForm(request.GET)
    results: list = []
    results_paginated = []
    indexed_models = []
    results_by_model: OrderedDict[str, dict] = OrderedDict()
    active_search_model = None
    sort_option = ""

    if search_form.is_valid():
        current_locale = _get_request_locale(request)
        search_query = search_form.cleaned_data["s"]
        search_model = search_form.cleaned_data["t"]
        sort_option = search_form.cleaned_data.get("sort", "")

        filterable_models = {}
        legacy_model_names = {}
        for model in apps.get_models():
            if (
                issubclass(model, index.Indexed)
                and hasattr(model, "search_filterable")
                and model.search_filterable
            ):
                indexed_models.append(model)
                identifier = _model_identifier(model)
                filterable_models[identifier] = model
                legacy_model_names.setdefault(model._meta.model_name, model)

        model_result_sets = []

        selected_model = None
        if search_model:
            selected_model = filterable_models.get(search_model)
            if not selected_model:
                legacy_model = legacy_model_names.get(search_model)
                if legacy_model:
                    selected_model = legacy_model
                    search_model = _model_identifier(legacy_model)

        if selected_model:
            active_search_model = _model_identifier(selected_model)
            model_results = search_model_backend(
                selected_model, search_query, current_locale
            )
            count = model_results.count()
            results_by_model[active_search_model] = {
                "model": selected_model,
                "count": count,
            }
            model_result_sets.append((active_search_model, model_results, count))
        else:
            for model in indexed_models:
                identifier = _model_identifier(model)
                model_results = search_model_backend(
                    model, search_query, current_locale
                )
                count = model_results.count()
                results_by_model[identifier] = {
                    "model": model,
                    "count": count,
                }
                model_result_sets.append((identifier, model_results, count))

        merged_results = []
        for _, model_results, _ in model_result_sets:
            merged_results.extend(model_results)

        if merged_results:
            sort_handlers = {
                "updated_desc": (
                    lambda obj: _timestamp_key(obj, UPDATED_FIELD_NAMES, False),
                    True,
                ),
                "updated_asc": (
                    lambda obj: _timestamp_key(obj, UPDATED_FIELD_NAMES, True),
                    False,
                ),
                "created_desc": (
                    lambda obj: _timestamp_key(obj, CREATED_FIELD_NAMES, False),
                    True,
                ),
                "created_asc": (
                    lambda obj: _timestamp_key(obj, CREATED_FIELD_NAMES, True),
                    False,
                ),
                "title_asc": (_title_key, False),
                "title_desc": (_title_key, True),
            }

            if sort_option in sort_handlers:
                key_func, reverse = sort_handlers[sort_option]
                merged_results = sorted(merged_results, key=key_func, reverse=reverse)

            per_page = GeneralSettings.for_request(request).search_num_results
            paginator = Paginator(merged_results, per_page)
            page_number = request.GET.get("p", 1)
            try:
                results_paginated = paginator.page(page_number)
            except PageNotAnInteger:
                results_paginated = paginator.page(1)
            except EmptyPage:
                results_paginated = paginator.page(paginator.num_pages)
            except InvalidPage:
                results_paginated = paginator.page(paginator.num_pages)

        results = merged_results

    context = {
        "request": request,
        "form": search_form,
        "results": results,
        "pagetypes": indexed_models,
        "results_paginated": results_paginated,
        "results_by_model": results_by_model,
        "active_search_model": active_search_model,
        "sort_option": sort_option if search_form.is_valid() else "",
    }
    # Render template
    return render(
        request,
        "cjkcms/pages/search.html",
        context,
    )


def favicon(request):
    if icon := LayoutSettings.for_request(request).favicon:
        return HttpResponsePermanentRedirect(icon.get_rendition("original").url)
    raise Http404()


def robots(request):
    return render(request, "cjkcms/robots.txt", content_type="text/plain")
