from datetime import datetime, timedelta, timezone
from wagtail.test.utils import WagtailPageTests
from django.contrib.auth.models import User, Group

from wagtail.models import Page
from cjkcms.models.cms_models import ArticlePage
import uuid


class AdvSettingsTests(WagtailPageTests):
    """Tests AdvSettings class functionality: custom id, customs class,
    visibility options, start/end visible.
    """

    def setUp(self):
        # create a test user
        test_user1 = User.objects.create_user(username="testuser1", password="12345")
        test_user1.save()

        self.group22 = Group(name="Group22")
        self.group22.save()
        test_user2 = User.objects.create_user(username="testuser2", password="12345")
        test_user2.groups.add(self.group22)
        test_user2.save()

        self.group23 = Group(name="Group23")
        self.group23.save()
        test_user3 = User.objects.create_user(username="testuser3", password="12345")
        test_user3.groups.add(self.group23)
        test_user3.save()

        test_user4 = User.objects.create_user(username="testuser4", password="12345")
        test_user4.groups.add(self.group22)
        test_user4.groups.add(self.group23)
        test_user4.save()

        self.in_the_past = datetime.now(tz=timezone.utc) - timedelta(days=1)
        self.in_the_future = datetime.now(tz=timezone.utc) + timedelta(days=1)

    def createArticlePage(self, title: str, settings: dict):
        # Get the HomePage
        home_page = Page.objects.get(path="00010001")

        body = [
            {
                "type": "quote",
                "value": {
                    "settings": settings,
                    "text": "Quotably interesting",
                    "author": "By Mr Nobody",
                },
                "id": str(uuid.uuid1()),
            }
        ]

        article_page = ArticlePage(title=title, body=body)

        home_page.add_child(instance=article_page)
        article_page.save_revision().publish()

        return article_page

    def test_visible_from_to(self):
        settings = {
            "visible_from": self.in_the_past.isoformat(),
            "visible_to": self.in_the_future.isoformat(),
        }

        self.createArticlePage(title="Test Article", settings=settings)

        ap = ArticlePage.objects.get(slug="test-article")

        response = self.client.get(ap.url)
        self.assertContains(response, "Quotably interesting", status_code=200)

    def test_not_visible_from(self):
        settings = {
            "visible_from": self.in_the_future.isoformat(),
        }

        self.createArticlePage(title="Test Article2", settings=settings)

        ap = ArticlePage.objects.get(slug="test-article2")

        response = self.client.get(ap.url)
        self.assertNotContains(response, "Quotably interesting", status_code=200)

    def test_not_visible_to(self):
        settings = {
            "visible_to": self.in_the_past.isoformat(),
        }

        self.createArticlePage(title="Test Article3", settings=settings)

        ap = ArticlePage.objects.get(slug="test-article3")

        response = self.client.get(ap.url)
        self.assertNotContains(response, "Quotably interesting", status_code=200)

    def test_visible_to_loggedin(self):
        settings = {
            "visibility": "auth-only",
            "visibility_groups": "",
        }

        self.createArticlePage(title="Test Article4", settings=settings)

        ap = ArticlePage.objects.get(slug="test-article4")

        response = self.client.get(ap.url)
        self.assertNotContains(response, "Quotably interesting", status_code=200)

        self.client.login(username="testuser1", password="12345")

        response = self.client.get(ap.url)
        # print(response.content)
        self.assertContains(response, "Quotably interesting", status_code=200)

    def test_invisible_to_loggedin(self):
        settings = {
            "visibility": "non-auth-only",
            "visibility_groups": "",
        }

        self.createArticlePage(title="Test Article5", settings=settings)

        ap = ArticlePage.objects.get(slug="test-article5")

        response = self.client.get(ap.url)
        self.assertContains(response, "Quotably interesting", status_code=200)

        self.client.login(username="testuser1", password="12345")

        ap = ArticlePage.objects.get(slug="test-article5")
        response = self.client.get(ap.url)
        # print(response.content)

        # @TODO: improve the test
        # note: the page meta description will contain the "Quotably interesting",
        # because the "body_preview" call gets the content rendered without context,
        # and so it sees the page as not-logged-in

        self.assertContains(
            response, '<div class="block-quote"></div>', status_code=200
        )

    def test_visible_to_specific_group(self):
        # sourcery skip: extract-duplicate-method
        settings = {
            "visibility": "include-groups",
            "visibility_groups": "Group22,Group23",
        }

        self.createArticlePage(title="Test Article6", settings=settings)

        ap = ArticlePage.objects.get(slug="test-article6")

        response = self.client.get(ap.url)
        self.assertNotContains(response, "Quotably interesting", status_code=200)

        # wrong group
        self.client.login(username="testuser1", password="12345")
        response = self.client.get(ap.url)
        self.assertNotContains(response, "Quotably interesting", status_code=200)

        self.client.logout()
        self.client.login(username="testuser2", password="12345")
        response = self.client.get(ap.url)
        self.assertContains(response, "Quotably interesting", status_code=200)

        self.client.logout()
        self.client.login(username="testuser4", password="12345")
        response = self.client.get(ap.url)
        self.assertContains(response, "Quotably interesting", status_code=200)

    def test_invisible_to_specific_group(self):
        # sourcery skip: extract-duplicate-method
        settings = {
            "visibility": "exclude-groups",
            "visibility_groups": "Group22",
        }

        self.createArticlePage(title="Test Article6", settings=settings)

        ap = ArticlePage.objects.get(slug="test-article6")

        response = self.client.get(ap.url)
        self.assertNotContains(response, "Quotably interesting", status_code=200)

        # wrong group
        self.client.login(username="testuser1", password="12345")
        response = self.client.get(ap.url)
        self.assertContains(response, "Quotably interesting", status_code=200)

        self.client.logout()
        self.client.login(username="testuser2", password="12345")
        response = self.client.get(ap.url)
        self.assertNotContains(response, "Quotably interesting", status_code=200)
