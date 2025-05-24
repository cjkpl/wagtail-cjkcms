from wagtail import blocks
from wagtail.blocks import StructBlock, StreamBlock
from cjkcms.blocks.html_blocks import ButtonBlock
from cjkcms.blocks.base_blocks import BaseBlock
from cjkcms.settings import cms_settings


class BootstrapColorChoiceBlock(blocks.ChoiceBlock):

    class Meta:
        label = "Color"


class InstructionBlock(StructBlock):
    header = blocks.CharBlock(
        label="Header",
        required=False,
    )

    pill_label = blocks.CharBlock(
        label="Pill button Label",
        help_text="Used only in Vertical Pills layout",
    )

    content_1 = blocks.RichTextBlock(
        icon="font",
        features=cms_settings.CJKCMS_RICHTEXT_FEATURES["full"],
        label="Content Section 1",
        required=False,
    )

    content_2 = blocks.RichTextBlock(
        icon="font",
        features=cms_settings.CJKCMS_RICHTEXT_FEATURES["full"],
        label="Content Section 2",
        required=False,
    )

    buttons = StreamBlock(
        [("button", ButtonBlock())],
        label="Step Buttons",
        required=False,
        block_counts={"button": {"min_num": 0, "max_num": 3}},
    )

    class Meta:
        icon = "plus"
        label = "Step"
        label_format = "{header} (Step)"


class MultiStepInstructionsBlock(BaseBlock):
    header = blocks.CharBlock(label="Headline", required=False)

    layout = blocks.ChoiceBlock(
        label="Layout",
        choices=[
            ("vertical_pills", "Vertical Pills"),
            ("alternating_cards", "Alternating Cards"),
        ],
        default="alternating_cards",
    )

    alignment = blocks.ChoiceBlock(
        label="Header & Buttons Alignment",
        choices=[
            ("left", "Left"),
            ("right", "Right"),
            ("center", "Center"),
        ],
        default="center",
    )

    # gutter size for content spacing, dropdown choices for intengers 0-5
    content_gutter = blocks.ChoiceBlock(
        label="Content Gutter Size",
        choices=[(str(i), str(i)) for i in range(6)],
        default="3",
        help_text="Horizontal gutter size for content spacing, 0-5",
    )

    steps = StreamBlock(
        [("step", InstructionBlock())],
        label="Steps",
        block_counts={"step": {"min_num": 1, "max_num": 10, "required": True}},
    )

    class Meta:
        icon = "group"
        label = "Multi Step Instructions"
        label_format = "{header} (Multi Step Instructions)"
        template = "cjkcms/blocks/multi_step_instructions.html"
