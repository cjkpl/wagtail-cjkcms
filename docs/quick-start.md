# Quick start guide

If you are starting froms cratch, you can use the quick install below. If you already have a project, you can follow the manual install steps below to add CjkCMS as a new app into your Wagtail project.

## Quick install of the CjkCMS, Django and Wagtail

* CjkCMS requires Django==4.x and Wagtail>=4.2.

Install the CjkCMS:
```
pip install wagtail-cjkcms
```
Create a new project. Use lowercase name of the project:
```
cjkcms start myproject
```
You should see the following output:
```
Creating a CjkCMS project called myproject
Success! myproject has been created

Next steps:
    1. cd myproject/
    2. python manage.py migrate
    3. python manage.py createsuperuser
    4. python manage.py runserver
    5. Go to http://localhost:8000/backend/ and start editing!
```
---

## Manual install
If you already have a Wagtail project, follow the [manual install](installation.md) steps to add CjkCMS as a new app.
