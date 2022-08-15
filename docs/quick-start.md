# Quick start guide

## Quick install

Note: See helper scripts ```boot_django.py``` and ```boot_urls.py``` in the Github repository for a preview of how the setup can be configured.

* (optional) If you are staring a new project, install Django 4.x, Wagtail 3.x, and start a new Wagtail project.
* Install the CjkCMS:
```
pip install django-cjkcms
```

* Add CjkCMS and its requirements to ```INSTALLED_APPS``` in your project configuration (e.g. ```base.py```):
```python
INSTALLED_APPS = [
    ...
    ### django-cjkcms ###
    "cjkcms",
    ### django-cjkcms requirements ###
    "wagtailseo",
    "wagtailcache",
    "wagtail.contrib.table_block",
    "wagtail.contrib.settings",
    "wagtail.contrib.modeladmin",
    "django_bootstrap5",
    "wagtail.contrib.sitemaps",
    "django.contrib.sitemaps",
    ### end django-cjkcms ###
```
* Run migrations:
```
python manage.py migrate
```
* Add ```cjkcms.urls``` to ```urls.py``` in your project:
```python
from cjkcms import urls as cjkcms_urls

urlpatterns = [
    ...
    # add cjkcms urls
    path("", include(cjkcms_urls)),

    # comment out the default wagtail search view,
    # it will be replaced by the cjkcms search view
    # path("search/", search_views.search, name="search"),
    ...
]
```

## Optional setup steps

Out of the box, CjkCMS can provide your project with generic, reusable pages:
`ArticleIndex`, `Article`, `WebPage` which you can use in your project, or extend with additional functionality. CjkCMS pages provide you with a generic "body" section and, using ```wagtail-seo``` package, a basic SEO functionality.

* Add concrete models: WebPage, ArticlePage, and ArticleIndexPage to your project, anywhere you want, e.g. 
in ```/home/models.py```. This will make the new page types visible in the admin panel. 
This step will provide you with a quick-start to put content into your new website in the admin panel, without further coding. If you skip this step, you need to create your own custom page types and models. You may use the three models in cjkcms.models.cms_models as a starting point. 
```python
# e.g. home/models.py
from cjkcms.models.cms_models import ArticleIndexPage, ArticlePage, WebPage
```

## Migrating the homepage: 

By default, Wagtail adds a homepage inherited from Page. 

### Change to WebPage model:

If you are starting a new website, you may want to replace it with CjkCMS WebPage, for the additional functionality provided by CjkCMS. 

To do this, you need to:
- log in to the wagtail admin
- go to Pages
- add a new page (any CjkCMS page type, e.g. most generic WebPage) at the top level, next to the Homepage
- go to Settings -> Sites and change the root page of your site to the new CMS page
- go back to pages, if there is no custom content in the default (old) homepage, you can delete it.

### Old Homepage cleanup

You cannot remove the HomePage model from home/models.py - first you need to delete that page in the admin panel - see section above. A safer solution is to keep the HomePage model, bug deactivate it by adding `max_count = 0` to the Homepage model, which effectively hides it from admin interface.

In `/home/models.py` change this:

```
class HomePage(Page):
    pass
```

to that:

```
class HomePage(Page):
    max_count = 0
```