from django.db import models
from django.contrib.auth.models import User

from notifications.models import NotifySubscribersModel
from topics.models import Topic


class Comment(NotifySubscribersModel):
    topic = models.ForeignKey(Topic)
    owner = models.ForeignKey(User)
    parent_comment = models.ForeignKey('self', null=True, blank=True)

    content = models.CharField(max_length=2000)
    upvotes = models.PositiveIntegerField(default=0)

    published_at = models.DateTimeField(auto_now_add=True, blank=True)
