from wagtail.embeds.models import Embed
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Removes all instances of the Embed model. "
    "Run this if protected vimeo embeds are failing."

    def handle(self, *args, **options):
        try:
            Embed.objects.all().delete()
            return "All Embed model instances were successfully deleted!"
        except Exception as e:
            return e
