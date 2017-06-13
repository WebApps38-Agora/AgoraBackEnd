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
            "username",
            "profile_picture",
            "alignment",
            "profession",
            "town",
            "country",
        )
