from rest_framework import serializers

from user_profile.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(
        source="user",
        read_only=True,
        slug_field="username",
    )

    class Meta:
        model = Profile
        fields = (
            "id",
            "username",
            "user",
            "profile_picture",
            "political_x",
            "political_y",
            "profession",
            "town",
            "country",
        )
        read_only_fields = ("id",)
        extra_kwargs = {
            "user": {
                "write_only": True,
                "required": False,
            },
        }
