from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from datetime import datetime, timezone
import pytz


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


def can_show_block(
    context, item_visibility: str, groups: str, visible_from, visible_to
) -> bool:
    """
    Block/item visibility conditional on selection in cms_settings.AUTH_VISIBILITY_CHOICES
    """

    if item_visibility == "hidden":
        return False

    time_ok = True
    if visible_from:
        time_ok = time_ok and visible_from <= datetime.now(timezone.utc)
    if visible_to:
        time_ok = time_ok and visible_to >= datetime.now(timezone.utc)

    # if time range does not allow showing, everything else is irrelevant
    if not time_ok:
        return False

    if item_visibility == "all":
        return True

    try:
        is_auth = context["request"].user.is_authenticated
    except KeyError:
        return False

    if not is_auth:
        return item_visibility == "non-auth-only"

    # here is_auth is True
    if item_visibility == "auth-only":
        return True

    # group include or exclude
    if item_visibility not in ["include-groups", "exclude-groups"]:
        return False

    groups_list = [word.strip() for word in groups.split(",")]
    user_in_group = context["request"].user.groups.filter(name__in=groups_list).exists()

    return (item_visibility == "include-groups" and user_in_group) or (
        item_visibility == "exclude-groups" and not user_in_group
    )
