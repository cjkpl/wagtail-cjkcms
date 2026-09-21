# mixins.py
from django.conf import settings
from django.contrib.admin.utils import label_for_field
from django.utils.functional import cached_property
from wagtail.admin.widgets.button import HeaderButton
from wagtail.snippets.views.snippets import IndexView as SnippetIndexView


class RecordsPerPageMixin:
    """Adds per-page selection support and exposes list-setup context values."""

    session_key = "wagtail_admin_records_per_page"

    def get_per_page_session_key(self):
        return self.session_key

    def get_allowed_per_page_values(self):
        return getattr(
            settings,
            "WAGTAIL_ADMIN_PER_PAGE_OPTIONS",
            [10, 20, 50, 100, 120],
        )

    def get_default_per_page(self):
        return getattr(
            settings,
            "WAGTAIL_ADMIN_DEFAULT_PER_PAGE",
            20,
        )

    def get_paginate_by(self, queryset):
        allowed_values = self.get_allowed_per_page_values()
        default_value = self.get_default_per_page()
        session_key = self.get_per_page_session_key()

        value = self.request.GET.get("per_page")

        if value is not None:
            try:
                value = int(value)
            except ValueError:
                value = default_value

            if value in allowed_values:
                self.request.session[session_key] = value
                return value

        return self.request.session.get(session_key, default_value)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["per_page_options"] = self.get_allowed_per_page_values()
        context["current_per_page"] = self.get_paginate_by(self.get_queryset())
        context["default_per_page"] = self.get_default_per_page()
        if hasattr(self, "_all_list_display"):
            context["all_list_display"] = self._all_list_display
            selected = self._get_selected_columns()
            context["selected_list_display"] = selected
            hidden = [col for col in self._all_list_display if col not in selected]
            ordered_for_modal = [*selected, *hidden]
            context["all_list_display_choices"] = [
                {
                    "name": column,
                    "label": self._get_column_label(column),
                }
                for column in ordered_for_modal
            ]

        return context

    def _get_column_label(self, column_name):
        try:
            label = label_for_field(column_name, self.model)
        except Exception:
            label = column_name.replace("_", " ")
        return str(label)


class RecordsPerPageSnippetIndexView(RecordsPerPageMixin, SnippetIndexView):
    """Snippet index view with per-model column visibility and list setup button."""

    template_name = "wagtailsnippets/snippets/list_with_setup.html"
    columns_session_prefix = "wagtail_admin_visible_columns"
    per_page_session_prefix = "wagtail_admin_records_per_page"

    def _model_key(self):
        return f"{self.model._meta.app_label}.{self.model._meta.model_name}"

    def get_per_page_session_key(self):
        return f"{self.per_page_session_prefix}:{self._model_key()}"

    def get_columns_session_key(self):
        return f"{self.columns_session_prefix}:{self._model_key()}"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self._all_list_display = [
            column for column in list(self.list_display) if isinstance(column, str)
        ]
        self._apply_selected_columns()

    def _sanitize_columns(self, columns):
        if not columns:
            return []
        allowed = set(self._all_list_display)
        selected = []
        seen = set()
        for column in columns:
            if column in allowed and column not in seen:
                selected.append(column)
                seen.add(column)
        return selected

    def _get_selected_columns(self):
        session_key = self.get_columns_session_key()
        value = self.request.GET.get("cols")

        if value is not None:
            requested = [item.strip() for item in value.split(",") if item.strip()]
            selected = self._sanitize_columns(requested)
            if selected:
                self.request.session[session_key] = selected
                return selected
            self.request.session.pop(session_key, None)
            return self._all_list_display

        stored = self.request.session.get(session_key, self._all_list_display)
        selected = self._sanitize_columns(stored)
        return selected or self._all_list_display

    def _apply_selected_columns(self):
        self.list_display = self._get_selected_columns()

    @cached_property
    def header_buttons(self):
        buttons = list(super().header_buttons)
        buttons.append(
            HeaderButton(
                "List setup",
                url="#",
                icon_name="cogs",
                attrs={"id": "list-setup-open", "aria-label": "Open list setup"},
                priority=20,
            )
        )
        return buttons
