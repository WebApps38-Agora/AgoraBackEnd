from django.db.models import F
from rest_framework import permissions, viewsets

from topics.models import Article, Source, Topic
from topics.serializers import (ArticleSerializer, NestedSourceSerializer,
                                NestedTopicSerializer, TopicSerializer)


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

    def get_queryset(self):
        if self.action == 'list':
            return sorted(
                Topic.objects.all(), key=lambda t: t.ranking, reverse=True
            )
        else:
            return Topic.objects.all()

    def get_object(self):
        obj = super().get_object()

        # If we're retrieving one topic, add 1 to views
        if self.action == "retrieve":
            obj.views = F('views') + 1
            obj.save()
            obj = self.get_queryset().get(id=obj.id)

        return obj


from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
