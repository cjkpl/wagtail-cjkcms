# -*- coding: utf-8 -*-

from django.test import TestCase
from cjkcms.templatetags.gravatar import gravatar_url, gravatar


class GravatarTests(TestCase):
    def test_gravatar_url(self):
        self.assertEqual(
            "https://www.gravatar.com/avatar/738668e0913f0841e3285ca39fa2fc4b?s=80&d=",
            gravatar_url("admin@cjk.pl"),
        )
        self.assertEqual(
            "https://www.gravatar.com/avatar/738668e0913f0841e3285ca39fa2fc4b?s=120&d=",
            gravatar_url("admin@cjk.pl", 120),
        )

    def test_gavatar(self):
        html = '<img src="https://www.gravatar.com/avatar/738668e0913f0841e3285ca39fa2fc4b?s=80&d=" width="80" height="80"  >'  # noqa
        self.assertEqual(html, gravatar(email="admin@cjk.pl"))

        html = '<img src="https://www.gravatar.com/avatar/738668e0913f0841e3285ca39fa2fc4b?s=130&d=" width="130" height="130"  >'  # noqa
        self.assertEqual(html, gravatar(email="admin@cjk.pl", size=130))

        html = '<img src="https://www.gravatar.com/avatar/738668e0913f0841e3285ca39fa2fc4b?s=180&d=" width="180" height="180" class="avatar" >'  # noqa
        self.assertEqual(
            html, gravatar(email="admin@cjk.pl", size=180, options='class="avatar"')
        )


class GravatarWithDefaultGravatarUrlTests(TestCase):
    def test_gravatar_url(self):
        self.assertEqual(
            "https://www.gravatar.com/avatar/738668e0913f0841e3285ca39fa2fc4b?s=80&d=www.foo.com",
            gravatar_url(email="admin@cjk.pl", default_url="www.foo.com"),
        )
        self.assertEqual(
            "https://www.gravatar.com/avatar/738668e0913f0841e3285ca39fa2fc4b?s=120&d=www.foo.com",
            gravatar_url("admin@cjk.pl", 120, "www.foo.com"),
        )

    def test_gavatar(self):
        html = '<img src="https://www.gravatar.com/avatar/738668e0913f0841e3285ca39fa2fc4b?s=80&d=www.foo.com" width="80" height="80"  >'  # noqa
        self.assertEqual(
            html, gravatar(email="admin@cjk.pl", default_url="www.foo.com")
        )

        html = '<img src="https://www.gravatar.com/avatar/738668e0913f0841e3285ca39fa2fc4b?s=130&d=www.foo.com" width="130" height="130"  >'  # noqa
        self.assertEqual(html, gravatar("admin@cjk.pl", 130, "www.foo.com"))

        html = '<img src="https://www.gravatar.com/avatar/738668e0913f0841e3285ca39fa2fc4b?s=180&d=www.foo.com" width="180" height="180" class="avatar" >'  # noqa
        self.assertEqual(
            html, gravatar("admin@cjk.pl", 180, "www.foo.com", 'class="avatar"')
        )


# @TODO: add test to verify that an image added in wagtail backend/settings gets used as default
