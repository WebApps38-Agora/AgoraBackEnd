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
            "first_name",
            "last_name",
            "gender",
            "profile_picture",
            "political_x",
            "political_y",
            "political_stance",
            "political_color",
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
