"""
Layout blocks are essentially a wrapper around content.
e.g. rows, columns, hero units, etc.
"""

from cjkcms.blocks.base_blocks import BaseLayoutBlock, CjkcmsAdvColumnSettings
from cjkcms.settings import cms_settings
from django.utils.translation import gettext_lazy as _
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

# Level 1 layout blocks


class ColumnBlock(BaseLayoutBlock):
    """
    Renders content in a column.
    """

    column_size = blocks.ChoiceBlock(
        choices=cms_settings.CJKCMS_FRONTEND_COL_SIZE_CHOICES,
        default=cms_settings.CJKCMS_FRONTEND_COL_SIZE_DEFAULT,
        required=False,
        label=_("Column size"),
    )

    advsettings_class = CjkcmsAdvColumnSettings

    class Meta:
        template = "cjkcms/blocks/column_block.html"
        icon = "placeholder"
        label = _("Column")
        label_format = _("Column")


class GridBlock(BaseLayoutBlock):
    """
    Renders a row of columns.
    """

    fluid = blocks.BooleanBlock(
        required=False,
        label=_("Full width"),
    )

    class Meta:
        template = "cjkcms/blocks/grid_block.html"
        icon = "fa-columns"
        label = _("Responsive Grid Row")
        label_format = _("Responsive Grid Row")

    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(local_blocks=[("content", ColumnBlock(local_blocks))])


class CardGridBlock(BaseLayoutBlock):
    """
    Renders a row of cards.
    """

    fluid = blocks.BooleanBlock(
        required=False,
        label=_("Full width"),
    )

    class Meta:
        template = "cjkcms/blocks/cardgrid_deck.html"
        icon = "fa-th-large"
        label = _("Card Grid")
        label_format = _("Card Grid")


class HeroBlock(BaseLayoutBlock):
    """
    Wrapper with color and image background options.
    """

    fluid = blocks.BooleanBlock(
        required=False,
        default=True,
        label=_("Full width"),
    )
    is_parallax = blocks.BooleanBlock(
        required=False,
        label=_("Parallax Effect"),
        help_text=_(
            "Background images scroll slower than foreground images, creating an illusion of depth."
        ),  # noqa
    )
    background_image = ImageChooserBlock(required=False)
    tile_image = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_("Tile background image"),
    )
    background_color = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Background color"),
        help_text=_("Hexadecimal, rgba, or CSS color notation (e.g. #ff0011)"),
    )
    foreground_color = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Text color"),
        help_text=_("Hexadecimal, rgba, or CSS color notation (e.g. #ff0011)"),
    )

    class Meta:
        template = "cjkcms/blocks/hero_block.html"
        icon = "fa-newspaper-o"
        label = "Hero Unit"
