from django.core.management.base import BaseCommand
from wagtail.embeds.models import Embed


class Command(BaseCommand):
    help = "Removes all instances of the Embed model. "
    "Run this if protected vimeo embeds are failing."

    def handle(self, *args, **options):
        Embed.objects.all().delete()
        return "All Embed model instances were successfully deleted!"
