from copy import copy

from django import forms
from wagtail.admin.panels import TabbedInterface


class CjkcmsPageFormMixin:
    """Resolve dynamic choices after the site's custom form has initialized."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, choices in self.instance.get_instance_field_choices().items():
            if name not in self.fields:
                continue
            field = self.fields[name]
            if not isinstance(field, forms.ChoiceField):
                # custom_template is stored as a CharField without model choices.
                # Retain form customizations and validators when making it a select.
                widget = field.widget
                if not isinstance(widget, (forms.Select, forms.HiddenInput)):
                    widget = forms.Select(attrs=widget.attrs)
                field = forms.TypedChoiceField(
                    required=field.required,
                    label=field.label,
                    help_text=field.help_text,
                    initial=field.initial,
                    disabled=field.disabled,
                    localize=field.localize,
                    error_messages=field.error_messages,
                    validators=field.validators,
                    widget=widget,
                    coerce=str,
                )
                self.fields[name] = field
            model_field = copy(self.instance._meta.get_field(name))
            model_field.choices = choices
            field.choices = model_field.get_choices(include_blank=True)


class CjkcmsTabbedInterface(TabbedInterface):
    def get_form_class(self):
        # Wrap the generated form, preserving the site's base_form_class and
        # its clean/save methods instead of requiring a new form superclass.
        form_class = super().get_form_class()
        return type(form_class.__name__, (CjkcmsPageFormMixin, form_class), {})
