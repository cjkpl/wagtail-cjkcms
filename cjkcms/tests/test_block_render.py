from datetime import UTC, datetime, timedelta

from django.test import SimpleTestCase

from cjkcms.blocks import QuoteBlock


class CountingQuoteBlock(QuoteBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context_calls = 0

    def get_context(self, value, parent_context=None):
        self.context_calls += 1
        return super().get_context(value, parent_context=parent_context)


class BlockRenderTests(SimpleTestCase):
    """Hidden blocks are skipped before any work is done to render them."""

    def render(self, **settings):
        block = CountingQuoteBlock()
        value = block.to_python(
            {"text": "Quotably interesting", "author": "", "settings": settings}
        )
        return block, block.render(value, context={})

    def test_visible_block_is_rendered(self):
        block, html = self.render(visibility="all")
        self.assertIn("Quotably interesting", html)
        self.assertEqual(block.context_calls, 1)

    def test_hidden_block_does_not_build_context(self):
        tomorrow = datetime.now(tz=UTC) + timedelta(days=1)
        yesterday = datetime.now(tz=UTC) - timedelta(days=1)
        hidden = (
            {"visibility": "hidden"},
            {"visibility": "auth-only"},
            {"visibility": "all", "visible_from": tomorrow.isoformat()},
            {"visibility": "all", "visible_to": yesterday.isoformat()},
        )
        for settings in hidden:
            with self.subTest(settings=settings):
                block, html = self.render(**settings)
                self.assertEqual(html, "")
                self.assertEqual(block.context_calls, 0)
