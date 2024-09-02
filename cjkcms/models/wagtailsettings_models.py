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
    github = models.URLField(
        blank=True,
        verbose_name=_("GitHub"),
        help_text=_("Your GitHub page URL"),
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
    pinterset = models.URLField(
        blank=True,
        verbose_name=_("Pinterest"),
        help_text=_("Your Pinterest page URL"),
    )
    tiktok = models.URLField(
        blank=True,
        verbose_name=_("TikTok"),
        help_text=_("Your TikTok account URL"),
    )

    location = models.CharField(
        blank=True,
        max_length=50,
        choices=cms_settings.CJKCMS_SOC_LOCATION_CHOICES,
        default=cms_settings.CJKCMS_SOC_LOCATION_DEFAULT,
        verbose_name=_("Location of social media block"),
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
            self.linkedin,
            self.github,
            self.youtube,
            self.vimeo,
            self.tiktok,
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
                FieldPanel("github"),
                FieldPanel("youtube"),
                FieldPanel("vimeo"),
                FieldPanel("pinterset"),
                FieldPanel("tiktok"),
            ],
            _("Social Media Accounts"),
        ),
        FieldPanel("location"),
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

    default_seo_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="default_seo_image",
        verbose_name=_("Default SEO Image"),
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
        choices=[],
        default="",
        verbose_name=_("Collapse navbar menu"),
        help_text=_(
            "Control on what screen sizes to show and collapse the navbar menu links."
        ),
    )
    navbar_format = models.CharField(
        blank=True,
        max_length=50,
        choices=[],
        default="",
        verbose_name=_("Navbar format"),
    )

    navbar_search = models.BooleanField(
        default=True,
        verbose_name=_("Search box"),
        help_text=_("Show search box in navbar"),
    )

    search_format = models.CharField(
        blank=True,
        max_length=50,
        choices=[],
        default="",
        verbose_name=_("Search format"),
    )

    searchbox_input_class = models.CharField(
        blank=True,
        max_length=255,
        default="border-secondary mb-0",
        verbose_name=_("Searchbox input class"),
        help_text=_("Classes applied to searchbox input"),
    )

    searchbutton_class = models.CharField(
        blank=True,
        max_length=255,
        default="btn btn-outline-secondary",
        verbose_name=_("Search button (with text) class"),
        help_text=_(
            "Classes applied to search button. Add e.g. `fas fa-search` for icon."
        ),
    )

    searchbutton_label = models.CharField(
        blank=True,
        max_length=255,
        default="Search",
        verbose_name=_("Search button label"),
        help_text=_(
            "Leave empty when using icon-only button. Otherwise, add button label."
        ),
    )

    navbar_langselector = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        choices=[],
        default=None,
        verbose_name=_("Language selector"),
        help_text=_("Choose lang choice selector"),
    )

    breadcrumbs = models.BooleanField(
        default=False,
        verbose_name=_("Breadcrumbs"),
        help_text=_("Show breadcrumbs in page header"),
    )

    # # defines layout for the breadcrumb: full, shortened
    # breadcrumb_layout_default = "full"
    # breadcrumb_layout_choices = (
    #     ("full", _("Display full")),
    #     ("shortened_dots", _("Shortened with dots in middle levels")),
    #     ("shortened_mobile_dots", _("Shortened with dots on mobile view")),
    # )

    # breadcrumb_layout = models.CharField(
    #     max_length=255,
    #     choices=breadcrumb_layout_choices,
    #     default=breadcrumb_layout_default,
    #     blank=True,
    #     verbose_name=_("Breadcrumbs layout"),
    # )

    breadcrumb_icon = models.CharField(
        blank=True,
        max_length=32,
        default="slash",
        verbose_name=_("Breadcrumb icon"),
        help_text=_("Bootstrap icon name. See docs for built-in options."),
    )

    color_scheme = models.CharField(
        blank=True,
        max_length=50,
        choices=[],
        default="",
        verbose_name=_("Color scheme"),
        help_text=_("Default light/dark/custom theme. (MD/Bootstrap only)"),  # noqa
    )

    light_dark_switch = models.BooleanField(
        default=False,
        verbose_name=_("Light/Dark switch"),
        help_text=_("Show switch to toggle light/dark theme (MD/Bootstrap only)"),
    )

    frontend_theme = models.CharField(
        blank=True,
        max_length=50,
        choices=[],
        default="",
        verbose_name=_("Theme variant"),
        help_text=cms_settings.CJKCMS_FRONTEND_THEME_HELP,
    )

    awesome_cdn = models.BooleanField(
        default=False,
        verbose_name=_("Font Awesome"),
        help_text=_("Load font awesome from CDN"),
    )

    bootstrap_icons = models.BooleanField(
        default=False,
        verbose_name=_("Bootstrap Icons CSS"),
        help_text=_("Load bootstrap icons css from local/static folder"),
    )

    custom_font = models.BooleanField(
        default=False,
        verbose_name=_("Use custom font"),
        help_text=_("Custom body font e.g. from CDN & include css body override"),
    )

    font_url = models.CharField(
        blank=True,
        max_length=250,
        default=cms_settings.CJKCMS_FONT_URL,
        verbose_name=_("Font URL"),
        help_text=_("Full URL to font css file"),
    )

    font_family = models.CharField(
        blank=True,
        max_length=128,
        default=cms_settings.CJKCMS_FONT_FAMILY,
        verbose_name=_("Font Family"),
        help_text=_("Font family name, e.g. 'Open Sans, sans-serif'"),
    )

    base_template = models.CharField(
        blank=True,
        max_length=200,
        default=cms_settings.CJKCMS_BASE_TEMPLATE_DEFAULT,
        verbose_name=_("Base template"),
        help_text=cms_settings.CJKCMS_BASE_TEMPLATE_HELP,
    )

    articles_show_author = models.BooleanField(
        default=True,
        verbose_name=_("Show author in articles"),
        help_text=_("If disabled, override by filling `display author as` in article"),
    )

    articles_date_format = models.CharField(
        blank=True,
        max_length=200,
        default="Y-m-d",
        verbose_name=_("Date format in articles"),
        help_text=_("Format of the publication date in articles. Set blank to hide."),
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("logo"),
                FieldPanel("favicon"),
                FieldPanel("default_seo_image"),
            ],
            heading=_("Branding"),
            classname="collapsed",
        ),
        InlinePanel(
            "site_navbar",
            help_text=_("Choose one or more navbars"),
            heading=_("Site Navbars"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("navbar_class"),
                FieldPanel("navbar_fixed"),
                FieldPanel("navbar_wrapper_fluid"),
                FieldPanel("navbar_content_fluid"),
                FieldPanel("navbar_collapse_mode"),
                FieldPanel("navbar_format"),
                FieldPanel("navbar_langselector"),
            ],
            heading=_("Site Navbar Layout"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("navbar_search"),
                FieldPanel("search_format"),
                FieldPanel("searchbox_input_class"),
                FieldPanel("searchbutton_class"),
                FieldPanel("searchbutton_label"),
            ],
            heading=_("Search box in navbar"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("breadcrumbs"),
                FieldPanel("breadcrumb_icon"),
            ],
            heading=_("Site Header / Breadcrumbs"),
        ),
        InlinePanel(
            "site_footer",
            help_text=_("Choose one or more footers"),
            heading=_("Site Footers"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("color_scheme"),
                FieldPanel("frontend_theme"),
                FieldPanel("base_template"),
                FieldPanel("awesome_cdn"),
                FieldPanel("bootstrap_icons"),
                FieldPanel("custom_font"),
                FieldPanel("font_url"),
                FieldPanel("font_family"),
            ],
            heading=_("Theming"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("articles_show_author"),
                FieldPanel("articles_date_format"),
            ],
            heading=_("Article Pages"),
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
            "color_scheme"
        ).choices = cms_settings.CJKCMS_FRONTEND_COLOR_SCHEME_CHOICES  # type: ignore
        self._meta.get_field(
            "navbar_format"
        ).choices = cms_settings.CJKCMS_FRONTEND_NAVBAR_FORMAT_CHOICES  # type: ignore
        self._meta.get_field(
            "search_format"
        ).choices = cms_settings.CJKCMS_FRONTEND_SEARCH_FORMAT_CHOICES  # type: ignore
        self._meta.get_field(
            "navbar_langselector"
        ).choices = cms_settings.CJKCMS_LANGUAGE_SELECTOR_CHOICES  # type: ignore
        # Set default dynamically.
        if not self.id:  # type: ignore # if new record / id not yet assigned
            self.frontend_theme = cms_settings.CJKCMS_FRONTEND_THEME_DEFAULT
            self.navbar_class = cms_settings.CJKCMS_FRONTEND_NAVBAR_CLASS_DEFAULT
            self.navbar_collapse_mode = (
                cms_settings.CJKCMS_FRONTEND_NAVBAR_COLLAPSE_MODE_DEFAULT
            )
            self.color_scheme = cms_settings.CJKCMS_FRONTEND_COLOR_SCHEME_DEFAULT
            self.navbar_format = cms_settings.CJKCMS_FRONTEND_NAVBAR_FORMAT_DEFAULT
            self.search_format = cms_settings.CJKCMS_FRONTEND_SEARCH_FORMAT_DEFAULT
            self.base_template = cms_settings.CJKCMS_BASE_TEMPLATE_DEFAULT


class NavbarOrderable(Orderable, models.Model):
    navbar_chooser = ParentalKey(
        LayoutSettings, related_name="site_navbar", verbose_name=_("Site Navbars")
    )  # type: ignore
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
    )  # type: ignore
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
    matomo_hostname = models.CharField(
        blank=True,
        max_length=128,
        verbose_name=_("Hostname (including http(s)://)"),
        help_text=_(
            "Matomo hostname (e.g. https://tracker.com). Without trailing slash."
        ),
    )
    matomo_site_id = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_("Site ID"),
        help_text=_("Numeric site id from Matomo website configuration."),
    )
    matomo_disable_cookies = models.BooleanField(
        default=False,
        verbose_name=_("Disable Matomo Cookies"),
        help_text=_("Disable Matomo cookies. Useful for GDPR compliance."),  # noqa
    )
    # Cookie consent - using https://github.com/orestbida/cookieconsent (MIT license)
    cookie_consent = models.BooleanField(
        default=False,
        verbose_name=_("Enable cookie consent"),
        help_text=_(
            "Enable simple GDPR compliant cookie consent banner. "
            "Intended as a quick solution for sites that don't need a fully customisable consent."
        ),  # noqa
    )
    cookie_consent_deny_btn = models.BooleanField(
        default=False,
        verbose_name=_("Show Accept Necessary"),
        help_text=_(
            "Show an [Accept Necessary Only] button in the cookie consent banner. "
            "If unchecked, the banner will only have an accept and settings buttons."
        ),  # noqa
    )
    privacy_page = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.CASCADE,
        related_name="+",
        blank=True,
        null=True,
        help_text=_(
            "Show a link to selected privacy policy page in cookie consent settings."
        ),
    )

    contact_page = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.CASCADE,
        related_name="+",
        blank=True,
        null=True,
        help_text=_(
            "Show [More info] section with link to selected contact page in cookie consent settings."  # noqa
        ),
    )

    class ConsentModalLayout(models.TextChoices):
        BOX = "box"
        CLOUD = "cloud"
        BAR = "bar"

    consent_modal_layout = models.CharField(
        max_length=6,
        choices=ConsentModalLayout.choices,
        default=ConsentModalLayout.CLOUD,
        help_text=_("Layout of the cookie consent modal"),
    )

    class SettingsModalLayout(models.TextChoices):
        BOX = "box"
        BAR = "bar"

    settings_modal_layout = models.CharField(
        max_length=6,
        choices=SettingsModalLayout.choices,
        default=SettingsModalLayout.BOX,
        help_text=_("Layout of the full cookie consent settings modal."),
    )

    panels = [
        HelpPanel(
            heading=_("Know your tracking"),
            content=_(
                "<h3><b>Which tracking IDs do I need?</b></h3>"
                "<p>Most common choice is Google Analytics - but beware of "
                "GDPR compliance issues!. Matomo is a good alternative, "
                "and can be configured for GDPR compliance.</p>"
            ),
        ),
        MultiFieldPanel(
            [
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
        MultiFieldPanel(
            [
                FieldPanel("matomo_site_id"),
                FieldPanel("matomo_hostname"),
                FieldPanel("matomo_disable_cookies"),
            ],
            heading=_("Matomo Analytics"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("cookie_consent"),
                FieldPanel("cookie_consent_deny_btn"),
                FieldPanel("privacy_page"),
                FieldPanel("contact_page"),
                FieldPanel("consent_modal_layout"),
                FieldPanel("settings_modal_layout"),
            ],
            heading=_("Cookie consent"),
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
            'For example: "sender@example.com" or '
            '"Sender Name <sender@example.com>" (without quotes)'
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
