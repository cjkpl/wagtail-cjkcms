# -*- coding: utf-8 -*-
from django.db import migrations
from wagtail.models import Locale


def create_homepage(apps, schema_editor):
    """Create app homepage based on CjkCMS WebPage model"""
    # Get models
    ContentType = apps.get_model("contenttypes.ContentType")
    Page = apps.get_model("wagtailcore.Page")
    Site = apps.get_model("wagtailcore.Site")
    ProjectWebPage = apps.get_model("testapp.ProjectWebPage")

    # Delete the default homepage
    # If migration is run multiple times, it may have already been deleted
    Page.objects.filter(slug="home").delete()

    # Create content type for homepage model
    project_webpage_content_type, __ = ContentType.objects.get_or_create(
        model="projectwebpage", app_label="testapp"
    )

    # Create a new homepage
    homepage = ProjectWebPage.objects.create(
        title="app Home",
        draft_title="app Home",
        slug="home",
        content_type=project_webpage_content_type,
        path="00010001",
        depth=2,
        numchild=0,
        url_path="/home/",
        locale_id=Locale.get_default().id,
    )

    # Create a site with the new homepage set as the root
    Site.objects.create(hostname="localhost", root_page=homepage, is_default_site=True)


def remove_homepage(apps, schema_editor):
    # Get models
    content_type = apps.get_model("contenttypes.ContentType")
    project_web_page = apps.get_model("testapp.ProjectWebPage")

    # Delete the default homepage
    # Page and Site objects CASCADE
    project_web_page.objects.filter(slug="home", depth=2).delete()

    # Delete content type for app webpage model
    content_type.objects.filter(model="projectwebpage", app_label="home").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("cjkcms", "0001_initial"),
        ("wagtailcore", "0057_page_locale_fields_notnull"),
        ("testapp", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_homepage, remove_homepage),
    ]
