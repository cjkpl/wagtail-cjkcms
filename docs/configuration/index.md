# Configuration of wagtail-cjkcms

## Settings

### Layout settings

#### Breadcrumbs

CjkCMS provides breadcrumbs for pages. You can enable them by activating a checkbox in:
```Settings -> Layout -> Breadcrumbs```

You can use any svg file as a separator. Built in icons are (bootstrap icons):
* chevron-right
* caret-right
* caret-right-fill
* slash

### Limiting access to Django settings in templates

Editors can reference a small, whitelisted subset of Django settings through the
`django_settings` template filter. By default only `DEBUG` and `TIME_ZONE` are
available to templates. To expose additional settings (for example a custom
flag used in your theme), set `CJKCMS_DJANGO_SETTINGS_WHITELIST` in your Django
project:

```python
# settings.py
CJKCMS_DJANGO_SETTINGS_WHITELIST = ["DEBUG", "TIME_ZONE", "MY_CUSTOM_FLAG"]
```

Any lookup that is not present in this list will raise a template error, which
helps catch unauthorized access to sensitive settings early.

### Limiting the number of search results

The search page loads the matching objects of every searchable model before
sorting and paginating them. To keep a very broad query from exhausting memory,
at most `CJKCMS_SEARCH_MAX_RESULTS` results are loaded per model (1000 by
default). The result counts shown next to each model still report every match.

```python
# settings.py
CJKCMS_SEARCH_MAX_RESULTS = 200   # or None to load every match
```

When a sort order other than relevance is chosen, it is applied to the most
relevant results within this limit.
