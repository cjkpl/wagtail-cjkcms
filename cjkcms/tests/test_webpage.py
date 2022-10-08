from wagtail.tests.utils import WagtailPageTests
from cjkcms.models import CjkcmsWebPage
from cjkcms.models.cms_models import WebPage
from wagtail.tests.utils.form_data import nested_form_data

from wagtail.core.models import Page


class WebPageTests(WagtailPageTests):
    """Tests CjkCms Web Page"""

    def test_cannot_create_cjkcms_web_page(self):
        # Get the HomePage
        # root_page = Page.objects.get(path='0001')
        # root page is useless, objects added here are not served under default site
        home_page = Page.objects.get(path="00010001")

        # Assert that a CjkcmsWebPage can NOT be made here, it's abstract
        self.assertCanNotCreateAt(
            home_page, CjkcmsWebPage, nested_form_data({"title": "About us"})
        )

    def test_can_create_web_page(self):
        # Get the HomePage
        body = [
            {
                "type": "embed_video",
                "value": {
                    "url": "https://youtu.be/AxLgTxBLsgI",
                },
                "id": "6ffa1b27-d884-4a9b-ba35-66140ff8a0ee",
            }
        ]
        home_page = Page.objects.get(path="00010001")

        web_page = WebPage(title="Test Web Home", body=body)

        home_page.add_child(instance=web_page)
        web_page.save_revision().publish()

        wp = WebPage.objects.get(slug="test-web-home")
        self.assertEqual(wp.title, "Test Web Home")

    # def test_site_root_is_polish(self):
    #     site = Site.objects.get()
    #     site.root_page.specific
