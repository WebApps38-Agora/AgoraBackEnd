from rest_framework import mixins, permissions, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import list_route
from rest_framework.response import Response

from user_profile.models import Profile
from user_profile.serializers import ProfileSerializer


class ProfilePermission(permissions.IsAuthenticated):
    """
    Only logged in user can see own profile
    """
    message = "You need to be logged in to look at your profile"

    def has_permission(self, request, view):
        if view.action == "retrieve":
            return True
        return super().has_permission(request, view)


class ProfileViewSet(mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (ProfilePermission,)

    def list(self, request):
        serializer = self.get_serializer(request.user.profile)
        return Response(serializer.data)

    @list_route(methods=["put"])
    def update_own_profile(self, request):
        serializer = self.get_serializer(
            request.user.profile,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
