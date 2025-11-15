from wagtail.models import Site
from cjkcms.models.wagtailsettings_models import MailchimpApiSettings

import requests


class MailchimpApi:
    user_string = "Website"
    proto_base_url = "https://{0}.api.mailchimp.com/3.0/"
    request_timeout = 5

    def __init__(self, site=None):
        self.set_access_token(site)

    def set_access_token(self, site=None):
        site = site or Site.objects.get(is_default_site=True)
        self.access_token = MailchimpApiSettings.for_site(site).mailchimp_api_key
        if self.access_token:
            self.set_base_url()
            self.is_active = True
        else:
            self.is_active = False

    def set_base_url(self):
        """
        The base url for the mailchimip api is dependent on the api key.
        """
        try:
            _, datacenter = self.access_token.rsplit("-", 1)
        except ValueError:
            self.base_url = None
            self.is_active = False
            return
        self.base_url = self.proto_base_url.format(datacenter)

    def default_headers(self):
        return {
            "Content-Type": "application/json",
        }

    def default_auth(self):
        return self.user_string, self.access_token

    def get_lists(self):
        endpoint = "lists?fields=lists.name,lists.id"
        return self._get(endpoint)

    def get_merge_fields_for_list(self, list_id):
        endpoint = (
            f"lists/{list_id}/merge-fields"
            "?fields=merge_fields.tag,merge_fields.merge_id,merge_fields.name"
        )
        return self._get(endpoint)

    def get_interest_categories_for_list(self, list_id):
        endpoint = (
            f"lists/{list_id}/interest-categories?fields=categories.id,categories.title"
        )
        return self._get(endpoint)

    def get_interests_for_interest_category(self, list_id, interest_category_id):
        endpoint = (
            f"lists/{list_id}/interest-categories/{interest_category_id}/interests"
            "?fields=interests.id,interests.name"
        )
        return self._get(endpoint)

    def add_user_to_list(self, list_id, data):
        endpoint = "lists/{0}".format(list_id)
        return self._post(endpoint, data=data)

    def _request(
        self,
        method,
        endpoint,
        params=None,
        data=None,
        json_data=None,
        auth=None,
        headers=None,
        timeout=None,
        **kwargs,
    ):
        if not getattr(self, "is_active", False) or not getattr(self, "base_url", None):
            raise RuntimeError("Mailchimp API is not configured with a valid key.")
        auth = auth or self.default_auth()
        headers = headers or self.default_headers()
        full_url = f"{self.base_url}{endpoint}"
        timeout = timeout or self.request_timeout
        response = requests.request(
            method,
            full_url,
            params=params,
            data=data,
            json=json_data,
            auth=auth,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )
        response.raise_for_status()
        return response.json()

    def _get(self, endpoint, params=None, **kwargs):
        return self._request("get", endpoint, params=params, **kwargs)

    def _post(self, endpoint, data=None, **kwargs):
        return self._request("post", endpoint, json_data=data, **kwargs)
