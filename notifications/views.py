from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication

from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class NotificationViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = NotificationSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = Notification.objects.all()

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
