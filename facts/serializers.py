from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from facts.models import FactReaction, Fact


class ReactionSerializer(serializers.HyperlinkedModelSerializer):
    # TODO: remove next line when user API implemented
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = FactReaction
        fields = (
            "fact",
            "owner",
            "is_upvote",
        )
        extra_kwargs = {"owner": {"write_only": True}}
        validators = [
            UniqueTogetherValidator(
                queryset=FactReaction.objects.all(),
                fields=("owner", "fact")
            )
        ]


class FactSerializer(serializers.HyperlinkedModelSerializer):
    # TODO: remove next line when user API implemented
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Fact
        fields = (
            "topic",
            "owner",
            "content",
            "factreaction_set",
            "score",
        )
        extra_kwargs = {"owner": {"write_only": True}}
