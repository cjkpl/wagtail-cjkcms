# -*- coding: utf-8 -*-
from django.db import migrations
from wagtail.models import Locale


def create_homepage(apps, schema_editor):
    """Create ISoNTech homepage based on CjkCMS WebPage model"""
    # Get models
    ContentType = apps.get_model("contenttypes.ContentType")
    Page = apps.get_model("wagtailcore.Page")
    Site = apps.get_model("wagtailcore.Site")
    IsontechWebPage = apps.get_model("home.IsontechWebPage")

    # Delete the default homepage
    # If migration is run multiple times, it may have already been deleted
    Page.objects.filter(slug="home").delete()

    # Create content type for homepage model
    isontech_webpage_content_type, __ = ContentType.objects.get_or_create(
        model="isontechwebpage", app_label="home"
    )

    # Create a new homepage
    homepage = IsontechWebPage.objects.create(
        title="ISonTech Home",
        draft_title="ISoNTech Home",
        slug="home",
        content_type=isontech_webpage_content_type,
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
    ContentType = apps.get_model("contenttypes.ContentType")
    IsontechWebPage = apps.get_model("home.IsontechWebPage")

    # Delete the default homepage
    # Page and Site objects CASCADE
    IsontechWebPage.objects.filter(slug="home", depth=2).delete()

    # Delete content type for isontech webpage model
    ContentType.objects.filter(model="isontechwebpage", app_label="home").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("cjkcms", "0001_initial"),
        ("wagtailcore", "0057_page_locale_fields_notnull"),
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_homepage, remove_homepage),
    ]
