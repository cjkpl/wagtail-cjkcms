import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db import IntegrityError, transaction
from django.test import Client, RequestFactory
from django.urls import reverse
from wagtail.admin.ui.tables import Column, UpdatedAtColumn
from wagtail.snippets.models import get_snippet_models
from wagtail.snippets.views.snippets import IndexView

from cjkcms.admin_viewsets import (
    CjkcmsSnippetIndexView,
    CjkcmsSnippetViewSet,
    ListingPreferencesMixin,
)
from cjkcms.models.admin_preferences import AdminListingPreference
from cjkcms.models.snippet_models import EventCalendar, Footer, Navbar

pytestmark = pytest.mark.django_db


@pytest.fixture
def admin_user():
    return get_user_model().objects.create_superuser(
        username="listing-admin", email="admin@example.com", password="test"
    )


@pytest.fixture
def admin_client(client, admin_user):
    client.force_login(admin_user)
    return client


def listing_url(model=Navbar, results=False):
    return reverse(
        f"wagtailsnippets_{model._meta.app_label}_{model._meta.model_name}:"
        f"{'list_results' if results else 'list'}"
    )


def preference_key(model=Navbar):
    return (
        f"{model._meta.label_lower}:"
        f"wagtailsnippets_{model._meta.app_label}_{model._meta.model_name}:list"
    )


def test_all_cms_snippets_use_preferences(admin_client):
    models = [model for model in get_snippet_models() if model._meta.app_label == "cjkcms"]
    assert len(models) == 8
    for model in models:
        response = admin_client.get(listing_url(model))
        assert response.status_code == 200
        assert isinstance(response.context["view"], ListingPreferencesMixin)
        assert b"data-listing-preferences-form" in response.content
    assert not AdminListingPreference.objects.exists()


def test_save_columns_and_page_size_applies_to_full_and_ajax_listing(admin_client, admin_user):
    Navbar.objects.bulk_create([Navbar(name=f"Nav {i:02}") for i in range(25)])
    url = listing_url()
    response = admin_client.get(url)
    assert response.context["paginator"].per_page == 20
    assert "custom_css_class" in response.context["table"].columns
    assert b"Add Navigation Bar" in response.content
    assert b"data-search-form" in response.content

    response = admin_client.post(
        url + "?p=2&ordering=name&q=Nav&language=en",
        {
            "listing_preferences_action": "apply",
            "visible_columns": ["custom_id"],
            "page_size": "10",
        },
    )
    assert response.status_code == 302
    assert response.url == url + "?ordering=name&q=Nav&language=en"
    preference = AdminListingPreference.objects.get(user=admin_user)
    assert preference.listing_key == preference_key()
    assert preference.hidden_columns == ["custom_css_class"]
    assert preference.page_size == 10

    for target in (url, listing_url(results=True)):
        response = admin_client.get(target)
        assert response.status_code == 200
        assert response.context["paginator"].per_page == 10
        assert len(response.context["page_obj"]) == 10
        assert "custom_css_class" not in response.context["table"].columns
        assert {"name", "custom_id", "bulk_actions"} <= response.context["table"].columns.keys()
    # A new browser session uses the same persisted preferences.
    another_browser = Client()
    another_browser.force_login(admin_user)
    assert another_browser.get(url).context["paginator"].per_page == 10


def test_preferences_are_isolated_by_user_and_listing(admin_client, admin_user):
    admin_client.post(listing_url(), {"listing_preferences_action": "apply", "page_size": "50"})
    other = get_user_model().objects.create_superuser(username="other", password="test")
    other_client = Client()
    other_client.force_login(other)
    response = other_client.get(listing_url())
    assert response.context["paginator"].per_page == 20
    assert "custom_css_class" in response.context["table"].columns
    assert admin_client.get(listing_url(Footer)).context["paginator"].per_page == 20
    assert AdminListingPreference.objects.count() == 1
    assert AdminListingPreference.objects.get().user == admin_user


@pytest.mark.parametrize(
    "data",
    [
        {"page_size": "100000"},
        {"page_size": "0"},
        {"page_size": "-1"},
        {"page_size": "oops"},
        {"visible_columns": ["secret_field"]},
        {"visible_columns": ["name"]},
        {"visible_columns": ["bulk_actions"]},
    ],
)
def test_invalid_preferences_are_rejected(admin_client, data):
    response = admin_client.post(listing_url(), {"listing_preferences_action": "apply", **data})
    assert response.status_code == 400
    assert not AdminListingPreference.objects.exists()


def test_reset_only_affects_current_listing_and_user(admin_client, admin_user):
    for model in (Navbar, Footer):
        admin_client.post(
            listing_url(model),
            {
                "listing_preferences_action": "apply",
                "page_size": "50",
            },
        )
    response = admin_client.post(
        listing_url() + "?p=9&q=hello", {"listing_preferences_action": "reset"}
    )
    assert response.url == listing_url() + "?q=hello"
    assert list(AdminListingPreference.objects.values_list("listing_key", flat=True)) == [
        preference_key(Footer)
    ]
    response = admin_client.get(listing_url())
    assert response.context["paginator"].per_page == 20
    assert "custom_css_class" in response.context["table"].columns


def test_stale_preferences_cannot_hide_required_columns(admin_client, admin_user):
    AdminListingPreference.objects.create(
        user=admin_user,
        listing_key=preference_key(),
        page_size=999,
        hidden_columns=["removed_column", "name", "bulk_actions", "custom_id"],
    )
    response = admin_client.get(listing_url())
    assert {"name", "bulk_actions", "custom_css_class"} <= response.context["table"].columns.keys()
    assert "custom_id" not in response.context["table"].columns
    assert response.context["paginator"].per_page == 20


def test_authentication_model_permissions_and_csrf(client, admin_user):
    assert client.post(listing_url(), {"listing_preferences_action": "apply"}).status_code == 302
    restricted = get_user_model().objects.create_user(username="restricted", password="test")
    restricted.user_permissions.add(Permission.objects.get(codename="access_admin"))
    client.force_login(restricted)
    response = client.post(listing_url(), {"listing_preferences_action": "apply"})
    # Wagtail converts PermissionDenied into a redirect to the admin homepage.
    assert response.status_code == 302
    assert response.url == reverse("wagtailadmin_home")
    assert not AdminListingPreference.objects.exists()
    csrf_client = Client(enforce_csrf_checks=True)
    csrf_client.force_login(admin_user)
    assert (
        csrf_client.post(listing_url(), {"listing_preferences_action": "apply"}).status_code == 403
    )
    csrf_client.get(listing_url())
    token = csrf_client.cookies["csrftoken"].value
    response = csrf_client.post(
        listing_url(),
        {
            "listing_preferences_action": "apply",
            "csrfmiddlewaretoken": token,
            "user": restricted.pk,
            "listing_key": "someone-elses-listing",
            "page_size": "10",
        },
    )
    assert response.status_code == 302
    preference = AdminListingPreference.objects.get()
    assert preference.user == admin_user
    assert preference.listing_key == preference_key()


def test_unique_preferences_and_user_deletion(admin_user):
    assert AdminListingPreference._meta.get_field("user").remote_field.model is get_user_model()
    AdminListingPreference.objects.create(user=admin_user, listing_key=preference_key())
    with pytest.raises(IntegrityError), transaction.atomic():
        AdminListingPreference.objects.create(user=admin_user, listing_key=preference_key())
    admin_user.delete()
    assert not AdminListingPreference.objects.exists()


def test_custom_listing_preserves_queryset_search_sorting_and_export(admin_user):
    Navbar.objects.bulk_create([Navbar(name="Keep Z"), Navbar(name="Keep A"), Navbar(name="Other")])

    class ProjectIndexView(ListingPreferencesMixin, IndexView):
        def get_base_queryset(self):
            return super().get_base_queryset().filter(name__startswith="Keep")

    class ProjectViewSet(CjkcmsSnippetViewSet):
        model = Navbar
        index_view_class = ProjectIndexView
        list_display = ["name", Column("custom_id"), UpdatedAtColumn()]
        search_fields = ["name"]
        list_filter = ["name"]
        list_export = ["name", "custom_id"]
        list_per_page = 7

    viewset = ProjectViewSet()
    AdminListingPreference.objects.create(
        user=admin_user, listing_key=preference_key(), hidden_columns=["_updated_at", "custom_id"]
    )
    factory = RequestFactory()
    request = factory.get(listing_url(), {"q": "Keep", "ordering": "name"})
    request.user = admin_user
    response = viewset.index_view(request)
    assert [item.name for item in response.context_data["object_list"]] == ["Keep A", "Keep Z"]
    assert "custom_id" not in response.context_data["table"].columns
    assert "_updated_at" not in response.context_data["table"].columns
    assert response.context_data["paginator"].per_page == 7
    response.render()
    assert b"filters-drilldown" in response.content
    assert b"data-listing-preferences-form" in response.content
    request = factory.get(listing_url(), {"name": "Keep A"})
    request.user = admin_user
    response = viewset.index_view(request)
    assert [item.name for item in response.context_data["object_list"]] == ["Keep A"]
    # Sorting on a hidden annotation-backed column must still build valid SQL.
    request = factory.get(listing_url(), {"ordering": "_updated_at"})
    request.user = admin_user
    response = viewset.index_view(request)
    assert len(response.context_data["object_list"]) == 2
    request = factory.get(listing_url(), {"export": "csv"})
    request.user = admin_user
    response = viewset.index_view(request)
    content = b"".join(response.streaming_content).decode()
    assert "Custom ID" in content
    assert "Keep A" in content
    assert "Other" not in content


def test_reordering_retains_unpaginated_behavior(admin_user):
    AdminListingPreference.objects.create(
        user=admin_user, listing_key=preference_key(), page_size=10
    )
    request = RequestFactory().get(listing_url())
    request.user = admin_user
    view = CjkcmsSnippetIndexView(
        model=Navbar, index_url_name="wagtailsnippets_cjkcms_navbar:list", paginate_by=20
    )
    view.setup(request)
    view.show_ordering_column = True
    assert view.get_paginate_by(Navbar.objects.all()) is None


def test_invalid_post_actions_and_results_endpoint(admin_client):
    assert admin_client.post(listing_url(), {}).status_code == 400
    assert (
        admin_client.post(
            listing_url(results=True), {"listing_preferences_action": "apply"}
        ).status_code
        == 400
    )
    assert not AdminListingPreference.objects.exists()


def test_ajax_save_and_reset_return_json_without_redirects(admin_client, admin_user):
    url = listing_url()
    response = admin_client.post(
        url,
        {
            "listing_preferences_action": "apply",
            "visible_columns": ["custom_id"],
            "page_size": "10",
        },
        HTTP_ACCEPT="application/json",
    )
    assert response.status_code == 200
    assert response.json() == {"saved": True}
    preference = AdminListingPreference.objects.get(user=admin_user)
    assert preference.hidden_columns == ["custom_css_class"]
    assert preference.page_size == 10
    response = admin_client.get(listing_url(results=True))
    assert "custom_css_class" not in response.context["table"].columns
    assert response.context["paginator"].per_page == 10
    response = admin_client.post(
        url, {"listing_preferences_action": "reset"}, HTTP_ACCEPT="application/json"
    )
    assert response.status_code == 200
    assert response.json() == {"saved": True}
    assert not AdminListingPreference.objects.exists()


def test_ajax_invalid_choices_leave_saved_preferences_unchanged(admin_client, admin_user):
    preference = AdminListingPreference.objects.create(
        user=admin_user, listing_key=preference_key(), page_size=20
    )
    response = admin_client.post(
        listing_url(),
        {
            "listing_preferences_action": "apply",
            "visible_columns": ["secret_field"],
            "page_size": "999",
        },
        HTTP_ACCEPT="application/json",
    )
    assert response.status_code == 400
    assert {"visible_columns", "page_size"} <= response.json().keys()
    preference.refresh_from_db()
    assert preference.page_size == 20
    assert preference.hidden_columns == []


def test_display_options_render_as_autosaving_wagtail_dropdown(admin_client):
    content = admin_client.get(listing_url()).content.decode()
    # An unknown theme leaves Wagtail's dropdown without styling or click-away.
    assert 'data-w-dropdown-theme-value="drilldown"' in content
    assert 'data-w-dropdown-keep-mounted-value="true"' in content
    assert f'data-results-url="{listing_url(results=True)}"' in content
    assert "data-listing-shortcuts" in content
    # Wagtail replaces only the results on AJAX refreshes; the options stay in the header.
    content = admin_client.get(listing_url(results=True)).content.decode()
    assert "data-listing-preferences-form" not in content


def test_listing_without_optional_columns_only_offers_page_size(admin_client):
    response = admin_client.get(listing_url(EventCalendar))
    assert response.context["listing_preferences_form"].fields["visible_columns"].choices == []
    content = response.content.decode()
    assert "data-listing-preferences-form" in content
    assert 'name="page_size"' in content
    assert "data-listing-shortcuts" not in content
    assert 'name="visible_columns"' not in content
