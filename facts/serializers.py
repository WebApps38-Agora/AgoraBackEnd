from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from facts.models import Reaction, Fact

class ReactionSerializer(serializers.HyperlinkedModelSerializer):
    # TODO: remove next line when user API implemented
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Reaction
        fields = (
            "fact",
            "owner",
            "is_upvote",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Reaction.objects.all(),
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
            "content",
            "owner",
            "reaction_set",
            "score",
        )
