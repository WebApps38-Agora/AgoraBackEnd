from django.db import models


class Topic(models.Model):
    """
    Definition of a news Topic.
    """
    title = models.CharField(max_length=140)
    date = models.DateField(auto_now_add=True)


class Source(models.Model):
    """
    A news outlet. Can be used to collect metrics and group articles.
    """
    id = models.CharField(primary_key=True, max_length=30)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)


class Article(models.Model):
    url = models.URLField()

    headline = models.CharField(max_length=140)
    description = models.CharField(max_length=1000, blank=True)
    content = models.TextField()
    content_len = models.PositiveIntegerField()
    url = models.URLField()
    url_image = models.URLField()

    topics = models.ManyToManyField(Topic)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.content_len = len(self.content)
        super().save(*args, **kwargs)
