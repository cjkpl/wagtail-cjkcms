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


# @login_required
# def import_index(request):
#     """
#     Landing page to replace wagtailimportexport.
#     """
#     return render(request, 'wagtailimportexport/index.html')


# @login_required
# def import_pages_from_csv_file(request):
#     """
#     Overwrite of the `import_pages` view from wagtailimportexport.  By default, the `import_pages`
#     view expects a json file to be uploaded.  This view converts the uploaded csv into the json
#     format that the importer expects.
#     """

#     if request.method == 'POST':
#         form = ImportPagesFromCSVFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             import_data = convert_csv_to_json(
#                 form.cleaned_data['file'].read().decode('utf-8').splitlines(),
#                 form.cleaned_data['page_type']
#             )
#             parent_page = form.cleaned_data['parent_page']
#             try:
#                 page_count = import_pages(import_data, parent_page)
#             except LookupError as e:
#                 messages.error(request, _(
#                     "Import failed: %(reason)s") % {'reason': e}
#                 )
#             else:
#                 messages.success(request, ngettext(
#                     "%(count)s page imported.",
#                     "%(count)s pages imported.",
#                     page_count) % {'count': page_count}
#                 )
#             return redirect('wagtailadmin_explore', parent_page.pk)
#     else:
#         form = ImportPagesFromCSVFileForm()

#     return render(request, 'wagtailimportexport/import_from_csv.html', {
#         'form': form,
#     })
