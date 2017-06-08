from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from facts.models import Reaction, Fact


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
        )
