from datetime import datetime, timezone


def can_show_block(
    context,
    item_visibility: str,
    groups: str,
    visible_from: datetime | None,
    visible_to: datetime | None,
) -> bool:
    """
    Block/item visibility conditional on selection in cms_settings.AUTH_VISIBILITY_CHOICES,
    as well as visible_from and visible_to datetimes.
    """

    if item_visibility == "hidden":
        return False

    now = datetime.now(timezone.utc)

    if visible_from and visible_from > now:
        return False

    if visible_to and visible_to < now:
        return False

    if item_visibility == "all":
        return True

    # if context is None or "request" not in context:
    #     is_auth = False
    # else:
    try:
        is_auth = context["request"].user.is_authenticated
    except (KeyError, TypeError):
        is_auth = False

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
