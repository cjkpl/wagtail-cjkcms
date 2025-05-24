"""
Blocks for StreamField content
"""

from django import forms
from django.template.loader import render_to_string
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.models import Collection
from taggit.models import Tag
from wagtail.coreutils import resolve_model_string
from wagtail.documents.blocks import DocumentChooserBlock

from cjkcms.settings import cms_settings
from cjkcms.utils import can_show_block


class ClassifierTermChooserBlock(blocks.FieldBlock):
    """
    Enables choosing a ClassifierTerm in the streamfield.
    Lazy loads the target_model from the string to avoid recursive imports.
    """

    widget = forms.Select
    _help_text = _("Choose a Classifier Term")

    def __init__(self, required=False, label=None, help_text=None, *args, **kwargs):
        self._required = required
        if help_text:
            self._help_text = help_text
        self._label = label
        super().__init__(*args, **kwargs)

    @cached_property
    def target_model(self):
        return resolve_model_string("cjkcms.ClassifierTerm")

    @cached_property
    def field(self):
        return forms.ModelChoiceField(
            queryset=self.target_model.objects.all().order_by(  # type: ignore
                "classifier__name", "name"
            ),
            widget=self.widget,
            required=self._required,
            label=self._label,
            help_text=self._help_text,
        )

    def to_python(self, value):
        """
        Convert the serialized value back into a python object.
        """
        if isinstance(value, int):
            try:
                return self.target_model.objects.get(pk=value)
            except self.target_model.DoesNotExist:
                return None
        return value

    def get_prep_value(self, value):
        """
        Serialize the model in a form suitable for wagtail's JSON-ish streamfield
        """
        return value.pk if isinstance(value, self.target_model) else value


class CollectionChooserBlock(blocks.FieldBlock):
    """
    Enables choosing a wagtail Collection in the streamfield.
    """

    target_model = Collection
    widget = forms.Select
    _help_text = _("Choose a collection")

    def __init__(self, required=False, label=None, help_text=None, *args, **kwargs):
        self._required = required
        if help_text:
            self._help_text = help_text
        self._label = label
        super().__init__(*args, **kwargs)

    @cached_property
    def field(self):
        return forms.ModelChoiceField(
            queryset=self.target_model.objects.all().order_by("name"),
            widget=self.widget,
            required=self._required,
            label=self._label,
            help_text=self._help_text,
        )

    def to_python(self, value):
        """
        Convert the serialized value back into a python object.
        """
        if isinstance(value, int):
            return self.target_model.objects.get(pk=value)
        return value

    def get_prep_value(self, value):
        """
        Serialize the model in a form suitable for wagtail's JSON-ish streamfield
        """
        return value.pk if isinstance(value, self.target_model) else value


class TagChooserBlock(blocks.FieldBlock):
    """
    Enables choosing a wagtail Tag in the streamfield.
    """

    target_model = Tag
    widget = forms.Select
    _help_text = _("Choose a tag")

    def __init__(self, required=False, label=None, help_text=None, *args, **kwargs):
        self._required = required
        if help_text:
            self._help_text = help_text
        self._label = label
        super().__init__(*args, **kwargs)

    @cached_property
    def field(self):
        return forms.ModelChoiceField(
            queryset=self.target_model.objects.all().order_by("name"),
            widget=self.widget,
            required=self._required,
            label=self._label,
            help_text=self._help_text,
        )

    def to_python(self, value):
        """
        Convert the serialized value back into a python object.
        """
        if isinstance(value, int):
            return self.target_model.objects.get(pk=value)
        return value

    def get_prep_value(self, value):
        """
        Serialize the model in a form suitable for wagtail's JSON-ish streamfield
        """
        return value.pk if isinstance(value, self.target_model) else value


class ButtonMixin(blocks.StructBlock):
    """
    Standard style and size options for buttons.
    """

    button_title = blocks.CharBlock(
        max_length=255,
        required=True,
        label=_("Button Title"),
    )
    button_style = blocks.ChoiceBlock(
        choices=cms_settings.CJKCMS_FRONTEND_BTN_STYLE_CHOICES,
        default=cms_settings.CJKCMS_FRONTEND_BTN_STYLE_DEFAULT,
        required=False,
        label=_("Button Style"),
    )
    button_size = blocks.ChoiceBlock(
        choices=cms_settings.CJKCMS_FRONTEND_BTN_SIZE_CHOICES,
        default=cms_settings.CJKCMS_FRONTEND_BTN_SIZE_DEFAULT,
        required=False,
        label=_("Button Size"),
    )
    visible_for = blocks.ChoiceBlock(
        choices=cms_settings.CJKCMS_AUTH_VISIBILITY_CHOICES,
        default=cms_settings.CJKCMS_AUTH_VISIBILITY_DEFAULT,
        required=False,
        label=_("Item visibility"),
    )


class CjkcmsAdvSettings(blocks.StructBlock):
    """
    Common fields each block should have,
    which are hidden under the block's "Advanced Settings" dropdown.
    """

    # placeholder, real value get set in __init__()
    custom_template = blocks.Block()

    force_theme = blocks.ChoiceBlock(
        choices=[
            (None, _("None")),
            ("light", _("Light")),
            ("dark", _("Dark")),
        ],
        default=None,
        required=False,
        label=_("Force Theme"),
        help_text=_(
            "Override the theme for this block, also adding bg-body and text-body classes."
        ),
    )

    custom_css_class = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Custom CSS Class"),
    )

    item_css_class = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Item CSS Class"),
        help_text=_("Used for multi-item blocks, like galleries or lists."),
    )

    custom_id = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Custom ID"),
    )

    visibility = blocks.ChoiceBlock(
        choices=cms_settings.CJKCMS_AUTH_VISIBILITY_CHOICES,
        default=cms_settings.CJKCMS_AUTH_VISIBILITY_DEFAULT,
        required=False,
        label=_("Item visibility"),
        help_text=_("Who can see this block?"),
    )

    visibility_groups = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Visibility Groups"),
        help_text=_(
            "Include or exclude these groups. Use comma to separate multiple groups."
        ),
    )

    visible_from = blocks.DateTimeBlock(required=False, label=_("Visible from"))

    visible_to = blocks.DateTimeBlock(required=False, label=_("Visible to"))

    class Meta:
        form_template = "wagtailadmin/block_forms/base_block_settings_struct.html"
        label = _("Advanced Settings")

    def __init__(self, local_blocks=None, template_choices=None, **kwargs):
        if not local_blocks:
            local_blocks = ()

        local_blocks += (
            (
                "custom_template",
                blocks.ChoiceBlock(
                    choices=template_choices,
                    default=None,
                    required=False,
                    label=_("Template"),
                ),
            ),
        )

        super().__init__(local_blocks, **kwargs)


class CjkcmsAdvTrackingSettings(CjkcmsAdvSettings):
    """
    CjkcmsAdvSettings plus additional tracking fields.
    """

    ga_tracking_event_category = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Tracking Event Category"),
    )
    ga_tracking_event_label = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Tracking Event Label"),
    )


class CjkcmsAdvColumnSettings(CjkcmsAdvSettings):
    """
    BaseBlockSettings plus additional column fields.
    """

    column_breakpoint = blocks.ChoiceBlock(
        choices=cms_settings.CJKCMS_FRONTEND_COL_BREAK_CHOICES,
        default=cms_settings.CJKCMS_FRONTEND_COL_BREAK_DEFAULT,
        required=False,
        verbose_name=_("Column Breakpoint"),
        help_text=_(
            "Screen size at which the column will expand horizontally or stack vertically."
        ),  # noqa
    )


class BaseBlock(blocks.StructBlock):
    """
    Common attributes for all blocks used in the CMS.
    """

    # subclasses can override this to determine the advanced settings class
    advsettings_class = CjkcmsAdvSettings

    # placeholder, real value get set in __init__() from advsettings_class
    settings = blocks.Block()

    def __init__(self, local_blocks=None, **kwargs):
        """
        Construct and inject settings block, then initialize normally.
        """
        klassname = self.__class__.__name__.lower()
        choices = cms_settings.CJKCMS_FRONTEND_TEMPLATES_BLOCKS.get(
            "*", []
        ) + cms_settings.CJKCMS_FRONTEND_TEMPLATES_BLOCKS.get(klassname, [])

        if not local_blocks:
            local_blocks = ()

        local_blocks += (
            ("settings", self.advsettings_class(template_choices=choices)),
        )

        super().__init__(local_blocks, **kwargs)

    def render(self, value, context=None):
        template = value["settings"]["custom_template"] or self.get_template(
            context=context
        )
        if not template:
            return self.render_basic(value, context=context)
        if context is None:
            new_context = self.get_context(value)
        else:
            new_context = self.get_context(value, parent_context=dict(context))

        visibility = value["settings"]["visibility"]
        visibility_groups = value["settings"]["visibility_groups"]
        visible_from = value["settings"]["visible_from"]
        visible_to = value["settings"]["visible_to"]
        if not can_show_block(
            context, visibility, visibility_groups, visible_from, visible_to
        ):
            return ""

        return mark_safe(render_to_string(template, new_context))


class BaseLayoutBlock(BaseBlock):
    """
    Common attributes for all blocks used in the CMS.
    """

    # Subclasses can override this to provide a default list of blocks for the content.
    content_streamblocks = []

    def __init__(self, local_blocks=None, **kwargs):
        if not local_blocks and self.content_streamblocks:
            local_blocks = self.content_streamblocks

        if local_blocks:
            local_blocks = (
                ("content", blocks.StreamBlock(local_blocks, label=_("Content"))),
            )

        super().__init__(local_blocks, **kwargs)


class LinkStructValue(blocks.StructValue):
    """
    Generates a URL for blocks with multiple link choices.
    """

    @property
    def url(self):
        page = self.get("page_link")
        doc = self.get("doc_link")
        ext = self.get("other_link")
        if page and ext:
            return "{0}{1}".format(page.url, ext)
        elif page:
            return page.url
        elif doc:
            return doc.url
        else:
            return ext


class BaseLinkBlock(BaseBlock):
    """
    Common attributes for creating a link within the CMS.
    """

    page_link = blocks.PageChooserBlock(
        required=False,
        label=_("Page link"),
    )
    doc_link = DocumentChooserBlock(
        required=False,
        label=_("Document link"),
    )
    other_link = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Other link"),
    )

    advsettings_class = CjkcmsAdvTrackingSettings

    class Meta:
        value_class = LinkStructValue
