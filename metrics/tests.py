from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.serializers import ValidationError

from metrics.models import HighlightedReaction
from metrics.serializers import (ArticleReactionSerializer,
                                 HighlightedReactionSerializer)
from topics.models import Article, Source, Topic
from topics.views import ArticleViewSet, TopicViewSet


class HighlightedReactionSerializerTest(TestCase):

    def setUp(self):
        p = Source(name="Test Paper")
        p.save()
        self.t = Topic()
        self.t.save()
        self.a = Article(headline="Test", url="http://test.com", source=p)
        self.a.save()
        self.a.topics.add(self.t)
        self.u = User(username="test")
        self.u.save()

        reaction = HighlightedReaction(
            article=self.a,
            topic=self.t,
            owner=self.u,
            location=0,
            content="This is a test",
            content_end=14,
            reaction=1,
        )
        reaction.save()

    def test_cant_react_to_same_thing_twice(self):
        data = {
            'article': self.a,
            'topic': self.t,
            'owner': self.u,
            'location': 0,
            'content': "This is a test",
            'reaction': 1,
        }

        serializer = HighlightedReactionSerializer()

        self.assertRaises(ValidationError, serializer.validate, data)

    def test_cant_react_to_subset_of_already_reacted(self):
        data = {
            'article': self.a,
            'topic': self.t,
            'owner': self.u,
            'location': 5,
            'content': "is a test",
            'reaction': 1,
        }

        serializer = HighlightedReactionSerializer()

        self.assertRaises(ValidationError, serializer.validate, data)

    def test_cant_react_to_intersection_of_already_reacted(self):
        data = {
            'article': self.a,
            'topic': self.t,
            'owner': self.u,
            'location': 5,
            'content': "is a test too",
            'reaction': 1,
        }

        serializer = HighlightedReactionSerializer()

        self.assertRaises(ValidationError, serializer.validate, data)

    def test_can_react_differently_to_same_text(self):
        data = {
            'article': self.a,
            'topic': self.t,
            'owner': self.u,
            'location': 0,
            'content': "This is a test",
            'reaction': 2,
        }

        serializer = HighlightedReactionSerializer()

        try:
            serializer.validate(data)
        except ValidationError:
            self.fail("Different reactions to same content should be valid")

    def test_can_react_to_disjoint_content(self):
        data = {
            'article': self.a,
            'topic': self.t,
            'owner': self.u,
            'location': 20,
            'content': "This is also a test",
            'reaction': 1,
        }

        serializer = HighlightedReactionSerializer()

        try:
            serializer.validate(data)
        except ValidationError:
            self.fail("HighlightedReactions to diff. content should be valid")


class ArticleReactionSerializerTest(TestCase):

    def setUp(self):
        p = Source(name="Test Paper")
        p.save()
        self.t = Topic()
        self.t.save()
        self.a = Article(headline="Test", url="http://test.com", source=p)
        self.a.save()
        self.a.topics.add(self.t)
        self.u = User(username="test")
        self.u.save()

    def test_cant_react_to_article_twice(self):
        data = {
            "owner": self.u.id,
            "topic": reverse(
                'topic-detail', args=[self.t.id]
            ),
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
            "topic": reverse(
                'topic-detail', args=[self.t.id]
            ),
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
