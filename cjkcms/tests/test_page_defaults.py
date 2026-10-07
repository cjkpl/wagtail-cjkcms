from django.test import TestCase
from wagtail.models import Locale, Page

from cjkcms.models.cms_models import ArticleIndexPage, ArticlePage, WebPage
from cjkcms.tests.testapp.models import ProjectArticleIndexPage


class PageDefaultsTests(TestCase):
    """Page type defaults apply to new pages only when no value is given."""

    def setUp(self):
        self.home_page = Page.objects.get(path="00010001")

    def add_page(self, model, **kwargs):
        page = model(title="Defaults", slug="defaults", **kwargs)
        self.home_page.add_child(instance=page)
        return model.objects.get(pk=page.pk)

    def assert_index_fields(self, page, show_subpages, related_show, order_by):
        self.assertEqual(page.index_show_subpages, show_subpages)
        self.assertEqual(page.related_show, related_show)
        self.assertEqual(page.index_order_by, order_by)

    def test_new_page_uses_page_type_defaults(self):
        self.assert_index_fields(WebPage(), False, False, "")
        self.assert_index_fields(ArticlePage(), False, True, "")
        self.assert_index_fields(ArticleIndexPage(), True, False, "")
        self.assert_index_fields(ProjectArticleIndexPage(), True, False, "-date_display")

    def test_values_passed_to_constructor_are_kept(self):
        page = WebPage(index_show_subpages=True, related_show=True, index_order_by="title")
        self.assert_index_fields(page, True, True, "title")

        page = ProjectArticleIndexPage(index_show_subpages=False, index_order_by="")
        self.assert_index_fields(page, False, False, "")

    def test_only_missing_values_get_defaults(self):
        page = ArticlePage(index_order_by="title")
        self.assert_index_fields(page, False, True, "title")

    def test_created_page_keeps_values(self):
        page = self.add_page(ArticleIndexPage, index_show_subpages=False)
        self.assert_index_fields(page, False, False, "")

    def test_loaded_page_keeps_stored_values(self):
        page = self.add_page(ArticleIndexPage)
        ArticleIndexPage.objects.filter(pk=page.pk).update(index_show_subpages=False)
        self.assertFalse(ArticleIndexPage.objects.get(pk=page.pk).index_show_subpages)
        self.assertFalse(
            ArticleIndexPage.objects.only("title").get(pk=page.pk).index_show_subpages
        )

    def test_copy_keeps_values(self):
        page = self.add_page(
            WebPage, index_show_subpages=True, related_show=True, index_order_by="title"
        )
        new_page = page.copy(update_attrs={"slug": "defaults-copy", "title": "Copy"})
        self.assert_index_fields(WebPage.objects.get(pk=new_page.pk), True, True, "title")

    def test_copy_keeps_values_differing_from_page_type_defaults(self):
        page = self.add_page(ArticleIndexPage, index_show_subpages=False)
        new_page = page.copy(update_attrs={"slug": "defaults-copy", "title": "Copy"})
        self.assert_index_fields(
            ArticleIndexPage.objects.get(pk=new_page.pk), False, False, ""
        )

    def test_alias_keeps_values(self):
        page = self.add_page(
            WebPage, index_show_subpages=True, related_show=True, index_order_by="title"
        )
        alias = page.create_alias(update_slug="defaults-alias")
        self.assert_index_fields(WebPage.objects.get(pk=alias.pk), True, True, "title")

    def test_translation_keeps_values(self):
        page = self.add_page(
            WebPage, index_show_subpages=True, related_show=True, index_order_by="title"
        )
        locale = Locale.objects.create(language_code="pl")
        translation = page.copy_for_translation(locale, copy_parents=True)
        self.assert_index_fields(
            WebPage.objects.get(pk=translation.pk), True, True, "title"
        )

    def test_revision_keeps_values(self):
        page = self.add_page(WebPage)
        page.index_show_subpages = True
        page.related_show = True
        page.index_order_by = "title"
        revision = page.save_revision()
        self.assert_index_fields(revision.as_object(), True, True, "title")
