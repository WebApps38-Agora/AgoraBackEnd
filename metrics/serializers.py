from math import isclose

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from metrics.models import ArticleReaction


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
            "owner",
            "bias_percent",
            "fact_percent",
            "fake_percent",
        )
        extra_kwargs = {"owner": {"write_only": True}}
        validators = [
            UniqueTogetherValidator(
                queryset=ArticleReaction.objects.all(),
                fields=("owner", "article")
            )
        ]


class ArticleMetric():
    def __init__(self, bias=None, fact=None, fake=None, opinion=None):
        self.bias = bias or 0
        self.fact = fact or 0
        self.fake = fake or 0


class ArticleMetricsSerializer(serializers.Serializer):
    bias = serializers.FloatField()
    fact = serializers.FloatField()
    fake = serializers.FloatField()
