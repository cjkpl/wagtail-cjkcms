import re

from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

# Elements whose content is code rather than text shown to the reader.
NON_TEXT_ELEMENTS_RE = re.compile(
    r"<(script|style)\b[^>]*>.*?</\1\s*>", re.DOTALL | re.IGNORECASE
)


def get_richtext_preview(content, max_length=200):
    """Returns a shortened version of a richtext field's content,
    with HTML tags stripped, and trimmed to max_length.
    Scripts and styles are left out together with their content.
    >>> get_richtext_preview('<h1><div>Hello </div>world</h1>')
    'Hello world'
    >>> get_richtext_preview('Hi worl\x64')
    'Hi world'
    >>> get_richtext_preview('<p>Hello</p><script>let a = 1;</script>')
    'Hello'"""
    # strip tags
    c = strip_tags(NON_TEXT_ELEMENTS_RE.sub("", str(content)))
    # truncate and add ellipses
    preview = f"{c[:max_length]}..." if len(c) > max_length else c
    return mark_safe(preview)
