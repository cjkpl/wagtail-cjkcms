# image_formats.py
from django.utils.html import format_html
from wagtail.images.formats import (
    Format,
    register_image_format,
    unregister_image_format,
)


class SurroundingDivImageFormat(Format):
    surrounding_classes = ""

    def __init__(self, name, label, classnames, filter_spec, surrounding_classes=""):
        self.surrounding_classes = surrounding_classes
        super().__init__(name, label, classnames, filter_spec)

    def image_to_html(self, image, alt_text, extra_attributes=None):

        default_html = super().image_to_html(image, alt_text, extra_attributes)

        return format_html(
            f'<div class="{self.surrounding_classes}">{default_html}</div>',
        )


# default left and right does not play well with bootstrap5
unregister_image_format("left")
unregister_image_format("right")

register_image_format(
    SurroundingDivImageFormat(
        "centered",
        "Centered",
        "bodytext-image",
        "width-640",
        surrounding_classes="d-flex justify-content-center",
    )
)

register_image_format(
    SurroundingDivImageFormat(
        "left",
        "Left-justified",
        "bodytext-image",
        "width-640",
        surrounding_classes="d-flex justify-content-start",
    )
)

register_image_format(
    SurroundingDivImageFormat(
        "right",
        "Right-justified",
        "bodytext-image",
        "width-640",
        surrounding_classes="d-flex justify-content-end",
    )
)

register_image_format(
    Format(
        "thumb-left",
        "Left-floating thumbnail",
        "bodytext-image float-start me-2",
        "width-200",
    )
)

register_image_format(
    Format(
        "thumb-right",
        "Right-floating thumbnail",
        "bodytext-image float-end ms-2",
        "width-200",
    )
)
