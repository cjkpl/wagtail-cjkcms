from django import forms
from django.utils.translation import gettext_lazy as _


class SearchForm(forms.Form):
    SORT_CHOICES = (
        ("", _("Relevance")),
        ("updated_desc", _("Last updated (newest)")),
        ("updated_asc", _("Last updated (oldest)")),
        ("created_desc", _("Created (newest)")),
        ("created_asc", _("Created (oldest)")),
        ("title_asc", _("Title A to Z")),
        ("title_desc", _("Title Z to A")),
    )

    s = forms.CharField(
        max_length=255,
        required=False,
        label=_("Search"),
    )
    t = forms.CharField(
        widget=forms.HiddenInput,
        max_length=255,
        required=False,
        label=_("Page type"),
    )
    sort = forms.CharField(
        required=False,
        label=_("Sort by"),
        widget=forms.Select(choices=SORT_CHOICES),
    )
