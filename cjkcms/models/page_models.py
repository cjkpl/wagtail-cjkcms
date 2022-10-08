"""
Base and abstract pages used in Cjk CMS.

Based on CODEREDCMS
"""

import logging
from datetime import datetime
from typing import Optional, TYPE_CHECKING

# import geocoder
from django import forms
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db import models
from django.utils.translation import gettext_lazy as _

# from eventtools.models import BaseEvent, BaseOccurrence
# from icalendar import Event as ICalEvent
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.core.fields import StreamField
from wagtail.core.models import PageBase, Page
from wagtail.core.utils import resolve_model_string
from wagtail.images import get_image_model_string
from wagtail.search import index
from wagtail.utils.decorators import cached_classmethod
from wagtailcache.cache import WagtailCacheMixin
from wagtailseo.models import SeoMixin, TwitterCard

from cjkcms import utils
from cjkcms.blocks import (
    CONTENT_STREAMBLOCKS,
    LAYOUT_STREAMBLOCKS,
)

from cjkcms.models.snippet_models import ClassifierTerm
from cjkcms.models.wagtailsettings_models import (
    LayoutSettings,
)

from cjkcms.settings import cms_settings
from cjkcms.widgets import ClassifierSelectWidget

if TYPE_CHECKING:
    from wagtail.images.models import AbstractImage

logger = logging.getLogger("cjkcms")


CJKCMS_PAGE_MODELS = []


def get_page_models():
    return CJKCMS_PAGE_MODELS


class CjkcmsPageMeta(PageBase):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        if "search_template" not in dct:
            cls.search_template = "cjkcms/pages/search_result.html"
        if not cls._meta.abstract:  # type: ignore
            CJKCMS_PAGE_MODELS.append(cls)


class CjkcmsTag(TaggedItemBase):
    class Meta:
        verbose_name = _("CMS Tag")

    content_object = ParentalKey("cjkcms.CjkcmsPage", related_name="tagged_items")


class CjkcmsPage(WagtailCacheMixin, SeoMixin, Page, metaclass=CjkcmsPageMeta):  # type: ignore
    """
    General use page with caching, templating, and SEO functionality.
    All pages should inherit from this.
    """

    class Meta:
        verbose_name = _("CjkCMS Page")

    # Do not allow this page type to be created in wagtail admin
    is_creatable = False

    # Templates
    # The page will render the following templates under certain conditions:
    #
    # template = ''
    # ajax_template = ''
    # search_template = ''

    ###############
    # Content fields
    ###############

    cover_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Cover image"),
    )

    ###############
    # Index fields
    ###############

    # Subclasses can override this to enabled index features by default.
    index_show_subpages_default = False

    # Subclasses can override this to query on a specific
    # page model, rather than the default wagtail Page.
    index_query_pagemodel = "cjkcms.CjkcmsPage"

    # Subclasses can override these fields to enable custom
    # ordering based on specific subpage fields.
    index_order_by_default = ""
    index_order_by_choices = (
        ("", _("Default Ordering")),
        ("-first_published_at", _("Date first published, newest to oldest")),
        ("first_published_at", _("Date first published, oldest to newest")),
        ("-last_published_at", _("Date updated, newest to oldest")),
        ("last_published_at", _("Date updated, oldest to newest")),
        ("title", _("Title, alphabetical")),
        ("-title", _("Title, reverse alphabetical")),
    )
    index_show_subpages = models.BooleanField(
        default=index_show_subpages_default, verbose_name=_("Show list of child pages")
    )
    index_order_by_classifier = models.ForeignKey(
        "cjkcms.Classifier",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Order child pages by classifier"),
        help_text=_(
            "Child pages will first be sorted following the order of this "
            "classifier’s terms (from Snippets > Classifiers)."
        ),
    )
    index_order_by = models.CharField(
        max_length=255,
        choices=index_order_by_choices,
        default=index_order_by_default,
        blank=True,
        verbose_name=_("Order child pages by"),
    )
    index_num_per_page = models.PositiveIntegerField(
        default=10,
        verbose_name=_("Number per page"),
    )
    index_classifiers = ParentalManyToManyField(
        "cjkcms.Classifier",
        blank=True,
        verbose_name=_("Filter child pages by"),
        help_text=_("Enable filtering child pages by these classifiers."),
    )

    ###############
    # Layout fields
    ###############

    custom_template = models.CharField(
        blank=True, max_length=255, choices=None, verbose_name=_("Template")
    )

    ###############
    # SEO overrides
    ###############

    seo_image_sources = [
        "og_image",
        "cover_image",
    ]

    ###############
    # Classify
    ###############

    classifier_terms = ParentalManyToManyField(
        "cjkcms.ClassifierTerm",
        blank=True,
        verbose_name=_("Classifiers"),
        help_text=_(
            "Categorize and group pages together with classifiers. "
            "Used to organize and filter pages across the site."
        ),  # noqa
    )
    tags = ClusterTaggableManager(
        through=CjkcmsTag,
        blank=True,
        verbose_name=_("Tags"),
        help_text=_("Used to organize pages across the site."),
    )

    ###############
    # Search
    ###############

    search_fields = Page.search_fields + [
        index.SearchField("seo_title", partial_match=True, boost=2),
        index.SearchField("search_description", boost=2),
        index.FilterField("index_show_subpages"),
        index.FilterField("index_order_by"),
        index.FilterField("custom_template"),
        index.FilterField("classifier_terms"),
    ]

    ###############
    # Panels
    ###############

    content_panels = Page.content_panels + [
        FieldPanel("cover_image"),
    ]

    body_content_panels = []

    bottom_content_panels = []

    classify_panels = [
        FieldPanel("classifier_terms", widget=ClassifierSelectWidget()),
        FieldPanel("tags"),
    ]

    layout_panels = [
        MultiFieldPanel([FieldPanel("custom_template")], heading=_("Visual Design")),
        MultiFieldPanel(
            [
                FieldPanel("index_show_subpages"),
                FieldPanel("index_num_per_page"),
                FieldPanel("index_order_by_classifier"),
                FieldPanel("index_order_by"),
                FieldPanel("index_classifiers", widget=forms.CheckboxSelectMultiple()),
            ],
            heading=_("Show Child Pages"),
        ),
    ]

    promote_panels = SeoMixin.seo_meta_panels + SeoMixin.seo_struct_panels

    integration_panels = []

    def __init__(self, *args, **kwargs):
        """
        Inject custom choices and defaults into the form fields
        to enable customization by subclasses.
        """
        super().__init__(*args, **kwargs)
        klassname = self.__class__.__name__.lower()
        template_choices = cms_settings.CJKCMS_FRONTEND_TEMPLATES_PAGES.get(
            "*", []
        ) + cms_settings.CJKCMS_FRONTEND_TEMPLATES_PAGES.get(klassname, [])

        self._meta.get_field("index_order_by").choices = self.index_order_by_choices  # type: ignore
        self._meta.get_field("custom_template").choices = template_choices  # type: ignore
        if not self.id:  # type: ignore
            self.index_order_by = self.index_order_by_default
            self.index_show_subpages = self.index_show_subpages_default

    @classmethod
    def get_panels(cls):  # sourcery skip: instance-method-first-arg-name
        panels = [
            ObjectList(
                cls.content_panels
                + cls.body_content_panels
                + cls.bottom_content_panels,
                heading=_("Content"),
            ),
            ObjectList(cls.classify_panels, heading=_("Classify")),
            ObjectList(cls.layout_panels, heading=_("Layout")),
            ObjectList(cls.promote_panels, heading=_("SEO"), classname="seo"),
            ObjectList(
                cls.settings_panels, heading=_("Settings"), classname="settings"
            ),
        ]

        if cls.integration_panels:
            panels.append(
                ObjectList(
                    cls.integration_panels,
                    heading="Integrations",
                    classname="integrations",
                )
            )
        return panels

    @cached_classmethod
    def get_edit_handler(cls):  # sourcery skip: instance-method-first-arg-name
        """
        Override to "lazy load" the panels overridden by subclasses.
        """
        panels = cls.get_panels()  # override e.g. by appending new panels
        edit_handler = TabbedInterface(panels)
        return edit_handler.bind_to_model(cls)

    @property
    def seo_logo(self) -> "Optional[AbstractImage]":
        # sourcery skip: assign-if-exp, or-if-exp-identity, use-named-expression
        """
        Gets logo for structured data using a fallback.
        Override method in SeoMixin.
        Gets the primary logo of the organization.
        """

        logo = super().seo_logo
        if logo:
            return logo
        layout_settings = LayoutSettings.for_site(self.get_site())
        if layout_settings.logo:
            return layout_settings.logo
        return None

    @property
    def seo_image(self) -> "Optional[AbstractImage]":
        """
        Override method in SeoMixin.
        Fallback to logo if opengraph image is not specified.
        """
        img = super().seo_image
        return self.seo_logo if img is None else img

    @property
    def seo_twitter_card_content(self) -> str:
        """
        Override of method in SeoMixin.
        Show a large twitter card if the page has an image set.
        """
        if self.seo_image:
            return TwitterCard.LARGE.value
        return self.seo_twitter_card.value

    def get_template(self, request, *args, **kwargs):
        """
        Override parent to serve different templates based on querystring.
        """
        return self.custom_template or super().get_template(request, args, kwargs)

    def get_index_children(self):
        """
        Returns query of subpages as defined by `index_` variables.
        """
        if self.index_query_pagemodel:
            querymodel = resolve_model_string(
                self.index_query_pagemodel, self._meta.app_label
            )
            query = querymodel.objects.child_of(self).live()  # type: ignore
        else:
            query = self.get_children().live()  # type: ignore

        # Determine query sorting order.
        order = []

        # To sort by term order of a specific classifier, annotate the child
        # pages with the `sort_order` of its ClassifierTerms.
        if self.index_order_by_classifier:
            terms = ClassifierTerm.objects.filter(
                classifier=self.index_order_by_classifier,
                # Reverse ManyToMany of `cjkcmspage.classifier_terms`.
                cjkcmspage=models.OuterRef("pk"),
            )
            query = query.annotate(
                term_sort_order=models.Subquery(terms.values("sort_order"))
            )
            order.append("term_sort_order")

        # Second, order by the specified model attribute.
        if self.index_order_by:
            order.append(self.index_order_by)

        # Order the query.
        if order:
            query = query.order_by(*order)

        return query

    def get_context(self, request, *args, **kwargs):
        """
        Add child pages and paginated child pages to context.
        """
        context = super().get_context(request)

        if self.index_show_subpages:
            # Get child pages
            all_children = self.get_index_children()
            # Filter by classifier terms if applicable
            if len(request.GET) > 0 and self.index_classifiers.exists():
                # Look up comma separated ClassifierTerm slugs i.e. `/?c=term1-slug,term2-slug`
                terms = []
                get_c = request.GET.get("c", None)
                if get_c:
                    terms = get_c.split(",")
                # Else look up individual querystrings i.e. `/?classifier-slug=term1-slug`
                else:
                    for classifier in self.index_classifiers.all().only("slug"):
                        get_term = request.GET.get(classifier.slug, None)
                        if get_term:
                            terms.append(get_term)
                if len(terms) > 0:
                    selected_terms = ClassifierTerm.objects.filter(slug__in=terms)
                    context["selected_terms"] = selected_terms
                    if len(selected_terms) > 0:
                        try:
                            for term in selected_terms:
                                all_children = all_children.filter(
                                    classifier_terms=term
                                )
                        except AttributeError:
                            logger.warning(
                                "Tried to filter by ClassifierTerm, but <%s.%s ('%s')>.get_index_children() did not return a queryset or is not a queryset of CjkcmsPage models.",  # noqa
                                self._meta.app_label,
                                self.__class__.__name__,
                                self.title,
                            )
            paginator = Paginator(all_children, self.index_num_per_page)
            pagenum = request.GET.get("p", 1)
            try:
                paged_children = paginator.page(pagenum)
            except (PageNotAnInteger, EmptyPage, InvalidPage) as e:  # noqa
                paged_children = paginator.page(1)

            context["index_paginated"] = paged_children
            context["index_children"] = all_children
        return context


###############################################################################
# Abstract pages providing pre-built common website functionality, suitable for subclassing.
# These are abstract so subclasses can override fields if desired.
###############################################################################


class CjkcmsWebPage(CjkcmsPage):
    """
    Provides a body and body-related functionality.
    This is abstract so that subclasses can override the body StreamField.
    """

    class Meta:
        verbose_name = _("CMS Web Page")
        abstract = True

    template = "cjkcms/pages/web_page.html"

    # Child pages should override based on what blocks they want in the body.
    # Default is LAYOUT_STREAMBLOCKS which is the fullest editor experience.

    body = StreamField(LAYOUT_STREAMBLOCKS, null=True, blank=True, use_json_field=True)

    # Search fields
    search_fields = CjkcmsPage.search_fields + [index.SearchField("body")]

    # Panels
    body_content_panels = [
        FieldPanel("body"),
    ]

    @property
    def body_preview(self):
        """
        A shortened version of the body without HTML tags.
        """
        return utils.get_richtext_preview(self.body)


class CjkcmsArticlePage(CjkcmsWebPage):
    """
    Article, suitable for news or blog content.
    """

    class Meta:
        verbose_name = _("CMS Article")
        abstract = True

    template = "cjkcms/pages/article_page.html"

    # Override body to provide simpler content
    body = StreamField(CONTENT_STREAMBLOCKS, null=True, blank=True, use_json_field=True)

    caption = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Caption"),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Author"),
    )
    author_display = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Display author as"),
        help_text=_("Override how the author’s name displays on this article."),
    )
    date_display = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Display publish date"),
    )

    def seo_author(self) -> str:
        """
        Override of method in SeoMixin.
        Gets author name using a fallback.
        """
        if self.author_display:
            return self.author_display
        if self.author:
            return self.author.get_full_name()
        return self.owner.get_full_name() if self.owner else ""

    @property
    def seo_published_at(self) -> datetime:
        """
        Override of method in SeoMixin.
        Gets published date.
        """
        return self.date_display or self.first_published_at

    @property
    def seo_description(self) -> str:
        """
        Override of method in SeoMixin.
        Gets the description using a fallback.
        """
        return self.search_description or self.caption or self.body_preview or ""

    search_fields = CjkcmsWebPage.search_fields + [
        index.SearchField("caption", boost=2),
        index.FilterField("author"),
        index.FilterField("author_display"),
        index.FilterField("date_display"),
    ]

    content_panels = CjkcmsWebPage.content_panels + [
        FieldPanel("caption"),
        MultiFieldPanel(
            [
                FieldPanel("author"),
                FieldPanel("author_display"),
                FieldPanel("date_display"),
            ],
            _("Publication Info"),
        ),
    ]


class CjkcmsArticleIndexPage(CjkcmsWebPage):
    """
    Shows a list of article sub-pages.
    """

    class Meta:
        verbose_name = _("CMS Article Index Page")
        abstract = True

    template = "cjkcms/pages/article_index_page.html"

    index_show_subpages_default = True

    index_order_by_default = "-date_display"
    index_order_by_choices = (
        ("-date_display", "Display publish date, newest first"),
    ) + CjkcmsWebPage.index_order_by_choices

    show_images = models.BooleanField(
        default=True,
        verbose_name=_("Show images"),
    )
    show_captions = models.BooleanField(
        default=True,
    )
    show_meta = models.BooleanField(
        default=True,
        verbose_name=_("Show author and date info"),
    )
    show_preview_text = models.BooleanField(
        default=True,
        verbose_name=_("Show preview text"),
    )

    layout_panels = CjkcmsWebPage.layout_panels + [
        MultiFieldPanel(
            [
                FieldPanel("show_images"),
                FieldPanel("show_captions"),
                FieldPanel("show_meta"),
                FieldPanel("show_preview_text"),
            ],
            heading=_("Child page display"),
        ),
    ]


# !GK events removed from CjkCMS (see Codered CRX if you need them)
# !GK forms removed from CjkCMS (see Codered CRX if you need them)
# !GK location models removed from CjkCMS (see Codered CRX if you need them)
