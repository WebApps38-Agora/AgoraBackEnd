from rest_framework import serializers
from discussions.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "topic",
            "owner",
            "parent_comment",
            "content",
        )
        extra_kwargs = {
            "owner": {
                "required": False,
                "write_only": True
            }
        }
