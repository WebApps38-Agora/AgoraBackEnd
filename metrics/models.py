from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models

from topics.models import Article, Topic


class Metric(models.Model):
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

    def save(self, *args, **kwargs):
        """
        Check for overlapping reactions assumes content is going to be correct
        """
        self.content_end = self.location + len(self.content)
        reactions = Metric.objects.filter(
            article=self.article,
            topic=self.topic,
            owner=self.owner,
            reaction=self.reaction,
        )

        overlapping_count = (
            reactions.filter(
                location__gte=self.location,
                location__lt=self.content_end
            ) |
            reactions.filter(
                content_end__lte=self.content_end,
                content_end__gt=self.location
            )
        ).distinct().count()

        if overlapping_count > 0:
            raise ValidationError(
                "Cannot add the same reaction twice to the same text"
            )

        return super().save(args, kwargs)
