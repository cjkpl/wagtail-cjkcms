from cjkcms.blocks.base_blocks import BaseBlock
from wagtail import blocks
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta, timezone
import re


def convert_to_utc(naive_dt, utc_offset_str):
    # Parse the UTC offset string (e.g., "UTC+05:30" or "UTC-02:00")
    match = re.match(r"UTC([+-])(\d{2}):(\d{2})", utc_offset_str)
    if not match:
        raise ValueError("Invalid UTC offset format. Use 'UTC±HH:MM'.")

    sign = match.group(1)
    hours = int(match.group(2))
    minutes = int(match.group(3))

    # Calculate the total offset in minutes
    total_offset = timedelta(hours=hours, minutes=minutes)
    if sign == "-":
        total_offset = -total_offset

    # Create a timezone with the given offset
    tz = timezone(total_offset)

    # Attach the offset to the naive datetime, making it timezone-aware
    aware_local_dt = naive_dt.replace(tzinfo=tz)

    # Convert the timezone-aware datetime to UTC
    utc_dt = aware_local_dt.astimezone(timezone.utc)

    return utc_dt


class CountdownBlock(BaseBlock):
    """
    Display a countdown to a specific date
    """

    title = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Title"),
    )

    start_date = blocks.DateTimeBlock(
        required=True,
        label=_("Start date and time"),
        help_text=_("Format: YYYY-MM-DD HH:MM"),
    )

    timezone = blocks.CharBlock(
        required=True,
        default="UTC",
        max_length=255,
        label=_("Timezone"),
        help_text=_("Timezone relative to UTC, e.g. UTC+01:00"),
    )

    url = blocks.URLBlock(
        max_length=255,
        label=_("Link"),
        required=False,
        help_text=_("Optional link"),
    )

    # hide_after_end_date = blocks.BooleanBlock(
    #     required=False,
    #     default=False,
    #     label=_("Hide after end date"),
    #     help_text=_("Hide this after end date, or show zeros if false"),
    # )

    theme = blocks.ChoiceBlock(
        choices=[
            ("light", _("Light")),
            ("dark", _("Dark")),
            ("cyber", _("Cyberpunk")),
            ("losange", _("Losange")),
            ("circle", _("Circle")),
            # ("flipbook", _("Flipbook")),
        ],
        default="light",
        label=_("Theme"),
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        sd = value.get("start_date")

        naive_datetime = datetime(
            sd.year, sd.month, sd.day, sd.hour, sd.minute
        )  # Naive datetime

        tz = value.get("timezone")
        if tz == "UTC" or tz == "":
            tz = "UTC+00:00"

        utc_offset_string = tz  # String containing UTC offset
        utc = convert_to_utc(naive_datetime, utc_offset_string)

        # print(naive_datetime, utc, utc_offset_string)
        context["year"] = utc.year
        context["month"] = utc.month
        context["day"] = utc.day
        context["hour"] = utc.hour
        context["minute"] = utc.minute
        context["second"] = 0
        return context

    class Meta:
        template = "cjkcms/blocks/countdown.html"
        icon = "history"
        label = "Countdown"
        ordering = ["start_date"]
        label_format = _("Countdown to {start_date}")
