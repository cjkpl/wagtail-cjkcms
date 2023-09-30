# Generated by Django 4.2.5 on 2023-09-30 21:11

import cjkcms.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cjkcms", "0014_navbar_alignment"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventCalendar",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Name")),
                (
                    "custom_css_class",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Custom CSS Class"
                    ),
                ),
                (
                    "custom_id",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Custom ID"
                    ),
                ),
                (
                    "events",
                    cjkcms.fields.CjkcmsStreamField(
                        use_json_field=True, verbose_name="Events"
                    ),
                ),
            ],
            options={
                "verbose_name": "Event calendar",
            },
        ),
    ]
