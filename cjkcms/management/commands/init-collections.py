from django.core.management.base import BaseCommand
from wagtail.core.models import Collection


class Command(BaseCommand):
    """Create a set of commonly used collections for a new website:
    covers, logos, resources, people, articles, cards, icons"""

    help = "Create a set of commonly used collections: "
    "covers, logos, resources, people, articles, cards, icons"

    def handle(self, *args, **options):
        names = ["Covers", "Logos", "Resources", "People", "Articles", "Cards", "Icons"]

        # try creating collection, if does not exist

        root_coll = Collection.get_first_root_node()

        if not root_coll:

            return

        for n in names:
            if Collection.objects.filter(name=n).exists():
                self.stdout.write(f"Collection {n} already exists, skipping creation.")
                continue
            root_coll.add_child(name=n)
            self.stdout.write(f"Created collection {n}")
