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

    def test_bias_percentage_has_to_be_valid(self):
        data = {
            "owner": self.u.id,
            "article": 'article-detail',
            "bias": -1,
        }

        serializer = ArticleReactionSerializer(data=data)
        self.assertRaises(
            ValidationError,
            serializer.is_valid,
            {'raise_exception': True}
        )

        data["bias"] = 101

        serializer = ArticleReactionSerializer(data=data)
        self.assertRaises(
            ValidationError,
            serializer.is_valid,
            {'raise_exception': True}
        )
