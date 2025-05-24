from wagtail import blocks
from wagtail.blocks import StructBlock, StreamBlock
from cjkcms.blocks.html_blocks import ButtonBlock
from cjkcms.blocks.base_blocks import BaseBlock
from cjkcms.settings import cms_settings

# Shared color choices for reuse
BOOTSTRAP_COLOR_CHOICES = [
    ("primary", "Primary (Blue)"),
    ("secondary", "Secondary (Grey)"),
    ("success", "Success (Green)"),
    ("danger", "Danger (Red)"),
    ("warning", "Warning (Yellow)"),
    ("info", "Info (Light Blue)"),
    ("light", "Light (White)"),
    ("dark", "Dark (Black))"),
]


class BootstrapColorChoiceBlock(blocks.ChoiceBlock):
    choices = BOOTSTRAP_COLOR_CHOICES

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

    theme = blocks.ChoiceBlock(
        label="Theme", choices=[("dark", "Dark"), ("light", "Light")], default="dark"
    )

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

    leading_color = BootstrapColorChoiceBlock(
        required=False,
        default="primary",
        help_text="Defaults to primary (blue)",
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
