from rest_framework import permissions, viewsets
from topics.models import Article, Paper, Topic
from topics.serializers import (ArticleSerializer, PaperSerializer,
                                TopicSerializer)


class TopicsAppPermission(permissions.BasePermission):
    message = "Only an admin can add topics / articles / papers"

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


class PaperViewSet(viewsets.ModelViewSet):
    """
    API endpoint for paper
    """
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer
    permission_classes = (TopicsAppPermission,)


class TopicViewSet(viewsets.ModelViewSet):
    """
    API endpoint for topics
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (TopicsAppPermission,)
