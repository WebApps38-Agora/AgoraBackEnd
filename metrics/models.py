from django.contrib.auth.models import User
from django.db import models

from topics.models import Article, Topic


class Reaction(models.Model):
    article = models.ForeignKey(Article)
    topic = models.ForeignKey(Topic)
    owner = models.ForeignKey(User)

    location = models.IntegerField()
    content = models.TextField()
    content_end = models.PositiveIntegerField()

    REACTION_CHOICES = (
        (1, "Bias"),
        (2, "Fact"),
        (3, "Fake"),
        (4, "Opinion"),
    )

    reaction = models.IntegerField(choices=REACTION_CHOICES)
    comment = models.CharField(max_length=140, blank=True)
