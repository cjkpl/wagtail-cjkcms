from django.core.management.base import BaseCommand
from wagtail.core.models import Page, Site
from cjkcms.models import Navbar, LayoutSettings, NavbarOrderable


class Command(BaseCommand):
    """
    Create main-menu nav bar, and assign it in the Layout settings.
    Assigs a custom_id=main-menu to detect attempts to re-create.
    """

    help = "creates CjkCMS Navbar with Home entry pointing to /, "
    "and if --add_auth also login/logout entries"
    add_auth_items = False

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force overwrite if navbar with custom_id=main-menu already exists",
        )

        parser.add_argument(
            "--add_auth_items",
            action="store_true",
            help="Add entries for `/login`, `signup` and `[username]`",
        )

    def _setup_main_menu(self):
        n = Navbar.objects.filter(custom_id="main-menu")
        if len(n) > 0:
            print("main-menu navbar already exists, re-creating")
            n.delete()

        home_page = Page.objects.filter(path="00010001").first()
        if not home_page:
            print(
                "Homepage not found in page tree. "
                "Create at least the home page, then create main-menu"
            )
            return

        home_item = (("page_link", {"display_text": "Home", "page": home_page}),)
        auth_items = (
            (
                (
                    "external_link",
                    {
                        "display_text": "Login",
                        "link": "/login",
                        "visible_for": "non-auth-only",
                    },
                ),
                (
                    "external_link",
                    {
                        "display_text": "Register",
                        "link": "/signup",
                        "visible_for": "non-auth-only",
                    },
                ),
                (
                    "page_link",
                    {
                        "display_text": "{{ user.first_last_name }}",
                        "page": home_page,
                        "visible_for": "auth-only",
                    },
                ),
            )
            if self.add_auth_items
            else ()
        )

        n = Navbar(
            name="Main menu",
            custom_id="main-menu",
            menu_items=(home_item + auth_items),
        )
        n.save()

        # get default Wagtail site
        site = Site.objects.filter(is_default_site=True).first()
        layout_settings = LayoutSettings.for_site(site)

        # add NavbarOrderable to Layout
        no = NavbarOrderable(navbar_chooser=layout_settings, navbar=n)
        no.save()

    def handle(self, raise_error=False, *args, **options):
        # check if ok to overwrite (force == 1)
        force = options["force"]
        verbosity = options["verbosity"]
        self.add_auth_items = options["add_auth_items"]
        checks = [Navbar.objects.filter(custom_id="main-menu").count() > 0]
        if any(checks) and not force:
            # YOU SHOULD NEVER RUN THIS COMMAND WITHOUT PRIOR DB DUMP
            raise RuntimeError(
                "Navbar with custom_id=main-menu found. Aborting. use force=1 to overwrite"
            )

        self._setup_main_menu()
        if verbosity > 0:
            msg = "Main menu navbar successfully created."
            self.stdout.write(msg)
