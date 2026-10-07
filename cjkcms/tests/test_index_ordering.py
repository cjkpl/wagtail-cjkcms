from django.test import TestCase
from wagtail.models import Page

from cjkcms.models import Classifier, ClassifierTerm
from cjkcms.models.cms_models import ArticleIndexPage, ArticlePage


class IndexClassifierOrderingTests(TestCase):
    """Child pages can be ordered by the terms of a classifier."""

    def setUp(self):
        home_page = Page.objects.get(path="00010001")
        self.classifier = Classifier.objects.create(name="Priority")
        self.high, self.medium, self.low = (
            ClassifierTerm.objects.create(
                classifier=self.classifier, name=name, sort_order=sort_order
            )
            for sort_order, name in enumerate(("High", "Medium", "Low"))
        )
        other = Classifier.objects.create(name="Other")
        self.other_term = ClassifierTerm.objects.create(
            classifier=other, name="Unrelated", sort_order=0
        )
        self.index = ArticleIndexPage(
            title="Index",
            slug="index",
            index_order_by_classifier=self.classifier,
            index_order_by="title",
        )
        home_page.add_child(instance=self.index)

    def add_article(self, title, *terms):
        article = ArticlePage(title=title, slug=title.lower())
        article.classifier_terms = list(terms)
        self.index.add_child(instance=article)
        return article

    def child_titles(self):
        return [page.title for page in self.index.get_index_children()]

    def test_children_follow_term_order(self):
        self.add_article("Low", self.low)
        self.add_article("High", self.high)
        self.add_article("Medium", self.medium)

        self.assertEqual(self.child_titles(), ["High", "Medium", "Low"])

    def test_child_with_several_terms_of_the_classifier(self):
        self.add_article("Low", self.low)
        self.add_article("Both", self.medium, self.low)
        self.add_article("High", self.high)

        # A page is placed by the first of its terms, and listed once.
        self.assertEqual(self.child_titles(), ["High", "Both", "Low"])
        # SQLite tolerates a subquery returning several rows, PostgreSQL does not.
        self.assertIn("LIMIT 1", str(self.index.get_index_children().query))

    def test_terms_of_other_classifiers_are_ignored(self):
        self.add_article("Second", self.other_term, self.low)
        self.add_article("First", self.other_term, self.high)

        self.assertEqual(self.child_titles(), ["First", "Second"])
