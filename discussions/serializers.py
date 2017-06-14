from django.contrib.auth.models import User
from rest_framework import serializers
from discussions.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    # TODO: remove next line when user API implemented
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Comment
        fields = (
            "id",
            "topic",
            "owner",
            "parent_comment",
            "content",
        )
        extra_kwargs = {"owner": {"write_only": True}}
