from django.contrib.auth.models import User
from django.db import models


class Notification(models.Model):
    users = models.ManyToManyField(User)
    timestamp = models.DateTimeField(auto_now=True)
    link = models.URLField(max_length=500)
    content = models.CharField(max_length=140)
    seen = models.BooleanField(default=False)


def notify_users(users, link, content):
    """
    Given a list of users, notify all of them
    """
    notification = Notification(link=link, content=content)
    notification.save()

    notification.users.add(*users)
