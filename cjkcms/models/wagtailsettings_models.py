"""
Custom wagtail settings, defined per-site
"""

import json

from cjkcms.models.snippet_models import Footer, Navbar
from cjkcms.settings import cms_settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, HelpPanel, InlinePanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.images import get_image_model_string
from wagtail.models import Orderable


@register_setting(icon="group")
class SocialMediaSettings(BaseSiteSetting):
    """
    Social media accounts.
    """

    class Meta:
        verbose_name = _("Social Media")
        app_label = "cjkcms"

    facebook = models.URLField(
        blank=True,
        verbose_name=_("Facebook"),
        help_text=_("Your Facebook page URL"),
    )
    twitter = models.URLField(
        blank=True,
        verbose_name=_("Twitter"),
        help_text=_("Your Twitter page URL"),
    )
    instagram = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Instagram"),
        help_text=_("Your Instagram username, without the @"),
    )
    linkedin = models.URLField(
        blank=True,
        verbose_name=_("LinkedIn"),
        help_text=_("Your LinkedIn page URL"),
    )
    youtube = models.URLField(
        blank=True,
        verbose_name=_("YouTube"),
        help_text=_("Your YouTube channel or user account URL"),
    )
    vimeo = models.URLField(
        blank=True,
        verbose_name=_("Vimeo"),
        help_text=_("Your Vimeo channel or user account URL"),
    )

    @property
    def twitter_handle(self):
        """
        Gets the handle of the twitter account from a URL.
        """
        return self.twitter.strip().strip("/").split("/")[-1]

    @property
    def social_json(self):
        """
        Returns non-blank social accounts as a JSON list.
        """
        socialist = [
            self.facebook,
            self.twitter,
            self.instagram,
            self.youtube,
            self.linkedin,
            self.vimeo,
        ]
        socialist = list(filter(None, socialist))
        return json.dumps(socialist)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("facebook"),
                FieldPanel("twitter"),
                FieldPanel("instagram"),
                FieldPanel("linkedin"),
                FieldPanel("youtube"),
                FieldPanel("vimeo"),
            ],
            _("Social Media Accounts"),
        )
    ]


@register_setting(icon="grip")
class LayoutSettings(ClusterableModel, BaseSiteSetting):
    """
    Branding, navbar, and theme settings.
    """

    class Meta:
        verbose_name = _("Layout")

    logo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Logo"),
        help_text=_("Brand logo used in the navbar and throughout the site"),
    )
    favicon = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="favicon",
        verbose_name=_("Favicon"),
    )
    navbar_color_scheme = models.CharField(
        blank=True,
        max_length=50,
        choices=None,
        default="",
        verbose_name=_("Navbar color scheme"),
        help_text=_(
            "Optimizes text and other navbar elements for use with light or dark backgrounds."
        ),  # noqa
    )
    navbar_class = models.CharField(
        blank=True,
        max_length=255,
        default="",
        verbose_name=_("Navbar CSS class"),
        help_text=_(
            'Custom classes applied to navbar e.g. "bg-light", "bg-dark", "bg-primary".'
        ),
    )
    navbar_fixed = models.BooleanField(
        default=False,
        verbose_name=_("Fixed navbar"),
        help_text=_("Fixed navbar will remain at the top of the page when scrolling."),
    )
    navbar_wrapper_fluid = models.BooleanField(
        default=True,
        verbose_name=_("Full width navbar"),
        help_text=_("The navbar will fill edge to edge."),
    )
    navbar_content_fluid = models.BooleanField(
        default=False,
        verbose_name=_("Full width navbar contents"),
        help_text=_("Content within the navbar will fill edge to edge."),
    )
    navbar_collapse_mode = models.CharField(
        blank=True,
        max_length=50,
        choices=None,
        default="",
        verbose_name=_("Collapse navbar menu"),
        help_text=_(
            "Control on what screen sizes to show and collapse the navbar menu links."
        ),
    )
    navbar_format = models.CharField(
        blank=True,
        max_length=50,
        choices=None,
        default="",
        verbose_name=_("Navbar format"),
    )
    navbar_search = models.BooleanField(
        default=True,
        verbose_name=_("Search box"),
        help_text=_("Show search box in navbar"),
    )

    navbar_langselector = models.BooleanField(
        default=True,
        verbose_name=_("Language selector"),
        help_text=_("Show lang choice dropdown in navbar"),
    )

    frontend_theme = models.CharField(
        blank=True,
        max_length=50,
        choices=None,
        default="",
        verbose_name=_("Theme variant"),
        help_text=cms_settings.CJKCMS_FRONTEND_THEME_HELP,
    )

    awesome_cdn = models.BooleanField(
        default=False,
        verbose_name=_("Font Awesome"),
        help_text=_("Load font awesome from CND"),
    )

    base_template = models.CharField(
        blank=True,
        max_length=200,
        default=cms_settings.CJKCMS_BASE_TEMPLATE_DEFAULT,
        verbose_name=_("Base template"),
        help_text=cms_settings.CJKCMS_BASE_TEMPLATE_HELP,
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("logo"),
                FieldPanel("favicon"),
            ],
            heading=_("Branding"),
        ),
        InlinePanel(
            "site_navbar",
            help_text=_("Choose one or more navbars"),
            heading=_("Site Navbars"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("navbar_color_scheme"),
                FieldPanel("navbar_class"),
                FieldPanel("navbar_fixed"),
                FieldPanel("navbar_wrapper_fluid"),
                FieldPanel("navbar_content_fluid"),
                FieldPanel("navbar_collapse_mode"),
                FieldPanel("navbar_format"),
                FieldPanel("navbar_search"),
                FieldPanel("navbar_langselector"),
            ],
            heading=_("Site Navbar Layout"),
        ),
        InlinePanel(
            "site_footer",
            help_text=_("Choose one or more footers"),
            heading=_("Site Footers"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("frontend_theme"),
                FieldPanel("base_template"),
                FieldPanel("awesome_cdn"),
            ],
            heading=_("Theming"),
        ),
    ]

    def __init__(self, *args, **kwargs):
        """
        Inject custom choices and defaults into the form fields
        to enable customization of settings without causing migration issues.
        """
        super().__init__(*args, **kwargs)
        # Set choices dynamically.
        self._meta.get_field(
            "frontend_theme"
        ).choices = cms_settings.CJKCMS_FRONTEND_THEME_CHOICES  # type: ignore
        self._meta.get_field(
            "navbar_collapse_mode"
        ).choices = cms_settings.CJKCMS_FRONTEND_NAVBAR_COLLAPSE_MODE_CHOICES  # type: ignore
        self._meta.get_field(
            "navbar_color_scheme"
        ).choices = cms_settings.CJKCMS_FRONTEND_NAVBAR_COLOR_SCHEME_CHOICES  # type: ignore
        self._meta.get_field(
            "navbar_format"
        ).choices = cms_settings.CJKCMS_FRONTEND_NAVBAR_FORMAT_CHOICES  # type: ignore
        # Set default dynamically.
        if not self.id:  # type: ignore # if new record / id not yet assigned
            self.frontend_theme = cms_settings.CJKCMS_FRONTEND_THEME_DEFAULT
            self.navbar_class = cms_settings.CJKCMS_FRONTEND_NAVBAR_CLASS_DEFAULT
            self.navbar_collapse_mode = (
                cms_settings.CJKCMS_FRONTEND_NAVBAR_COLLAPSE_MODE_DEFAULT
            )
            self.navbar_color_scheme = (
                cms_settings.CJKCMS_FRONTEND_NAVBAR_COLOR_SCHEME_DEFAULT
            )
            self.navbar_format = cms_settings.CJKCMS_FRONTEND_NAVBAR_FORMAT_DEFAULT
            self.base_template = cms_settings.CJKCMS_BASE_TEMPLATE_DEFAULT


class NavbarOrderable(Orderable, models.Model):
    navbar_chooser = ParentalKey(
        LayoutSettings, related_name="site_navbar", verbose_name=_("Site Navbars")
    )
    navbar = models.ForeignKey(
        Navbar,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("navbar")]


class FooterOrderable(Orderable, models.Model):
    footer_chooser = ParentalKey(
        LayoutSettings, related_name="site_footer", verbose_name=_("Site Footers")
    )
    footer = models.ForeignKey(
        Footer,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("footer")]


@register_setting(icon="history")
class AnalyticsSettings(BaseSiteSetting):
    """
    Tracking and Google Analytics.
    """

    class Meta:
        verbose_name = _("Tracking")

    ga_tracking_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("Universal Analytics Tracking ID"),
        help_text=_(
            'Google Analytics tracking ID (begins with "UA-"). '
            "Note: will stop working by 1 July 2023!"
        ),
    )
    g4_tracking_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("G4 Analytics Tracking ID"),
        help_text=_(
            'G4 Google Analytics tracking ID ("G-..."). If both G4 & UA set, both will be used.'
        ),
    )
    ga_track_button_clicks = models.BooleanField(
        default=False,
        verbose_name=_("Track button clicks"),
        help_text=_(
            "Track all button clicks using Google Analytics event tracking. "
            "Event tracking details can be specified in each button’s advanced settings options."
        ),  # noqa
    )
    gtm_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("Google Tag Manager ID"),
        help_text=_('Begins with "GTM-"'),
    )

    panels = [
        HelpPanel(
            heading=_("Know your tracking"),
            content=_(
                "<h3><b>Which tracking IDs do I need?</b></h3>"
                "<p>Before adding tracking to your site, "
                '<a href="https://docs.coderedcorp.com/wagtail-crx/how_to/add_tracking_scripts.html" '  # noqa
                'target="_blank">read about the difference between UA, G, GTM, '
                "and other tracking IDs</a>.</p>"
            ),
        ),
        MultiFieldPanel(
            [
                FieldPanel("ga_tracking_id"),
                FieldPanel("g4_tracking_id"),
                FieldPanel("ga_track_button_clicks"),
            ],
            heading=_("Google Analytics"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("gtm_id"),
            ],
            heading=_("Google Tag Manager"),
        ),
    ]


@register_setting(icon="cog")
class GeneralSettings(BaseSiteSetting):
    """
    Various site-wide settings. A good place to put
    one-off settings that don't belong anywhere else.
    """

    from_email_address = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("From email address"),
        help_text=_(
            "The default email address this site appears to send from. "
            'For example: "sender@abc.com" or "Sender Name <sender@abc.com>" (without quotes)'
        ),
        # noqa
    )
    search_num_results = models.PositiveIntegerField(
        default=20,
        verbose_name=_("Number of results per page"),
    )
    external_new_tab = models.BooleanField(
        default=False, verbose_name=_("Open all external links in new tab")
    )

    gravatar = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Gravatar Default"),
        help_text=_("Gravatar image when user email not found in gravatar db"),
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("from_email_address"),
            ],
            _("Email"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("search_num_results"),
            ],
            _("Search Settings"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("external_new_tab"),
            ],
            _("Links"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("gravatar"),
            ],
            _("Avatar"),
        ),
    ]

    class Meta:
        verbose_name = _("General")


@register_setting(icon="mail")
class MailchimpApiSettings(BaseSiteSetting):
    """
    Settings for Mailchimp API services.
    """

    class Meta:
        verbose_name = _("Mailchimp API")

    mailchimp_api_key = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("Mailchimp API Key"),
        help_text=_("The API Key used for Mailchimp."),
    )


@register_setting(icon="password")
class AdobeApiSettings(BaseSiteSetting):
    """
    Settings for Adobe PDF Embed services
    """

    adobe_embed_id = models.CharField(
        null=True,
        blank=True,
        max_length=64,
        verbose_name=_("Adobe Embed API ID"),
        help_text=_("Adobe PDF Embed API Client ID"),
    )
