from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from facts.models import FactReaction, Fact


class ReactionSerializer(serializers.ModelSerializer):
    owner_profile = serializers.SlugRelatedField(
        source="owner",
        read_only=True,
        slug_field="profile",
    )

    class Meta:
        model = FactReaction
        fields = (
            "fact",
            "owner",
            "owner_profile",
            "is_upvote",
        )
        extra_kwargs = {
            "owner": {
                "write_only": True,
                "required": False,
            }
        }
        validators = [
            UniqueTogetherValidator(
                queryset=FactReaction.objects.all(),
                fields=("owner", "fact")
            )
        ]


class FactSerializer(serializers.ModelSerializer):
    owner_profile = serializers.SlugRelatedField(
        source="owner",
        read_only=True,
        slug_field="profile",
    )

    class Meta:
        model = Fact
        fields = (
            "topic",
            "owner",
            "owner_profile",
            "content",
            "factreaction_set",
            "score",
        )
        extra_kwargs = {
            "owner": {
                "write_only": True,
                "required": False,
            }
        }
