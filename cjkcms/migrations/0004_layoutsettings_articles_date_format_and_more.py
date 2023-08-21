# Generated by Django 4.1.3 on 2022-11-27 18:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cjkcms", "0003_alter_footer_content_alter_navbar_menu_items"),
    ]

    operations = [
        migrations.AddField(
            model_name="layoutsettings",
            name="articles_date_format",
            field=models.CharField(
                blank=True,
                default="Y-m-d",
                help_text="Format of the publication date in articles. Set blank to hide.",
                max_length=200,
                verbose_name="Date format in articles",
            ),
        ),
        migrations.AddField(
            model_name="layoutsettings",
            name="articles_show_author",
            field=models.BooleanField(
                default=True,
                help_text="If disabled, override by filling `display author as` in article",
                verbose_name="Show author in articles",
            ),
        ),
    ]
