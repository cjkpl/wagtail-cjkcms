from .snippet_models import Navbar, EventCalendar
from wagtail.snippets.views.snippets import SnippetViewSet


class NavbarSnippet(SnippetViewSet):
    model = Navbar
    menu_label = "Navigation"
    menu_icon = "link"  # change as required
    add_to_admin_menu = True
    list_display = (
        "name",
        "custom_css_class",
        "custom_id",
    )
    search_fields = [
        "name",
    ]


class EventCalendarSnippet(SnippetViewSet):
    model = EventCalendar
    menu_label = "Public Events"
    menu_icon = "calendar"  # change as required
    # add_to_admin_menu = True
    list_display = ("name",)
    search_fields = [
        "name",
    ]
