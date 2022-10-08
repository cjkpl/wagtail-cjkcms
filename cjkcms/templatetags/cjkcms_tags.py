import contextlib
import string
import random

from bs4 import BeautifulSoup
from django import template
from django.conf import settings
from django.db.models.query import QuerySet

# from django.forms import ClearableFileInput
from django.utils.safestring import mark_safe
from wagtail.core.models import Collection
from wagtail.images.models import Image

from cjkcms import __version__

from cjkcms.blocks.base_blocks import CjkcmsAdvSettings
from cjkcms.forms import SearchForm
from cjkcms.models import Footer, Navbar
from cjkcms.settings import cms_settings

from cjkcms.models.wagtailsettings_models import LayoutSettings

register = template.Library()


@register.filter
def is_advanced_setting(obj):
    return CjkcmsAdvSettings in (obj.__class__,) + obj.__class__.__bases__


@register.simple_tag
def cjkcms_version():
    return __version__


@register.simple_tag
def generate_random_id():
    value = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(20)
    )
    return f"cms-{value}"


@register.simple_tag
def brand_logo_long():
    return cms_settings.CJKCMS_BRAND_LOGO_LONG


@register.simple_tag
def brand_logo_square():
    return cms_settings.CJKCMS_BRAND_LOGO_SQUARE


# TODO: add a test
@register.simple_tag
def is_menu_item_dropdown(value):
    return len(value.get("sub_links", [])) > 0 or (
        value.get("show_child_links", False)
        and len(value.get("page", []).get_children().live()) > 0
    )


# TODO: add a test
@register.simple_tag(takes_context=True)
def is_active_page(context, curr_page, other_page):
    if hasattr(curr_page, "get_url") and hasattr(other_page, "get_url"):
        curr_url = curr_page.get_url(context["request"])
        other_url = other_page.get_url(context["request"])
        return curr_url == other_url
    return False


# TODO: add a test
@register.simple_tag
def get_pictures(collection_id):
    collection = Collection.objects.get(id=collection_id)
    return Image.objects.filter(collection=collection)


@register.simple_tag(takes_context=True)
def get_navbar_css(context):
    layout = LayoutSettings.for_request(context["request"])
    fixed = "fixed-top" if layout.navbar_fixed else ""
    return " ".join(
        [
            fixed,
            layout.navbar_collapse_mode,
            layout.navbar_color_scheme,
            layout.navbar_format,
            layout.navbar_class,
        ]
    )


@register.simple_tag(takes_context=True)
def get_navbars(context) -> "QuerySet[Navbar]":
    layout = LayoutSettings.for_request(context["request"])
    navbarorderables = layout.site_navbar.all()
    return Navbar.objects.filter(navbarorderable__in=navbarorderables).order_by(
        "navbarorderable__sort_order"
    )


@register.simple_tag(takes_context=True)
def get_footers(context) -> "QuerySet[Footer]":
    layout = LayoutSettings.for_request(context["request"])
    footerorderables = layout.site_footer.all()
    return Footer.objects.filter(footerorderable__in=footerorderables).order_by(
        "footerorderable__sort_order"
    )


@register.simple_tag
def get_searchform(request=None):
    return SearchForm(request.GET) if request else SearchForm()


@register.filter
def cjkcms_settings(value):
    return getattr(cms_settings, value)


@register.filter
def django_settings(value):
    return getattr(settings, value)


@register.simple_tag
def query_update(querydict, key=None, value=None):
    """
    Alters querydict (request.GET) by updating/adding/removing key to value
    """
    get = querydict.copy()
    if key:
        if value:
            get[key] = value
        else:
            with contextlib.suppress(KeyError):
                del get[key]
    return get


@register.simple_tag
def render_iframe_from_embed(embed):
    soup = BeautifulSoup(embed.html, "html.parser")
    with contextlib.suppress(AttributeError, TypeError):
        iframe_tags = soup.find("iframe")
        iframe_tags["title"] = embed.title  # type: ignore
        return mark_safe(soup.prettify())
    return mark_safe(embed.html)


@register.filter
def map_to_bootstrap_alert(message_tag):
    """
    Converts a message level to a bootstrap 5 alert class
    """
    message_to_alert_dict = {
        "debug": "primary",
        "info": "info",
        "success": "success",
        "warning": "warning",
        "error": "danger",
    }

    try:
        return message_to_alert_dict[message_tag]
    except KeyError:
        return ""


@register.simple_tag(takes_context=True)
def can_show_item(context, item_visibility: str) -> bool:
    """
    Menu item visibility conditional on selection in cms_settings.AUTH_VISIBILITY_CHOICES
    """
    if item_visibility == "hidden":
        return False
    if item_visibility == "all":
        return True
    is_auth = context["request"].user.is_authenticated
    return bool(
        is_auth
        and item_visibility == "auth-only"
        or not is_auth
        and item_visibility == "non-auth-only"
    )


@register.simple_tag(takes_context=True)
def link_display(context, text: str) -> str:
    """
    Check for double-curly braces + user.username/first_name/last_name/first_last_name.
    If found, display as requested from user record
    """
    if text not in {
        "{{ user.username }}",
        "{{ user.first_name }}",
        "{{ user.last_name }}",
        "{{ user.first_last_name }}",
    }:
        return text
    u = context["request"].user
    if text == "{{ user.username }}":
        return u.username
    if text == "{{ user.first_name }}":
        return u.first_name
    if text == "{{ user.last_name }}":
        return u.last_name
    return f"{u.first_name} {u.last_name}"


@register.filter
def get_name_of_class(class_type):
    if hasattr(class_type.__class__, "search_name"):
        return class_type.__class__.search_name
    elif hasattr(class_type.__class__, "_meta") and hasattr(
        class_type.__class__._meta, "verbose_name"
    ):
        return class_type.__class__._meta.verbose_name
    else:
        return class_type.__class__.__name__


@register.filter
def get_plural_name_of_class(class_type):
    if hasattr(class_type.__class__, "search_name_plural"):
        return class_type.__class__.search_name_plural
    elif hasattr(class_type.__class__, "_meta") and hasattr(
        class_type.__class__._meta, "verbose_name_plural"
    ):
        return class_type.__class__._meta.verbose_name_plural
    else:
        return f"{class_type.__class__.__name__}s"
