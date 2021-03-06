from django.db import models
from django.utils import timezone
import math

from notifications.models import NotifySubscribersModel


class Topic(NotifySubscribersModel):
    """
    Definition of a news Topic.
    """
    published_at = models.DateTimeField(auto_now_add=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    ranking = models.FloatField(default=0)

    @property
    def title(self):
        return (self.article_set.all()[0].headline
                if self.article_set.count() > 0 else '')

    @staticmethod
    def update_rankings():
        '''Returns a number which ranks topics based on their age and number of
        views. A higher share of views (relative to the views of all topics)
        positively affects the ranking of the topic while an old age
        negatively affects it.

        The negative contribution of the age increases exponentially,
        while the positive contribution of views is linear, scaled such that:
        - A one-week old topic which has solely been viewed has a ranking of 1
        - A brand new topic which has never been viewed also has a ranking of 1

        A scaling constant of 0.01 in the exponential is used to stretch the
        age falloff. Age is counted in hours.'''

        total_views = Topic.total_topic_views()

        for topic in Topic.objects.all():
            age = (
                timezone.now() - topic.published_at
            ).total_seconds() / 60 / 60
            share_of_views = (
                topic.views / total_views
                if total_views > 0 else 0
            )
            topic.ranking = (1 + math.exp(0.01 * 24 * 7) *
                             share_of_views - math.exp(0.01 * age) +
                             topic.source_count)
            topic.save()

    @property
    def source_count(self):
        return len(set([article.source for article in self.article_set.all()]))

    @property
    def article_images(self):
        return [article.url_image for article in self.article_set.all()]

    def __str__(self):
        return self.title

    @staticmethod
    def total_topic_views():
        return sum(topic.views for topic in Topic.objects.all())

    class Meta:
        ordering = ["-ranking"]


class Tag(NotifySubscribersModel):
    name = models.TextField(max_length=20)
    topics = models.ManyToManyField(Topic)
    topic_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-topic_count"]


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
    description = models.CharField(max_length=1000, blank=True, null=True)
    content = models.TextField()
    content_len = models.PositiveIntegerField()
    url = models.URLField(max_length=500)
    url_image = models.URLField(max_length=500, blank=True, null=True)
    published_at = models.DateTimeField(null=True)

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, null=True)

    bias = models.FloatField(default=-1)

    def save(self, *args, **kwargs):
        self.content_len = len(self.content)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.headline

    def update_bias(self, new_bias):
        if self.bias < 0:
            self.bias = new_bias
        else:
            self.bias = (self.bias + new_bias) / 2

        self.save()

    class Meta:
        ordering = ["bias"]
