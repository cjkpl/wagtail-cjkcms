from django.utils.html import format_html
from wagtail import blocks
from wagtail.blocks import StructBlock, StructValue, StreamBlock, PageChooserBlock


# class CustomPropertyStructValue(StructValue):
#     def something(self):
#         pass


class ButtonsBlock(StructBlock):
    label = blocks.CharBlock(
        label="Label (Displayed Text)", classname="collapsible collapsed"
    )
    internal_page_link = PageChooserBlock(
        label="Link to the Page",
        required=False,
        help_text=format_html(
            "Remember that <strong>Link to the Page</strong> always takes precedence over <strong>Link to the External "
            "Website</strong>, so if both fields are completed, the system will use the former value. "
        ),
    )
    external_link = blocks.CharBlock(
        label="Link to the External Website", required=False
    )

    class ColorChoiceBlock(blocks.ChoiceBlock):
        choices = [
            ("primary", "Primary (Blue)"),
            ("secondary", "Secondary (Grey)"),
            ("success", "Success (Green)"),
            ("danger", "Danger (Red)"),
            ("warning", "Warning (Yellow)"),
            ("info", "Info (Light Blue)"),
            ("light", "Light (White)"),
            ("dark", "Dark (Black))"),
        ]

        class Meta:
            label = "Button Color"

    color = ColorChoiceBlock(
        required=False,
        default="primary",
        help_text=(
            format_html(
                "If you leave this field blank, the button "
                "will be displayed in the default, blue colour. "
            ),
        ),
    )

    class Meta:
        icon = "plus"


class StepButton(StreamBlock):
    button = ButtonsBlock(label="Button")

    class Meta:
        icon = "plus"
        label = "Step Button"
        block_counts = {"button": {"min_num": 0, "max_num": 3, "required": False}}


class SimpleRichTextBlock(blocks.RichTextBlock):
    """RichText Without (Limited) All the Features."""

    def __init__(
        self, required=True, help_text=None, editor="default", features=None, **kwargs
    ):
        super().__init__(**kwargs)
        # self.features = ["bold", "italic", "link"]

    class Meta:
        icon = "edit"
        label = "Simple RichText"


class InstructionBlock(StructBlock):
    label = blocks.CharBlock(
        label="Button Label",
        help_text=format_html(
            "This label will only be visible when the <strong>Vertical Pills</strong> option in the <strong>Layout & "
            "Styling</strong> section is selected. "
        ),
    )
    header = blocks.CharBlock(
        label="Header",
    )
    content = SimpleRichTextBlock()

    step_button = StepButton(required=False)

    class Meta:
        icon = "plus"


class InstructionContainerBlock(StreamBlock):
    instruction = InstructionBlock(label="Step")

    class Meta:
        icon = "plus"
        block_counts = {"instruction": {"min_num": 1, "max_num": 10, "required": True}}


class MultiStepInstructionsBlock(StructBlock):
    class IsMultiStepInstructionsVisibleChoiceBlock(blocks.ChoiceBlock):
        choices = [(True, "Yes"), (False, "No")]

        class Meta:
            label = "Are Multi Step Instructions Visible?"
            default = True

    is_multi_step_instructions_visible = IsMultiStepInstructionsVisibleChoiceBlock(
        default="True", help_text=format_html("<hr>" "<br>")
    )

    class MultiStepInstructionsLightDarkToggleChoiceBlock(blocks.ChoiceBlock):
        choices = [("dark", "Dark"), ("light", "Light")]

        class Meta:
            label = "Light/Dark Mode"

    multi_step_instructions_light_dark_toggle = (
        MultiStepInstructionsLightDarkToggleChoiceBlock(default="Dark")
    )

    headline = blocks.CharBlock(label="Headline")

    class IsHeadlineVisibleChoiceBlock(blocks.ChoiceBlock):
        choices = [(True, "Yes"), (False, "No")]

        class Meta:
            label = "Is Headline Visible?"

    is_headline_visible = IsHeadlineVisibleChoiceBlock(
        default="True", help_text=format_html("<br>")
    )

    class MultiStepInstructionsStylingChoiceBlock(blocks.ChoiceBlock):
        choices = [
            ("vertical_pills", "Vertical Pills"),
            ("sequential_cards", "Sequential Cards"),
        ]

        class Meta:
            label = "Layout"

    multi_step_instructions_styling = MultiStepInstructionsStylingChoiceBlock(
        default="Sequential Cards",
        help_text=format_html(
            "This options will change the layout and styling of the Multi Step Instructions."
            "<br>"
            "<br>"
            "If you choose the "
            "<strong>Sequential Cards</strong> "
            "option, please try also to upload the graphics "
            "into the Rich Text Editor (WYSIWYG) field to "
            "make the layout clear and transparent. "
            "Otherwise, it is more optional as the layout is more responsive."
        ),
    )

    class HeaderButtonsAlignmentChoiceBlock(blocks.ChoiceBlock):
        choices = [
            ("Align to the Left", "Align to the Left"),
            ("Align to the Center", "Align to the Center"),
        ]

        class Meta:
            label = "Alignment of Header & Buttons"

    multi_step_instructions_header_and_buttons_alignment = HeaderButtonsAlignmentChoiceBlock(
        default="Align to the Left",
        help_text=format_html(
            "Please note that if you want to align the text and image as well, you will need to do this with the "
            "<strong>Rich Text Editor</strong> (WYSIWYG). "
        ),
    )

    class LeadingColorChoiceBlock(blocks.ChoiceBlock):
        choices = [
            ("primary", "Primary (Blue)"),
            ("secondary", "Secondary (Grey)"),
            ("success", "Success (Green)"),
            ("danger", "Danger (Red)"),
            ("warning", "Warning (Yellow)"),
            ("info", "Info (Light Blue)"),
            ("light", "Light (White)"),
            ("dark", "Dark (Black))"),
        ]

        class Meta:
            label = "Leading Color"

    leading_color = LeadingColorChoiceBlock(
        required=False,
        default="primary",
        help_text=(
            format_html(
                "If you leave this field blank, blue colour will be set as the default."
                "<br> <br>"
            ),
        ),
    )

    instruction = InstructionContainerBlock(label="Instruction")

    class Meta:
        icon = "group"
        label = "Multi Step Instructions"
        template = "cjkcms/blocks/multi_step_instructions.html"
        # value_class = CustomPropertyStructValue
