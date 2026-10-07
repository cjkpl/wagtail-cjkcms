from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from wagtail.models import Page

from cjkcms.models.cms_models import WebPage
from cjkcms.templatetags.cjkcms_tags import is_menu_item_dropdown


class MenuItemDropdownTests(TestCase):
    def setUp(self):
        home_page = Page.objects.get(path="00010001")
        self.parent = WebPage(title="Parent", slug="parent")
        home_page.add_child(instance=self.parent)

    def add_child(self, live=True):
        child = WebPage(title="Child", slug=f"child-{live}", live=live)
        self.parent.add_child(instance=child)
        return child

    def test_sub_links_make_a_dropdown(self):
        with self.assertNumQueries(0):
            self.assertTrue(is_menu_item_dropdown({"sub_links": ["link"]}))

    def test_no_dropdown_without_sub_links_or_child_links(self):
        self.add_child()
        value = {"sub_links": [], "page": self.parent, "show_child_links": False}
        with self.assertNumQueries(0):
            self.assertFalse(is_menu_item_dropdown(value))

    def test_no_dropdown_without_page(self):
        self.assertFalse(is_menu_item_dropdown({"show_child_links": True}))
        self.assertFalse(
            is_menu_item_dropdown({"page": None, "show_child_links": True})
        )

    def test_child_links_need_a_live_child(self):
        value = {"sub_links": [], "page": self.parent, "show_child_links": True}
        self.assertFalse(is_menu_item_dropdown(value))

        self.add_child(live=False)
        self.assertFalse(is_menu_item_dropdown(value))

        self.add_child(live=True)
        self.assertTrue(is_menu_item_dropdown(value))

    def test_child_pages_are_not_loaded(self):
        self.add_child()
        value = {"sub_links": [], "page": self.parent, "show_child_links": True}
        with CaptureQueriesContext(connection) as queries:
            self.assertTrue(is_menu_item_dropdown(value))
        self.assertEqual(len(queries), 1)
        self.assertNotIn('"wagtailcore_page"."title"', queries[0]["sql"])
