# Manual installation details

## Project folder
The first step when setting up a new project is to create a folder for the project. We will call our project `cmsdemo`

```
mkdir cmsdemo
cd cmsdemo
```
We will assume that we are in user's home folder /home/, for the purpose of illustration, as later on we will have three nested folders with the same name, and it may get confusing!

The resulting folder structure should be: `/home/cmsdemo/`


## Virtual environment
It is strongly recommended to use a virtual environment for the development of your project.
Typical steps for creating a virtual environment are listed below.

!!! note
    There are two typical approaches to naming a virtual environment:

    * always the same name, e.g.: `venv`
    * a name that is different for each project, e.g.: `env-cmsdemo`
    
    We use the second approach, so that when you activate the virtual environment, you can see its' name in the terminal, and it is harder to confuse it with other virtual environments.

```
python3 -m venv ./env-cmsdemo/
source ./env-cmsdemo/bin/activate
```
or on Windows:
```
python -m venv env-cmsdemo
source env-cmsdemo/Scripts/activate
```

## Install wagtail-cjkcms
```
pip install wagtail-cjkcms
```
This will install all required dependencies into the virtual environment, including Wagtail and Django.

## Quick install
If you are starting from scratch, you can use the quick install below. If you already have a project, you can follow the manual install steps below to add CjkCMS as a new app into your Wagtail project. See [quick start](quick-start.md) for more details. Otherwise follow the steps below.

## Start new Wagtail project
With all required packages installed, you can start a new Wagtail project. We will name it `cmsdemo`, like the parent folder.
```
wagtail start cmsdemo
cd cmsdemo
```
Remember to change change directory to the newly created folder. You should be in the folder: `/home/cmsdemo/cmsdemo/`. Inside you will see several files : `Dockerfile, manage.py, requirements.txt` and folders `cmsdemo, home, search`.

!!! note
    If you want to switch from the default SQLite database to PostgreSQL, now is the time to do so.

## Migrate & add an admin
Run required migrations and create a superuser:
```
python manage.py migrate
python manage.py createsuperuser
```

## Start the dev server
Start the development server and make sure you can see the default Wagtail page:
```
python manage.py runserver
```
This lets you make sure that the default Wagtail setup worked. CMS will be activated in the next step.


* Add CjkCMS and its requirements to ```INSTALLED_APPS``` in your project configuration (e.g. ```base.py```):
```python
INSTALLED_APPS = [
    ...
    ### wagtail-cjkcms ###
    "cjkcms",
    ### wagtail-cjkcms requirements ###
    "wagtailseo",
    "wagtailcache",
    "wagtail.contrib.table_block",
    "wagtail.contrib.settings",
    "wagtail.contrib.modeladmin",
    "django_bootstrap5",
    "wagtail.contrib.sitemaps",
    "django.contrib.sitemaps",
    ### end wagtail-cjkcms ###
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


## Changing the homepage: 
By default, Wagtail adds a homepage inherited from Page. If you want to use CjkCMS WebPage as your homepage, you need to change the homepage to `WebPage`. Otherwise you can start adding new CjkCMS pages to your project anywhere in the page tree.

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


## Summary and next steps

At this stage you should be able to log in to the Wagtail admin interface. Visit `localhost:8000/admin/` and you should see the login page.

After you log in using the superuser credentials, you should see the admin panel with CMS-specific additions:
* `Navigation Bars` in the side menu
* Additional menu items in `Settings`: `Social Media`, `Layout`, `Tracking`, `General`, `Mailchimp API`, `Adobe API`, `SEO`