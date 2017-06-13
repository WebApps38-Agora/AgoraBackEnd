from django.contrib.auth.models import User
from django.db import models

from topics.models import Article


class Reaction(models.Model):
    """
    Base abstract class for reactions
    """
    article = models.ForeignKey(Article)
    owner = models.ForeignKey(User)

    class Meta:
        abstract = True


class ArticleReaction(Reaction):
    """
    Article wide reaction. Sum of fields should equal 100
    """
    bias_percent = models.FloatField()
    fact_percent = models.FloatField()
    fake_percent = models.FloatField()

    class Meta:
        unique_together = ("owner", "article")
