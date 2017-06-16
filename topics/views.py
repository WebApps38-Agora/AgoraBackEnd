from allauth.socialaccount.providers.facebook.views import (
        FacebookOAuth2Adapter
)
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_auth.registration.views import SocialLoginView
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response


from topics.models import Article, Source, Tag, Topic
from topics.serializers import (ArticleSerializer, NestedSourceSerializer,
                                NestedTopicSerializer, NestedTagSerializer,
                                TopicSerializer)


class TopicsAppPermission(permissions.BasePermission):
    message = "Only an admin can add topics / articles / sources"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_staff:
            return True

        return False


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for articles
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (TopicsAppPermission,)


class SourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for sources
    """
    queryset = Source.objects.all()
    serializer_class = NestedSourceSerializer
    permission_classes = (TopicsAppPermission,)


class TopicViewSet(viewsets.ModelViewSet):
    """
    API endpoint for topics
    """
    queryset = Topic.objects.all()
    permission_classes = (TopicsAppPermission,)

    def get_serializer_class(self):
        if self.action == 'list':
            return TopicSerializer
        else:
            return NestedTopicSerializer

    def get_object(self):
        obj = super().get_object()

        # If we're retrieving one topic, add 1 to views
        if self.action == "retrieve":
            obj.views = F('views') + 1
            obj.save()
            obj = self.get_queryset().get(id=obj.id)

        return obj

    @detail_route()
    def subscribe(self, request, pk):
        topic = get_object_or_404(Topic, pk=pk)

        if request.user.is_authenticated:
            topic.subscribers.add(request.user)

        return Response("Success")

    @detail_route()
    def unsubscribe(self, request, pk):
        topic = get_object_or_404(Topic, pk=pk)

        if request.user.is_authenticated:
            topic.subscribers.remove(request.user)

        return Response("Success")


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = NestedTagSerializer

    @detail_route()
    def subscribe(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)

        if request.user.is_authenticated:
            tag.subscribers.add(request.user)

        return Response("Success")

    @detail_route()
    def unsubscribe(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)

        if request.user.is_authenticated:
            tag.subscribers.remove(request.user)

        return Response("Success")


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
