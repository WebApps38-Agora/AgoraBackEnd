from django.contrib.auth.models import User
from django.db import models


def profile_pic_path(instance, filename):
    return "profile_pics/{}".format(instance.user.username)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    political_x = models.IntegerField()
    political_y = models.IntegerField()
    profession = models.CharField(max_length=30)
    town = models.CharField(max_length=30)
    country = models.CharField(max_length=30)

    profile_picture = models.URLField(max_length=500)
