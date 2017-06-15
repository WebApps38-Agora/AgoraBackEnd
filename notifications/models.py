from django.contrib.auth.models import User
from django.db import models


class Notification(models.Model):
    users = models.ManyToManyField(User, through="NotifiedUsers")
    timestamp = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=140)

    notification_type = models.CharField(max_length=20)
    relevant_id = models.IntegerField()


class NotifiedUsers(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)


class NotifySubscribersModel(models.Model):
    """
    Mixin for models that can take have subscribers and notify them
    """
    subscribers = models.ManyToManyField(User, related_name="subscriber")

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

        to_notify = self.subscribers.all()

        for to_exclude in exclude:
            to_notify = to_notify.exclude(id=to_exclude.id)

        notification.users.add(*to_notify)

    class Meta:
        abstract = True
