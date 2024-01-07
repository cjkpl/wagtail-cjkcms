import json
import unittest
from unittest.mock import patch, Mock
from urllib.error import URLError
from datetime import timedelta, datetime

from cjkcms.finders.oembed import OEmbedFinderWithReferer
from wagtail.embeds.exceptions import EmbedNotFoundException


class TestOEmbedFinderWithReferer(unittest.TestCase):
    def setUp(self):
        self.finder = OEmbedFinderWithReferer()
        self.url = "http://vimeo.com/video"
        self.endpoint = "http://oembed.com/provider"
        self.oembed_response = {
            "type": "video",
            "html": "<iframe></iframe>",
            "url": "http://example.com/embedded",
            "title": "Example Video",
            "author_name": "Author",
            "provider_name": "Provider",
            "thumbnail_url": "http://vimeo.com/thumbnail.jpg",
            "width": 640,
            "height": 480,
            "cache_age": 3600,
        }

    @patch("urllib.request.urlopen")
    @patch("django.utils.timezone.now")
    def test_find_embed_success(self, mock_now, mock_urlopen):
        # Set a fixed time for the duration of this test
        fixed_time = datetime(2024, 1, 1, 12, 0, 0)
        mock_now.return_value = fixed_time

        # Mocking the response from urlopen
        mock_response = Mock()
        mock_response.read.return_value = json.dumps(self.oembed_response).encode(
            "utf-8"
        )
        mock_urlopen.return_value = mock_response

        # Mocking the _get_endpoint method to return a predefined endpoint
        self.finder._get_endpoint = Mock(return_value=self.endpoint)

        result = self.finder.find_embed(self.url)
        expected_cache_until = fixed_time + timedelta(seconds=3600)
        expected_result = {
            "title": "Example Video",
            "author_name": "Author",
            "provider_name": "Provider",
            "type": "video",
            "thumbnail_url": "http://vimeo.com/thumbnail.jpg",
            "width": 640,
            "height": 480,
            "html": '<iframe referrerpolicy="origin"></iframe>',
            "cache_until": expected_cache_until,
        }
        self.assertEqual(result, expected_result)

    @patch("urllib.request.urlopen")
    def test_find_embed_urlerror(self, mock_urlopen):
        mock_urlopen.side_effect = URLError("Test Error")
        self.finder._get_endpoint = Mock(return_value=self.endpoint)

        with self.assertRaises(EmbedNotFoundException):
            self.finder.find_embed(self.url)
