from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from metrics.models import ArticleReaction


class ArticleReactionSerializer(serializers.ModelSerializer):
    owner_profile = serializers.SlugRelatedField(
        source="owner.profile",
        read_only=True,
        slug_field="id",
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
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=ArticleReaction.objects.all(),
        #         fields=("owner", "article")
        #     )
        # ]


class ArticleMetric():
    def __init__(self, bias=None):
        self.bias = bias or -1


class ArticleMetricsSerializer(serializers.Serializer):
    bias = serializers.FloatField()
