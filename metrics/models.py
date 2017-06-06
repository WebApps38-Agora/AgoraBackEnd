from django.contrib.auth.models import User
from django.db import models

from topics.models import Article, Topic


class Reaction(models.Model):
    """
    Base abstract class for reactions
    """
    article = models.ForeignKey(Article)
    topic = models.ForeignKey(Topic)
    owner = models.ForeignKey(User)

    class Meta:
        abstract = True


class HighlightedReaction(Reaction):
    """
    Reaction to an highlighted piece of text from an article
    """
    location = models.IntegerField()
    content = models.TextField()
    content_end = models.PositiveIntegerField()

    REACTION_CHOICES = (
        (1, "Bias"),
        (2, "Fact"),
        (3, "Fake"),
    )

    reaction = models.IntegerField(choices=REACTION_CHOICES)
    comment = models.CharField(max_length=140, blank=True)


class ArticleReaction(Reaction):
    """
    Article wide reaction. Sum of fields should equal 100
    """
    bias_percent = models.FloatField()
    fact_percent = models.FloatField()
    fake_percent = models.FloatField()

    class Meta:
        unique_together = ("owner", "article")
