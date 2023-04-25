# Generated by Django 4.0.10 on 2023-04-25 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cjkcms', '0007_layoutsettings_bootstrap_icons'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layoutsettings',
            name='navbar_langselector',
            field=models.CharField(blank=True, default=None, help_text='Choose lang choice selector', max_length=255, null=True, verbose_name='Language selector'),
        ),
    ]
