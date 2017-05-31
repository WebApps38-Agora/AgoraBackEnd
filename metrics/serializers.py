from django.contrib.auth.models import User
from rest_framework import serializers

from metrics.models import Metric


class MetricSerializer(serializers.HyperlinkedModelSerializer):
    # TODO: remove next line when user API implemented
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Metric
        fields = (
            "article",
            "topic",
            "owner",
            "location",
            "content",
            "reaction",
            "comment",
        )
