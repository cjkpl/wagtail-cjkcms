import hashlib
import urllib.parse

from django.template import Library
from wagtail.core.models import Site

from cjkcms.models import GeneralSettings

register = Library()


@register.simple_tag
def gravatar_url(email, size=80, default_url=None):
    """
    Returns gravatar url for:
    - email
    - with a specific image size
    - with a default image url, if email-hash not found in gravatar db
    """
    if default_url:
        d_url = default_url
    else:
        site = Site.objects.filter(is_default_site=True)[0]
        d_gravatar = GeneralSettings.for_site(site).gravatar
        d_url = d_gravatar.get_rendition("original").url if d_gravatar else ""

    gravatar_url = (
        "https://www.gravatar.com/avatar/"
        + hashlib.md5(email.lower().encode("utf-8")).hexdigest()
        + "?"
    )
    gravatar_url += urllib.parse.urlencode({"s": str(size), "d": d_url})
    return gravatar_url


@register.simple_tag
def gravatar(email, size=80, default_url=None, options=""):
    url = gravatar_url(email, size, default_url)
    return '<img src="%s" width="%s" height="%s" %s >' % (url, size, size, options)
