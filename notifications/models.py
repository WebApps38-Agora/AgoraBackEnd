from django.contrib.auth.models import User
from django.db import models


class Notification(models.Model):
    users = models.ManyToManyField(User, through="NotifiedUsers")
    timestamp = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=140)

    notification_type = models.CharField(max_length=20)
    relevant_id = models.IntegerField()


class NotifiedUsers(models.Model):
    id_key = models.AutoField(primary_key=True)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)

    class Meta:
        ordering = ["seen"]


class NotifySubscribersModel(models.Model):
    """
    Mixin for models that can take have subscribers and notify them
    """
    subscribers = models.ManyToManyField(
        User,
        related_name="%(class)s_subscriber",
    )

    def notify_all(
            self, notification_type, relevant_id, content, exclude=None):
        """
        Notify all subscribers
        """
        exclude = exclude or []

        to_notify = self.subscribers.all()

        for to_exclude in exclude:
            to_notify = to_notify.exclude(id=to_exclude.id)

        # If there's no one to notify, terminate
        if to_notify.count() == 0:
            return

        notification = Notification(
            notification_type=notification_type,
            relevant_id=relevant_id,
            content=content
        )
        notification.save()

        for user in to_notify:
            notified = NotifiedUsers(notification=notification, user=user)
            notified.save()

    class Meta:
        abstract = True
