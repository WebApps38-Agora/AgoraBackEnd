from django.contrib.auth.models import User
from django.db import models


class Notification(models.Model):
    users = models.ManyToManyField(User)
    timestamp = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=140)
    seen = models.BooleanField(default=False)

    notification_type = models.CharField(max_length=20)
    relevant_id = models.IntegerField()


class NotifySubscribersModelMixin():
    """
    Mixin for models that can take have subscribers and notify them
    """
    subscribers = models.ManyToManyField(User)

    def notify_all(
            self, notification_type, relevant_id, content, exclude=None):
        """
        Notify all subscribers
        """
        exclude = exclude or []
        notification = Notification(
            notification_type=notification_type,
            relevant_id=relevant_id,
            content=content
        )
        notification.save()

        notification.users.add(
            *self.subscribers.all().exclude(user__in=exclude)
        )
