import re
from typing import Final
from urllib.parse import unquote_plus

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


SQL_INJECTION_SEARCH_PATTERNS: Final[tuple[re.Pattern[str], ...]] = (
    re.compile(
        r"\bwaitfor\b\s+\bdelay\b\s+['\"]?\d{1,2}:\d{1,2}:\d{1,2}",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:pg_sleep|sleep|benchmark)\s*\(",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bor\b.*\d+\s*=\s*\(\s*select\b.*\bfrom\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bunion\b(?:\s+\ball\b)?\s+\bselect\b",
        re.IGNORECASE,
    ),
)


def normalize_search_query_for_validation(value: str) -> str:
    normalized = value
    for _decode_attempt in range(2):
        decoded = unquote_plus(normalized)
        if decoded == normalized:
            break
        normalized = decoded
    return normalized


def is_suspicious_search_query(value: str) -> bool:
    normalized = normalize_search_query_for_validation(value)
    return any(pattern.search(normalized) for pattern in SQL_INJECTION_SEARCH_PATTERNS)


class SearchForm(forms.Form):
    SORT_CHOICES = (
        ("", _("Relevance")),
        ("updated_desc", _("Last Updated (Newest)")),
        ("updated_asc", _("Last Updated (Oldest)")),
        ("created_desc", _("Created (Newest)")),
        ("created_asc", _("Created (Oldest)")),
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

    def clean_s(self) -> str:
        search_query = self.cleaned_data["s"].strip()
        if search_query and is_suspicious_search_query(search_query):
            raise ValidationError(
                _("Please Enter Valid Search Query"),
                code="invalid_search_query",
            )
        return search_query
