from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver


def profile_pic_path(instance, filename):
    return "profile_pics/{}".format(instance.user.username)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)

    MALE = "male"
    FEMALE = "female"

    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
    )

    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True)

    political_x = models.IntegerField(default=0)
    political_y = models.IntegerField(default=0)
    profession = models.CharField(max_length=30, null=True)
    town = models.CharField(max_length=30, null=True)
    country = models.CharField(max_length=30, null=True)

    profile_picture = models.URLField(max_length=500, null=True)


@receiver(
    models.signals.post_save,
    sender=User,
    dispatch_uid="Add blank profile",
)
def add_blank_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        profile = Profile(user=instance)
        profile.save()
        instance.profile = profile
        instance.save()
