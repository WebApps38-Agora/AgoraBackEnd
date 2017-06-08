from django.db import models
from django.contrib.auth.models import User


class Fact(models.Model):
    content = models.CharField(max_length=300)

    def score(self):
        score = 0
        for reaction in self.reaction_set:
            score += 1 if reaction.is_upvote else -1
        return score


class Reaction(models.Model):
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE)
    user = models.ForeignKey(User)
    is_upvote = models.BooleanField(default=False)
