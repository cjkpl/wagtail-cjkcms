from django import forms
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.admin.ui.tables import (
    BulkActionsCheckboxColumn,
    ButtonsColumnMixin,
    TitleColumn,
)
from wagtail.snippets.views.snippets import IndexView, SnippetViewSet

from cjkcms.models.admin_preferences import AdminListingPreference


class ListingPreferencesForm(forms.Form):
    visible_columns = forms.MultipleChoiceField(
        label=_("Columns"), required=False, widget=forms.CheckboxSelectMultiple
    )
    page_size = forms.TypedChoiceField(
        label=_("Rows per page"), required=False, coerce=int, empty_value=None
    )

    def __init__(self, *args, columns, page_sizes, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["visible_columns"].choices = columns
        self.fields["page_size"].choices = [("", _("Default"))] + [
            (size, str(size)) for size in page_sizes
        ]


class ListingPreferencesMixin:
    """Add personal display options to a Wagtail model listing view.

    Place before the existing IndexView superclass. Custom listing templates
    should include the display-options header and assets (see documentation).
    """

    listing_page_sizes = (10, 20, 50, 100)
    listing_required_columns = ()

    @cached_property
    def listing_preference_key(self):
        return f"{self.model._meta.label_lower}:{self.index_url_name}"

    @cached_property
    def listing_preference(self):
        if not self.request.user.is_authenticated:
            return None
        return AdminListingPreference.objects.filter(
            user=self.request.user, listing_key=self.listing_preference_key
        ).first()

    @cached_property
    def configurable_columns(self):
        columns = list(self.columns)
        # Keep the first content column even if a project uses a custom class.
        primary = next(
            (
                column.name
                for column in columns
                if not isinstance(column, BulkActionsCheckboxColumn)
            ),
            None,
        )
        return [
            column
            for column in columns
            if column.name != primary
            and column.name not in self.listing_required_columns
            and not isinstance(column, (BulkActionsCheckboxColumn, TitleColumn, ButtonsColumnMixin))
        ]

    @cached_property
    def hidden_listing_columns(self):
        stored = self.listing_preference.hidden_columns if self.listing_preference else []
        if not isinstance(stored, list):
            return set()
        return {column.name for column in self.configurable_columns if column.name in stored}

    def get_table(self, object_list):
        table = super().get_table(object_list)
        # Table owns its columns dictionary. Leave the view's complete columns
        # intact for ordering, queryset annotations, and exports.
        for name in self.hidden_listing_columns:
            table.columns.pop(name, None)
        return table

    def get_paginate_by(self, queryset):
        default = super().get_paginate_by(queryset)
        if default is None:  # Preserve Wagtail's drag-and-drop reordering mode.
            return None
        preference = self.listing_preference
        if preference and preference.page_size in self.listing_page_sizes:
            return preference.page_size
        return default

    def get_listing_preferences_form(self, data=None):
        preference = self.listing_preference
        return ListingPreferencesForm(
            data=data,
            columns=[(column.name, column.label) for column in self.configurable_columns],
            page_sizes=self.listing_page_sizes,
            initial={
                "visible_columns": [
                    column.name
                    for column in self.configurable_columns
                    if column.name not in self.hidden_listing_columns
                ],
                "page_size": preference.page_size
                if preference and preference.page_size in self.listing_page_sizes
                else None,
            },
        )

    def get_listing_preferences_url(self):
        query = self.request.GET.copy()
        query.pop(self.page_kwarg, None)
        query.pop("export", None)
        return self.index_url + (f"?{query.urlencode()}" if query else "")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["listing_preferences_form"] = self.get_listing_preferences_form()
        context["listing_preferences_url"] = self.get_listing_preferences_url()
        return context

    def post(self, request, *args, **kwargs):
        # Normal IndexView dispatch still enforces the model's permission policy.
        # Never take a user ID or listing identifier from the submitted data.
        if not request.user.is_authenticated:
            raise PermissionDenied
        if self.results_only:
            return HttpResponseBadRequest("Use the listing URL to save display options.")
        lookup = {"user": request.user, "listing_key": self.listing_preference_key}
        action = request.POST.get("listing_preferences_action")
        if action == "reset":
            AdminListingPreference.objects.filter(**lookup).delete()
        elif action == "apply":
            form = self.get_listing_preferences_form(request.POST)
            if not form.is_valid():
                return HttpResponseBadRequest(
                    form.errors.as_json(), content_type="application/json"
                )
            visible = set(form.cleaned_data["visible_columns"])
            AdminListingPreference.objects.update_or_create(
                **lookup,
                defaults={
                    "hidden_columns": [
                        column.name
                        for column in self.configurable_columns
                        if column.name not in visible
                    ],
                    "page_size": form.cleaned_data["page_size"],
                },
            )
        else:
            return HttpResponseBadRequest("Unknown display options action.")
        return HttpResponseRedirect(self.get_listing_preferences_url())


class CjkcmsSnippetIndexView(ListingPreferencesMixin, IndexView):
    pass


class CjkcmsSnippetViewSet(SnippetViewSet):
    index_view_class = CjkcmsSnippetIndexView
    index_template_name = "cjkcms/admin/snippets/index.html"
