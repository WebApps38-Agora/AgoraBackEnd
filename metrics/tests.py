from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.serializers import ValidationError

from metrics.models import Reaction
from metrics.serializers import ReactionSerializer
from topics.models import Article, Source, Topic


class ReactionSerializerTest(TestCase):

    def setUp(self):
        p = Source(name="Test Paper")
        p.save()
        self.t = Topic(title="Test Topic")
        self.t.save()
        self.a = Article(headline="Test", url="http://test.com", source=p)
        self.a.save()
        self.a.topics.add(self.t)
        self.u = User(username="test")
        self.u.save()

        reaction = Reaction(
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

        serializer = ReactionSerializer()

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

        serializer = ReactionSerializer()

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

        serializer = ReactionSerializer()

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

        serializer = ReactionSerializer()

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

        serializer = ReactionSerializer()

        try:
            serializer.validate(data)
        except ValidationError:
            self.fail("Reactions to diff. content should be valid")
