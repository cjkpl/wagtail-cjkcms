# Quick start guide

## Quick install

Note: See helper scripts ```boot_django.py``` and ```boot_urls.py``` in the Github repository for a preview of how the setup can be configured.

* (optional) If you are staring a new project, install Django 4.x, Wagtail 3.x, and start a new Wagtail project.
* Install the CjkCMS:
```
pip install django-cjkcms
```

## Note for version 0.2.1

Until Codered's packages wagtail-seo and wagtail-cache are updated for compatibility with Wagtail 4, the cjkcms switches to forked versions of these packages. You will need to install them manually with:
```
pip install git+https://github.com/cjkpl/wagtail-cache.git
pip install git+https://github.com/cjkpl/wagtail-seo.git
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


> * [outdated begin - these models are automatically added as of version 0.2.2] 
> Add concrete models: WebPage, ArticlePage, and ArticleIndexPage to your project, anywhere you want, e.g. in ```/home/models.py```.  [end]

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