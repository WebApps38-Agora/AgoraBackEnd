from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from notifications.models import Notification, NotifiedUsers
from notifications.serializers import NotificationSerializer


class NotificationViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = NotificationSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = Notification.objects.all()

    def get_queryset(self):
        return NotifiedUsers.objects.all().filter(
            user=self.request.user
        ).annotate(
            id=F("notification__id"),
            timestamp=F("notification__timestamp"),
            content=F("notification__content"),
            relevant_id=F("notification__relevant_id"),
            notification_type=F("notification__notification_type"),
        )

    @detail_route()
    def seen(self, request, pk):
        notification = get_object_or_404(
            NotifiedUsers,
            notification=pk,
            user=request.user
        )
        notification.seen = True
        notification.save()

        return Response("Success")

    @detail_route()
    def unsee(self, request, pk):
        notification = get_object_or_404(
            NotifiedUsers,
            notification=pk,
            user=request.user
        )
        notification.seen = False
        notification.save()

        return Response("Success")
