from collections import OrderedDict

from django.apps import apps
from django.core.paginator import EmptyPage, InvalidPage, PageNotAnInteger, Paginator
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import render
from wagtail.models import Page
from wagtail.search import index
from wagtail.search.backends import get_search_backend

from cjkcms.forms import SearchForm
from cjkcms.models import (
    GeneralSettings,
    LayoutSettings,
)

from wagtail.models import Locale


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
        return backend.search(
            search_query,
            model.objects.live().public().filter(locale=current_locale),
        )
    else:
        # Search normally for non-page models
        return backend.search(search_query, model)


def _model_identifier(model):
    return f"{model._meta.app_label}.{model._meta.model_name}"


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

    if search_form.is_valid():
        current_locale = Locale.get_active()
        search_query = search_form.cleaned_data["s"]
        search_model = search_form.cleaned_data["t"]

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

        total_results = sum(count for _, _, count in model_result_sets)
        if total_results:
            per_page = GeneralSettings.for_request(request).search_num_results
            paginator = Paginator(range(total_results), per_page)
            page_number = request.GET.get("p", 1)
            try:
                page = paginator.page(page_number)
            except PageNotAnInteger:
                page = paginator.page(1)
            except EmptyPage:
                page = paginator.page(paginator.num_pages)
            except InvalidPage:
                page = paginator.page(paginator.num_pages)

            start_index = page.start_index() - 1
            end_index = page.end_index()
            needed = end_index - start_index
            page_results = []
            offset = 0

            for _, model_results, count in model_result_sets:
                if start_index >= offset + count:
                    offset += count
                    continue
                local_start = max(0, start_index - offset)
                remaining = needed - len(page_results)
                local_end = min(count, local_start + remaining)
                if local_start < local_end:
                    page_results.extend(model_results[local_start:local_end])
                offset += count
                if len(page_results) >= needed:
                    break

            page.object_list = page_results
            results_paginated = page
            results = page_results

    context = {
        "request": request,
        "form": search_form,
        "results": results,
        "pagetypes": indexed_models,
        "results_paginated": results_paginated,
        "results_by_model": results_by_model,
        "active_search_model": active_search_model,
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
