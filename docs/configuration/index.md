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

### Integrity of theme files loaded from a CDN

The built-in themes load Bootstrap, MDB, Bootswatch and Font Awesome from public
CDNs. Each of these files is listed in `CJKCMS_ASSET_INTEGRITY` with its
[Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)
hash, so the browser refuses a file which was altered on the CDN.

Files are matched by their full URL. If you point a theme to a different file
through `CJKCMS_THEME_FILES`, it is loaded without a check unless you add its hash:

```python
# settings.py
from cjkcms.settings import _DefaultSettings

CJKCMS_ASSET_INTEGRITY = {
    **_DefaultSettings.CJKCMS_ASSET_INTEGRITY,  # keep the built-in hashes
    "https://cdn.example.com/my-theme.min.css": "sha384-...",
}
```

Set `CJKCMS_ASSET_INTEGRITY = {}` to switch the checks off.
