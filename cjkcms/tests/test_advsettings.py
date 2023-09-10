# from wagtail.test.utils import WagtailPageTests
# from wagtail.test.utils.form_data import nested_form_data

# from wagtail.models import Page
# from cjkcms.models.cms_models import ArticlePage


# class AdvSettingsTests(WagtailPageTests):
#     """Tests AdvSettings class functionality: custom id, customs class,
#     visibility opions, start/end visible.
#     """

#     def test_can_create_article_page(self):
#         # Get the HomePage
#         home_page = Page.objects.get(path="00010001")

#         body = [
#             {
#                 "type": "embed_video",
#                 "value": {
#                     "url": "https://youtu.be/AxLgTxBLsgI",
#                 },
#                 "id": "6ffa1b27-d884-4a9b-ba35-66140ff8a0ee",
#             }
#         ]

#         # set adv settings

#         article_page = ArticlePage(title="Test Article", body=body)

#         home_page.add_child(instance=article_page)
#         article_page.save_revision().publish()

#         ap = ArticlePage.objects.get(slug="test-article")

#         # self.assertEqual(ap.title, "Test Article")
