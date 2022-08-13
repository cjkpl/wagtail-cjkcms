import json

from datetime import timedelta
from urllib import request as urllib_request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request

from django.utils import timezone

from wagtail.embeds.exceptions import EmbedNotFoundException

from wagtail.embeds.finders.oembed import OEmbedFinder
from django.conf import settings


class OEmbedFinderWithReferer(OEmbedFinder):
    def find_embed(self, url, max_width=None, max_height=None):
        # Find provider
        endpoint = self._get_endpoint(url)
        if endpoint is None:
            raise EmbedNotFoundException

        # Work out params
        params = self.options.copy()
        params["url"] = url
        params["format"] = "json"
        params["referrerpolicy"] = "origin"
        if max_width:
            params["maxwidth"] = max_width
        if max_height:
            params["maxheight"] = max_height

        # Perform request
        request = Request(f"{endpoint}?{urlencode(params)}")
        request.add_header("User-agent", "Mozilla/5.0")
        # add referer to request header
        request.add_header("referer", settings.BASE_URL)
        try:
            r = urllib_request.urlopen(request)
            oembed = json.loads(r.read().decode("utf-8"))
        except (URLError, json.decoder.JSONDecodeError) as e:
            raise EmbedNotFoundException from e

        # Convert photos into HTML
        if oembed["type"] == "photo":
            html = '<img src="%s" alt="">' % (oembed["url"],)
        elif oembed["type"] == "video":
            html = oembed.get("html")
            # add referrerpolicty in front of iframe
            html = html[:7] + ' referrerpolicy="origin"' + html[7:]
        else:
            html = oembed.get("html")

        print(html)

        result = {
            "title": oembed.get("title", ""),
            "author_name": oembed.get("author_name", ""),
            "provider_name": oembed.get("provider_name", ""),
            "type": oembed["type"],
            "thumbnail_url": oembed.get("thumbnail_url"),
            "width": oembed.get("width"),
            "height": oembed.get("height"),
            "html": html,
        }

        try:
            cache_age = int(oembed["cache_age"])
        except (KeyError, TypeError, ValueError):
            pass
        else:
            result["cache_until"] = timezone.now() + timedelta(seconds=cache_age)

        return result
