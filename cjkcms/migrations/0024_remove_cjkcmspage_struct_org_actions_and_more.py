# Generated by Django 5.1.5 on 2025-02-08 10:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cjkcms', '0023_alter_navbar_language'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cjkcmspage',
            name='struct_org_actions',
        ),
        migrations.RemoveField(
            model_name='cjkcmspage',
            name='struct_org_address_country',
        ),
        migrations.RemoveField(
            model_name='cjkcmspage',
            name='struct_org_address_locality',
        ),
        migrations.RemoveField(
            model_name='cjkcmspage',
            name='struct_org_address_postal',
        ),
        migrations.RemoveField(
            model_name='cjkcmspage',
            name='struct_org_address_region',
        ),
        migrations.RemoveField(
            model_name='cjkcmspage',
            name='struct_org_address_street',
        ),
        migrations.RemoveField(
            model_name='cjkcmspage',
            name='struct_org_extra_json',
        ),
        migrations.RemoveField(
            model_name='cjkcmspage',
            name='struct_org_geo_lat',
        ),
        migrations.RemoveField(
            model_name='cjkcmspage',
            name='struct_org_geo_lng',
        ),
        migrations.RemoveField(
            model_name='cjkcmspage',
            name='struct_org_hours',
        ),
        migrations.RemoveField(
            model_name='cjkcmspage',
            name='struct_org_image',
        ),
        migrations.RemoveField(
            model_name='cjkcmspage',
            name='struct_org_logo',
        ),
        migrations.RemoveField(
            model_name='cjkcmspage',
            name='struct_org_name',
        ),
        migrations.RemoveField(
            model_name='cjkcmspage',
            name='struct_org_phone',
        ),
        migrations.RemoveField(
            model_name='cjkcmspage',
            name='struct_org_type',
        ),
        migrations.AlterField(
            model_name='cjkcmspage',
            name='og_image',
            field=models.ForeignKey(blank=True, help_text='Shown when linking to this page on social media. If blank, may show an image from the page, or the default from Settings > SEO.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Preview image'),
        ),
    ]
