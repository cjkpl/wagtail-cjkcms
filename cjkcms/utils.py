from django.utils.html import strip_tags
from django.utils.safestring import mark_safe


def get_richtext_preview(content, max_length=200):
    """Returns a shortened version of a richtext field's content,
    with HTML tags stripped, and trimmed to max_length.
    >>> get_richtext_preview('<h1><div>Hello </div>world</h1>')
    'Hello world'
    >>> get_richtext_preview('Hi worl\x64')
    'Hi world'"""
    # strip tags
    c = strip_tags(content)
    # truncate and add ellipses
    preview = f"{c[:max_length]}..." if len(c) > 200 else c
    return mark_safe(preview)
