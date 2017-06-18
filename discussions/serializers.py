from rest_framework import serializers
from discussions.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    owner_profile = serializers.SlugRelatedField(
        source="owner.profile",
        read_only=True,
        slug_field="id",
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "topic",
            "owner",
            "owner_profile",
            "parent_comment",
            "published_at",
            "content",
        )
        extra_kwargs = {
            "owner": {
                "required": False,
                "write_only": True
            }
        }
