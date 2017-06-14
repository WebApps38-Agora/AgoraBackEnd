from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication

from user_profile.models import Profile
from user_profile.serializers import ProfileSerializer


class ProfileViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
