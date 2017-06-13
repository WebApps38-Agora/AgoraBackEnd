from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.serializers import ValidationError

from metrics.models import ArticleReaction
from metrics.serializers import ArticleReactionSerializer
from metrics.views import ArticleMetricsViewSet
from topics.models import Article, Source, Topic


class ArticleReactionSerializerTest(TestCase):

    def setUp(self):
        p = Source(name="Test Paper")
        p.save()
        self.t = Topic()
        self.t.save()
        self.a = Article(headline="Test", url="http://test.com", source=p)
        self.a.save()
        self.a.topic = self.t
        self.u = User(username="test")
        self.u.save()

    def test_cant_react_to_article_twice(self):
        data = {
            "owner": self.u.id,
            "article": reverse(
                'article-detail', args=[self.a.id]
            ),
            "bias_percent": 33.33,
            "fact_percent": 33.33,
            "fake_percent": 33.34,
        }

        serializer = ArticleReactionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer = ArticleReactionSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_sum_of_percent_has_to_add_up_to_100(self):
        data = {
            "owner": self.u.id,
            "article": reverse(
                'article-detail', args=[self.a.id]
            ),
            "bias_percent": 10.33,
            "fact_percent": 33.33,
            "fake_percent": 33.34,
        }

        serializer = ArticleReactionSerializer(data=data)
        self.assertRaises(
            ValidationError,
            serializer.is_valid,
            {'raise_exception': True}
        )


class ArticleMetricsViewSetTest(TestCase):

    def setUp(self):
        p = Source(name="Test Paper")
        p.save()
        self.t = Topic()
        self.t.save()
        self.a = Article(headline="Test", url="http://test.com", source=p)
        self.a.save()
        self.a.topic = self.t
        self.u1 = User(username="test")
        self.u1.save()
        self.u2 = User(username="test2")
        self.u2.save()

    def test_get_object_returns_avg(self):
        ArticleReaction(
            owner=self.u1, article=self.a,
            bias_percent=20, fact_percent=20, fake_percent=60
        ).save()
        ArticleReaction(
            owner=self.u2, article=self.a,
            bias_percent=40, fact_percent=40, fake_percent=20
        ).save()

        view = ArticleMetricsViewSet(kwargs={"article": 1})
        metric = view.get_object()

        self.assertEqual(metric.bias, 30)
        self.assertEqual(metric.fake, 40)
        self.assertEqual(metric.fact, 30)
