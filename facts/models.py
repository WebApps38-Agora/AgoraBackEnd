from django.db import models
from django.contrib.auth.models import User
from topics.models import Topic


class Fact(models.Model):
    content = models.CharField(max_length=300)
    topic = models.ForeignKey(Topic)
    owner = models.ForeignKey(User)

    @property
    def score(self):
        score = 0
        for reaction in self.factreaction_set.all():
            score += 1 if reaction.is_upvote else -1
        return score


class FactReaction(models.Model):
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE)
    owner = models.ForeignKey(User)
    is_upvote = models.BooleanField(default=False)
