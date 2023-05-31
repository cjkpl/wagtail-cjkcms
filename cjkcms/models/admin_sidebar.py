from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
)
from .snippet_models import Navbar


class NavbarAdmin(ModelAdmin):
    model = Navbar
    menu_icon = "link"  # change as required
    list_display = (
        "name",
        "custom_css_class",
        "custom_id",
    )
    search_fields = [
        "name",
    ]
