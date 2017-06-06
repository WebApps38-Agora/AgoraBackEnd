from django.db import models
from django.utils import timezone
import math

class Topic(models.Model):
    """
    Definition of a news Topic.
    """
    published_at = models.DateTimeField(auto_now_add=True, blank=True)
    views = models.PositiveIntegerField(default=0)

    @property
    def title(self):
        return self.article_set.all()[0].headline if self.article_set.count() > 0 else ''

    @property
    def ranking(self):
        '''Returns a number which ranks topics based on their age and number of
        views. A higher share of views (relative to the views of all topics)
        positively affects the ranking of the topic while an old age
        negatively affects it.

        The negative contribution of the age increases exponentially,
        while the positive contribution of views is a linear, scaled
        such that a 1 week old topic which has solely been viewed has a ranking
        of 0.

        A scaling constant of 0.01 in the exponential is used to stretch the
        age falloff. Age is counted in hours.'''

        age = (timezone.now() - self.published_at).total_seconds() / 60
        total_views = Topic.total_topic_views()
        share_of_views = self.views / total_views if total_views > 0 else 0

        return math.exp(0.01 * 24 * 7) * share_of_views - math.exp(0.01 * age)

    @staticmethod
    def total_topic_views():
        return sum(topic.views for topic in Topic.objects.all())


class Source(models.Model):
    """
    A news outlet. Can be used to collect metrics and group articles.
    """
    id = models.CharField(primary_key=True, max_length=30)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    url = models.URLField(max_length=500)
    url_logo = models.URLField(max_length=500)


class Article(models.Model):
    headline = models.CharField(max_length=140)
    description = models.CharField(max_length=1000, blank=True)
    content = models.TextField()
    content_len = models.PositiveIntegerField()
    url = models.URLField(max_length=500)
    url_image = models.URLField(max_length=500)
    published_at = models.DateTimeField(null=True)

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.content_len = len(self.content)
        super().save(*args, **kwargs)
