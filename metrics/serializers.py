from math import isclose

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from metrics.models import ArticleReaction, HighlightedReaction


class ArticleReactionSerializer(serializers.HyperlinkedModelSerializer):
    # TODO: remove next line when user API implemented
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate(self, data):
        """
        Checks that sum of different fields = 100
        """
        total_sum = (
            data["bias_percent"] + data["fact_percent"] + data["fake_percent"]
        )

        if not isclose(total_sum, 100, rel_tol=1e-5):
            raise serializers.ValidationError(
                "Total percentage of metrics should add up to 100"
            )

        return data

    class Meta:
        model = ArticleReaction
        fields = (
            "article",
            "topic",
            "owner",
            "bias_percent",
            "fact_percent",
            "fake_percent",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=ArticleReaction.objects.all(),
                fields=("owner", "article")
            )
        ]


class HighlightedReactionSerializer(serializers.HyperlinkedModelSerializer):
    # TODO: remove next line when user API implemented
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate(self, data):
        """
        Check for overlapping reactions assumes content is going to be correct
        """
        data["content_end"] = data["location"] + len(data["content"])
        reactions = HighlightedReaction.objects.filter(
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
        model = HighlightedReaction
        fields = (
            "article",
            "topic",
            "owner",
            "location",
            "content",
            "reaction",
            "comment",
        )


class ArticleMetric():
    def __init__(self, bias=None, fact=None, fake=None, opinion=None):
        self.bias = bias or 0
        self.fact = fact or 0
        self.fake = fake or 0


class ArticleMetricsSerializer(serializers.Serializer):
    bias = serializers.IntegerField()
    fact = serializers.IntegerField()
    fake = serializers.IntegerField()
