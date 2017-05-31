from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from metrics.models import Metric
from topics.models import Article, Paper, Topic


class MetricTest(TestCase):

    def setUp(self):
        p = Paper(name="Test Paper")
        p.save()
        self.t = Topic(title="Test Topic")
        self.t.save()
        self.a = Article(headline="Test", url="http://test.com", paper=p)
        self.a.save()
        self.a.topics.add(self.t)
        self.u = User(username="test")
        self.u.save()

        reaction = Metric(
            article=self.a,
            topic=self.t,
            owner=self.u,
            location=0,
            content="This is a test",
            reaction=1,
        )
        reaction.save()

    def test_cant_react_to_same_thing_twice(self):
        reaction = Metric(
            article=self.a,
            topic=self.t,
            owner=self.u,
            location=0,
            content="This is a test",
            reaction=1,
        )

        self.assertRaises(ValidationError, reaction.save)

    def test_cant_react_to_subset_of_already_reacted(self):
        reaction = Metric(
            article=self.a,
            topic=self.t,
            owner=self.u,
            location=5,
            content="is a test",
            reaction=1,
        )

        self.assertRaises(ValidationError, reaction.save)

    def test_cant_react_to_interesction_of_already_reacted(self):
        reaction = Metric(
            article=self.a,
            topic=self.t,
            owner=self.u,
            location=10,
            content="test test",
            reaction=1,
        )

        self.assertRaises(ValidationError, reaction.save)

    def test_can_react_differently_to_same_text(self):
        reaction = Metric(
            article=self.a,
            topic=self.t,
            owner=self.u,
            location=0,
            content="This is a test",
            reaction=2,
        )
        reaction.save()

        self.assertEqual(Metric.objects.all().count(), 2)

    def test_can_react_to_disjoint_content(self):
        reaction = Metric(
            article=self.a,
            topic=self.t,
            owner=self.u,
            location=20,
            content="This is also test",
            reaction=1,
        )
        reaction.save()

        self.assertEqual(Metric.objects.all().count(), 2)
