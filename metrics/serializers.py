from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from metrics.models import ArticleReaction


class ArticleReactionSerializer(serializers.ModelSerializer):
    owner_profile = serializers.SlugRelatedField(
        source="owner",
        read_only=True,
        slug_field="profile",
    )

    def validate(self, data):
        """
        Checks that bias has valid percentage
        """

        if data["bias"] < 0 or data["bias"] > 100:
            raise serializers.ValidationError(
                "Invalid bias percentage"
            )

        return data

    class Meta:
        model = ArticleReaction
        fields = (
            "article",
            "owner",
            "owner_profile",
            "bias",
        )
        extra_kwargs = {
            "owner": {
                "write_only": True,
                "required": False,
            }
        }
        validators = [
            UniqueTogetherValidator(
                queryset=ArticleReaction.objects.all(),
                fields=("owner", "article")
            )
        ]


class ArticleMetric():
    def __init__(self, bias=None):
        self.bias = bias or 0


class ArticleMetricsSerializer(serializers.Serializer):
    bias = serializers.FloatField()
