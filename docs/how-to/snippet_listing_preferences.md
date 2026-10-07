# Personal snippet display options

CjkCMS snippet listings include a **Display options** cog beside the header
controls. Editors can hide optional columns, select 10, 20, 50, or 100 rows per
page, and reset the listing to its defaults. Preferences belong to the signed-in
user and listing and persist across browsers. They do not change other users'
views or permissions. The title/edit link and action columns remain visible.

Choosing **Default** uses the viewset's `list_per_page`. Wagtail's drag-and-drop
reordering mode continues to show all entries. Applying options retains search,
filters, and ordering and returns to the first page. Hidden columns remain
available for sorting and exports; this feature controls presentation, not access.

## Deployment and storage

Run `python manage.py migrate` and `python manage.py collectstatic` when deploying
this release, then restart the application. No project user-model changes are
required. CjkCMS owns an `AdminListingPreference` table with a foreign key to
`settings.AUTH_USER_MODEL`, a unique user/listing key, hidden column identifiers,
and an optional page size. It does not modify Wagtail's user profile or a site's
custom profile. Rows are created only when an editor applies preferences and are
deleted when the user is deleted or the listing is reset.

The key combines the model's `app_label.model_name` with the listing's URL name.
Changing either starts a new set of defaults. Column identifiers are Wagtail
`Column.name` values, not translated labels or column positions. Newly added
columns appear by default; removed identifiers are ignored. Unsupported stored
page sizes fall back to the viewset default.

## Project snippets

All eight CMS-owned snippets are enabled automatically. Project and third-party
snippets keep their existing registrations until explicitly adopted. For a new
or standard project viewset:

```python
# project/wagtail_hooks.py
from wagtail.snippets.models import register_snippet

from cjkcms.admin_viewsets import CjkcmsSnippetViewSet
from .models import Product


class ProductViewSet(CjkcmsSnippetViewSet):
    model = Product
    list_display = ["name", "sku", "price"]
    list_per_page = 20
    search_fields = ["name", "sku"]


register_snippet(ProductViewSet)
```

Replace the existing registration; do not register a model twice. In particular,
remove an existing `@register_snippet` decorator when registering its viewset.
Only columns explicitly exposed by the viewset are offered in the chooser.

## Existing customized listings

To retain a project's custom index view, put `ListingPreferencesMixin` before
that view's existing superclass:

```python
from cjkcms.admin_viewsets import CjkcmsSnippetViewSet, ListingPreferencesMixin


class ProductIndexView(ListingPreferencesMixin, ExistingProductIndexView):
    listing_page_sizes = (10, 20, 50, 100)
    listing_required_columns = ("sku",)


class ProductViewSet(CjkcmsSnippetViewSet):
    model = Product
    index_view_class = ProductIndexView
```

Keep the project's other viewset options and overrides. If its viewset already
has a custom superclass, retain that superclass and set `index_view_class` as
above plus `index_template_name = "cjkcms/admin/snippets/index.html"`.
Overrides of `get_table`, `get_paginate_by`, and `get_context_data` should call
`super()`. A custom `post` handler needs to delegate display-option submissions
to the mixin; its default POST handler is reserved for these options.

For a custom index template, extend `cjkcms/admin/snippets/index.html`, or include
`cjkcms/admin/listing_preferences.html` in your header and load
`cjkcms/css/listing-preferences.css` and `cjkcms/js/listing-preferences.js`.
The JavaScript preserves the current search/filter query after AJAX updates and
provides Escape/click-away dismissal. The form also works without JavaScript,
using the query from its initial page render.

The reusable mixin may also be used with Wagtail model listing views that expose
the same table, pagination, URL, and permission-policy interfaces. It does not
alter chooser dialogs, page explorer listings, or unrelated third-party views.
