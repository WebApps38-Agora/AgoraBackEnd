from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import detail_route

from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class NotificationViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = NotificationSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = Notification.objects.all()

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @detail_route()
    def seen(self, request, pk):
        notification = Notification.objects.get(
            notification=pk, user=request.user
        )
        notification.seen = True
        notification.save()

    @detail_route()
    def unsee(self, request, pk):
        notification = Notification.objects.get(
            notification=pk, user=request.user
        )
        notification.seen = False
        notification.save()
