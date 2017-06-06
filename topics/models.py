from django.db import models


class Topic(models.Model):
    """
    Definition of a news Topic.
    """
    def title(self):
        return self.article_set.all()[0].headline if self.article_set.count() > 0 else ''


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
