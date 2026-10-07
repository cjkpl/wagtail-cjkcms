from unittest.mock import patch

import pytest
from django import forms
from django.core.exceptions import ValidationError
from django.test import override_settings
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page

from cjkcms.models.cms_models import ArticlePage, WebPage
from cjkcms.models.page_models import CjkcmsPage
from cjkcms.panels import CjkcmsTabbedInterface

pytestmark = pytest.mark.django_db


TEMPLATES = {
    "*": [("", "Default"), ("shared.html", "Shared")],
    "webpage": [("web.html", "Web")],
    "articlepage": [("article.html", "Article")],
}


@pytest.fixture(autouse=True)
def template_settings():
    with override_settings(CJKCMS_FRONTEND_TEMPLATES_PAGES=TEMPLATES):
        yield


def edit_form_class(model, fields=("custom_template", "index_order_by")):
    return (
        CjkcmsTabbedInterface([FieldPanel(name) for name in fields])
        .bind_to_model(model)
        .get_form_class()
    )


def clean_choice_fields(page, exclude=()):
    page.clean_fields(
        exclude={
            field.name
            for field in page._meta.fields
            if field.name not in {"custom_template", "index_order_by"}
        }
        | set(exclude)
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "model,other,template",
    [(WebPage, ArticlePage, "web.html"), (ArticlePage, WebPage, "article.html")],
)
def test_interleaved_page_types_validate_save_and_restore_revision(model, other, template):
    parent = Page.objects.get(path="00010001")
    page = model(title="Template test", custom_template=template)
    parent.add_child(instance=page)
    form = edit_form_class(model)(
        data={"custom_template": template, "index_order_by": "title"}, instance=page
    )

    # Reproduce a different page being fetched between form creation and validation.
    other(title="Unrelated page")
    CjkcmsPage()
    assert form.is_valid(), form.errors
    saved = form.save()
    revision = saved.save_revision()
    restored = revision.as_object()
    other()
    restored.full_clean()
    saved.refresh_from_db()
    assert saved.custom_template == restored.custom_template == template


def test_real_edit_handler_keeps_choices_local_to_each_form():
    web_form_class = WebPage.get_edit_handler().get_form_class()
    article_form_class = ArticlePage.get_edit_handler().get_form_class()
    web = web_form_class(instance=WebPage())
    article = article_form_class(instance=ArticlePage())
    assert list(web.fields["custom_template"].choices) == TEMPLATES["*"] + TEMPLATES["webpage"]
    assert (
        list(article.fields["custom_template"].choices) == TEMPLATES["*"] + TEMPLATES["articlepage"]
    )
    web.fields["custom_template"].choices = []
    assert list(web_form_class(instance=WebPage()).fields["custom_template"].choices) == (
        TEMPLATES["*"] + TEMPLATES["webpage"]
    )


def test_instantiation_does_not_mutate_shared_fields():
    fields = [CjkcmsPage._meta.get_field(name) for name in ("custom_template", "index_order_by")]
    original_choices = [field.choices for field in fields]
    WebPage()
    ArticlePage()
    CjkcmsPage()
    assert [field.choices for field in fields] == original_choices


@pytest.mark.parametrize("template", ["", "shared.html", "web.html"])
def test_model_accepts_default_global_and_model_templates(template):
    page = WebPage(custom_template=template)
    ArticlePage()
    clean_choice_fields(page)


@pytest.mark.parametrize("template", ["article.html", "removed.html"])
def test_form_and_model_reject_other_page_templates_and_removed_templates(template):
    page = WebPage(custom_template=template)
    field = edit_form_class(WebPage)(instance=page).fields["custom_template"]
    with pytest.raises(ValidationError) as form_error:
        field.clean(template)
    assert form_error.value.code == "invalid_choice"
    with pytest.raises(ValidationError) as model_error:
        clean_choice_fields(page)
    assert model_error.value.error_dict["custom_template"][0].code == "invalid_choice"
    clean_choice_fields(page, exclude={"custom_template"})


def test_excluded_form_field_is_not_reintroduced():
    form = edit_form_class(WebPage, fields=("title",))(instance=WebPage())
    assert "custom_template" not in form.fields
    assert "index_order_by" not in form.fields


def test_form_retains_blank_option_when_settings_omit_it():
    with override_settings(CJKCMS_FRONTEND_TEMPLATES_PAGES={"webpage": [("web.html", "Web")]}):
        field = edit_form_class(WebPage)(instance=WebPage()).fields["custom_template"]
        assert next(iter(field.choices))[0] == ""
        assert field.clean("") == ""


def test_model_keeps_length_validation_and_aggregates_errors():
    template = "x" * 256
    with override_settings(CJKCMS_FRONTEND_TEMPLATES_PAGES={"*": [(template, "Long")]}):
        page = WebPage(custom_template=template, index_num_per_page=-1)
        with pytest.raises(ValidationError) as error:
            page.clean_fields()
    assert error.value.error_dict["custom_template"][0].code == "max_length"
    assert "index_num_per_page" in error.value.error_dict


def test_subclass_ordering_choices_are_isolated():
    with patch.object(WebPage, "index_order_by_choices", [("custom_order", "Custom")]):
        page = WebPage()
        page.index_order_by = "custom_order"
        form = edit_form_class(WebPage)(instance=page)
        ArticlePage()
        assert form.fields["index_order_by"].clean("custom_order") == "custom_order"
        clean_choice_fields(page)
        other = ArticlePage()
        other.index_order_by = "custom_order"
        with pytest.raises(ValidationError) as error:
            clean_choice_fields(other)
        assert error.value.error_dict["index_order_by"][0].code == "invalid_choice"


@pytest.mark.django_db
def test_site_custom_form_is_preserved():
    class SitePageForm(WagtailAdminPageForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["custom_template"].help_text = "Site help"
            self.fields["custom_template"].widget = forms.HiddenInput()

        def clean(self):
            cleaned = super().clean()
            self.site_clean_called = True
            return cleaned

    with patch.object(WebPage, "base_form_class", SitePageForm):
        form = edit_form_class(WebPage)(data={"custom_template": "web.html"}, instance=WebPage())
    assert isinstance(form, SitePageForm)
    assert form.fields["custom_template"].help_text == "Site help"
    assert isinstance(form.fields["custom_template"].widget, forms.HiddenInput)
    assert form.is_valid(), form.errors
    assert form.site_clean_called
