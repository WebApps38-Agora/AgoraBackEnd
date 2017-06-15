from django.db import models
from django.contrib.auth.models import User

from notifications.models import NotifySubscribersModelMixin
from topics.models import Topic


class Comment(NotifySubscribersModelMixin, models.Model):
    topic = models.ForeignKey(Topic)
    owner = models.ForeignKey(User)
    parent_comment = models.ForeignKey('self', null=True, blank=True)

    content = models.CharField(max_length=2000)
    upvotes = models.PositiveIntegerField(default=0)
