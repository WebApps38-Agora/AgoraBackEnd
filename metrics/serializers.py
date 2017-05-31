from django.contrib.auth.models import User
from rest_framework import serializers

from metrics.models import Metric


class MetricSerializer(serializers.HyperlinkedModelSerializer):
    # TODO: remove next line when user API implemented
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate(self, data):
        """
        Check for overlapping reactions assumes content is going to be correct
        """
        data["content_end"] = data["location"] + len(data["content"])
        reactions = Metric.objects.filter(
            article=data["article"],
            topic=data["topic"],
            owner=data["owner"],
            reaction=data["reaction"],
        )

        overlapping_count = (
            reactions.filter(
                location__gte=data["location"],
                location__lt=data["content_end"],
            ) |
            reactions.filter(
                content_end__lte=data["content_end"],
                content_end__gt=data["location"]
            ) |
            reactions.filter(
                location__lte=data["location"],
                content_end__gte=data["content_end"]
            )
        ).count()

        if overlapping_count > 0:
            raise serializers.ValidationError(
                "Cannot add the same reaction twice to the same text"
            )

        return data

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
