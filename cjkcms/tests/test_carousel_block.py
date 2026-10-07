from html.parser import HTMLParser

from django.test import TestCase

from cjkcms.blocks import CarouselBlock
from cjkcms.models import Carousel, CarouselSlide


class TagCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class CarouselBlockTests(TestCase):
    def setUp(self):
        self.carousel = Carousel.objects.create(name="Home")
        for number in (1, 2, 3):
            CarouselSlide.objects.create(
                carousel=self.carousel, sort_order=number, custom_id=f"slide-{number}"
            )

    def render(self):
        block = CarouselBlock()
        value = block.to_python({"carousel": self.carousel.pk, "settings": {}})
        html = block.render(value, context={})
        parser = TagCollector()
        parser.feed(html)
        return html, parser.tags

    def test_indicator_buttons_are_well_formed(self):
        _html, tags = self.render()
        indicators = [
            attrs for tag, attrs in tags if tag == "button" and "data-bs-slide-to" in attrs
        ]

        self.assertEqual(
            [attrs["data-bs-slide-to"] for attrs in indicators], ["0", "1", "2"]
        )
        # Only the first indicator is active, and no tag swallows the next one.
        self.assertEqual(
            [attrs.get("class") for attrs in indicators], ["active", None, None]
        )
        for attrs in indicators:
            self.assertNotIn("<", "".join(attrs))
            self.assertEqual(attrs["data-bs-target"], f"#carousel-{self.carousel.pk}")

    def test_slides_use_custom_id_as_given(self):
        _html, tags = self.render()
        slides = [
            attrs
            for tag, attrs in tags
            if tag == "div" and "carousel-item" in attrs.get("class", "")
        ]

        self.assertEqual(
            [attrs["id"] for attrs in slides], ["slide-1", "slide-2", "slide-3"]
        )
        self.assertIn("active", slides[0]["class"])

    def test_controls_are_well_formed(self):
        html, tags = self.render()

        self.assertNotIn('visually-hidden""', html)
        labels = [attrs for tag, attrs in tags if attrs.get("class") == "visually-hidden"]
        self.assertEqual(len(labels), 2)
