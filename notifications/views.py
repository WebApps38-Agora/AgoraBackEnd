from django.db.models import F
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import detail_route

from notifications.models import Notification, NotifiedUsers
from notifications.serializers import NotificationSerializer #, NotifiedUsersSerializer


class NotificationViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = NotificationSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = Notification.objects.all()

    def get_queryset(self):
        # return NotifiedUsers.objects.all().filter(user=self.request.user.id)
        return NotifiedUsers.objects.all().filter(user=self.request.user)\
                                          .annotate(
                                              timestamp=F("notification__timestamp"),
                                              content=F("notification__content"),
                                              relevant_id=F("notification__relevant_id")
                                              )

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
