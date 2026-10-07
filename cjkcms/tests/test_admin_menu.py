import pytest
from django.urls import reverse
from wagtail.admin.menu import admin_menu

from cjkcms.models import Footer, Navbar

pytestmark = pytest.mark.django_db


def menu_items(rf, user):
    request = rf.get("/admin/")
    request.user = user
    return admin_menu.menu_items_for_request(request)


def listing_url(model):
    return reverse(f"wagtailsnippets_{model._meta.app_label}_{model._meta.model_name}:list")


def test_navigation_menu_item_is_shown_once(rf, admin_user):
    items = [item for item in menu_items(rf, admin_user) if item.label == "Navigation"]

    assert [item.url for item in items] == [listing_url(Navbar)]


def test_footers_are_listed_under_snippets(rf, admin_client, admin_user):
    urls = [item.url for item in menu_items(rf, admin_user)]
    assert listing_url(Footer) not in urls

    response = admin_client.get(reverse("wagtailsnippets:index"))
    assert response.status_code == 200
    content = response.content.decode()
    assert listing_url(Footer) in content
    # Navbars keep their own menu item, so they are not repeated here.
    assert listing_url(Navbar) not in content.split("<main")[1]


def test_footer_listing_still_works(admin_client):
    Footer.objects.create(name="Main footer", content=[])

    response = admin_client.get(listing_url(Footer))

    assert response.status_code == 200
    assert b"Main footer" in response.content
    assert "custom_css_class" in response.context["table"].columns
