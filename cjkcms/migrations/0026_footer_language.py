# Generated manually by Codex on 2026-01-29
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cjkcms", "0025_alter_filmpanel_background_color_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="footer",
            name="language",
            field=models.CharField(
                blank=True,
                choices=[],
                default="_all_",
                help_text="Select a language to limit display to specific locale.",
                max_length=10,
                verbose_name="Show in language",
            ),
        ),
    ]
