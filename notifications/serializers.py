from rest_framework import serializers

from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    seen = serializers.BooleanField()
    
    class Meta:
        model = Notification
        fields = (
            "timestamp",
            "content",
            "relevant_id",
            "seen",
        )
