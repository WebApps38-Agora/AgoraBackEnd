from django.test import TestCase
from django.contrib.auth.models import User

from facts.models import Fact, FactReaction
from topics.models import Topic

class FactTest(TestCase):

    def setUp(self):
        self.t = Topic()
        self.t.save()

        self.u1 = User(username="1")
        self.u1.save()

        self.u2 = User(username="2")
        self.u2.save()

    def test_fact_score(self):
        fact = Fact(content="Some Fact", topic=self.t, owner=self.u1)
        fact.save()

        reactions = [None]*3
        reactions[0] = FactReaction(owner=self.u2, fact=fact, is_upvote=True)
        reactions[1] = FactReaction(owner=self.u2, fact=fact, is_upvote=True)
        reactions[2] = FactReaction(owner=self.u2, fact=fact, is_upvote=False)
        for reaction in reactions:
            reaction.save()

        self.assertEqual(fact.score, 1)
