# Generated by Django 5.0.2 on 2024-02-18 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cjkcms', '0018_layoutsettings_search_format'),
    ]

    operations = [
        migrations.AddField(
            model_name='layoutsettings',
            name='searchbox_input_class',
            field=models.CharField(blank=True, default='border-secondary mb-0', help_text='Classes applied to searchbox input', max_length=255, verbose_name='Searchbox input class'),
        ),
        migrations.AddField(
            model_name='layoutsettings',
            name='searchbutton_class',
            field=models.CharField(blank=True, default='btn btn-outline-secondary', help_text='Classes applied to search button. Add e.g. `fas fa-search` for icon.', max_length=255, verbose_name='Search button (with text) class'),
        ),
        migrations.AddField(
            model_name='layoutsettings',
            name='searchbutton_label',
            field=models.CharField(blank=True, default='Search', help_text='Leave empty when using icon-only button. Otherwise, add button label.', max_length=255, verbose_name='Search button label'),
        ),
    ]
