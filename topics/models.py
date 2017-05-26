from django.db import models


class Topic(models.Model):
    """
    Definition of a news Topic.
    """
    title = models.CharField(max_length=140)
    date = models.DateField(auto_now_add=True)


class Paper(models.Model):
    """
    A newspaper. Can be used to collect metrics and group articles.
    """
    name = models.CharField(max_length=30)


class Article(models.Model):
    headline = models.CharField(max_length=140)
    description = models.CharField(max_length=1000)
    url = models.URLField()

    topics = models.ManyToManyField(Topic)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
