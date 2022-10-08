# Installation details

## Project folder
The first step when setting up a new project is to create a folder for the project. We will call our project `cmsdemo`

```
mkdir cmsdemo
cd cmsdemo
```
We will assume that we are in the home folder /home/, for the purpose of illustration, as later on we will have three nested folders with the same name, and it may get confusing!

The resulting folder structure should be: `/home/cmsdemo/`


## Virtual environment
It is strongly recommended to use a virtual environment for the development of your project.
Typical steps for creating a virtual environment are listed below.

!!! note
    There are two typical approaches to naming a virtual environment:

    * always the same name, e.g.: `venv`
    * a name that is different for each project, e.g.: `env-cmsdemo`
    
    We recommend the second approach, so that when you activate the virtual environment, you can see its' name in the terminal, and it is harder to confuse it with other virtual environments.

```
python3 -m venv ./env-cmsdemo/
source ./env-cmsdemo/bin/activate
```
or on Windows:
```
python -m venv env-cmsdemo
source env-cmsdemo/Scripts/activate
```

## Install django-cjkcms
```
pip install django-cjkcms
```
This will install all required dependencies into the virtual environment, including Wagtail and Django.

## Note for version 0.2.1

Until Codered's packages wagtail-seo and wagtail-cache are updated for compatibility with Wagtail 4, the cjkcms switches to forked versions of these packages. You will need to install them manually with:
```
pip install git+https://github.com/cjkpl/wagtail-cache.git
pip install git+https://github.com/cjkpl/wagtail-seo.git
```

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

## Activate CMS: update project config
* Add CjkCMS and its requirements to ```INSTALLED_APPS``` in your project configuration
(/home/cmsdemo/cmsdemo/cmsdemo/settings/base.py)).
!!! note
    Yes, there are three nested folders named `cmsdemo`: your main project folder, and inside two folders created by Wagtail.

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

Restart the development server, if it is not running. You should see a message like this:
```
You have 4 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): cjkcms, wagtailseo.
Run 'python manage.py migrate' to apply them.
```

Proceed as per message above. Stop the server, execute the `migrate` command, and restart the server.

## Add utility URLs provided by CjkCMS

* Add cjkcms-specific urls, which provide SEO-related pages: favicon.ico, robots.txt, sitemap.xml.
* Replace default wagtail `search` with cjkcms-specific search: comment out the `search` view.

```python
# in the main urls.py in your project:
from cjkcms import urls as cjkcms_urls

urlpatterns = [
    ...
    # replace wagtail search with cjkcms version (comment out line below)
    # path('search/', search_views.search, name='search'),

    # and add cjkcms urls
    path('', include(cjkcms_urls)),
    ...
]
```

## Summary and next steps

At this stage you should be able to log in to the Wagtail admin interface. Visit `localhost:8000/admin/` and you should see the login page.

After you log in using the superuser credentials, you should see the admin panel with CMS-specific additions:
* `Navigation Bars` in the side menu
* Additional menu items in `Settings`: `Social Media`, `Layout`, `Tracking`, `General`, `Mailchimp API`, `Adobe API`, `SEO`