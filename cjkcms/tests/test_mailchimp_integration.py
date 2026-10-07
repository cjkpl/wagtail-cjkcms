import json
from types import SimpleNamespace

from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.test import SimpleTestCase

from cjkcms.models.integration_models import MailchimpSubscriberIntegration


def render(merge_fields, submission, email_field="{{ email }}"):
    data = {
        "email_field": email_field,
        "merge_fields": merge_fields,
        "interest_categories": {"cat": {"interests": {"abc": True}}},
    }
    integration = SimpleNamespace(
        get_data=lambda: data,
        combine_interest_categories=lambda: (
            MailchimpSubscriberIntegration.combine_interest_categories(integration)
        ),
    )
    return MailchimpSubscriberIntegration.render_dictionary(integration, submission)


class MailchimpMergeFieldTests(SimpleTestCase):
    def test_merge_fields_are_filled_from_submission(self):
        rendered = render(
            {"FNAME": "{{ first_name }}", "CITY": "{{ city|upper }}"},
            {"email": "jane@example.com", "first_name": "Jane", "city": "Gdynia"},
        )
        member = json.loads(rendered)["members"][0]
        self.assertEqual(member["email_address"], "jane@example.com")
        self.assertEqual(member["merge_fields"], {"FNAME": "Jane", "CITY": "GDYNIA"})
        self.assertEqual(member["interests"], {"abc": True})

    def test_merge_fields_can_not_load_tag_libraries(self):
        for library in ("cjkcms_tags", "static", "i18n"):
            with self.subTest(library=library), self.assertRaises(TemplateSyntaxError):
                render({"FNAME": "{% load " + library + " %}"}, {"email": "a@b.pl"})

    def test_merge_fields_can_not_include_templates(self):
        with self.assertRaises(TemplateDoesNotExist):
            render({"FNAME": "{% include 'cjkcms/robots.txt' %}"}, {"email": "a@b.pl"})
