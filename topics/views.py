from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from topics.models import Article, Source, Topic
from topics.serializers import (ArticleSerializer, SourceSerializer,

import topics.newsapi as newsapi
import topics.semantic as semantic


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
    serializer_class = SourceSerializer
    permission_classes = (TopicsAppPermission,)


class TopicViewSet(viewsets.ModelViewSet):
    """
    API endpoint for topics
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (TopicsAppPermission,)


class UpdateNews(APIView):
    def get(request, pk, format=None):
        newsapi.update_article_database(['bbc-news', 'the-guardian-uk', 'daily-mail'])
        semantic.create_all_topics()
        return Response(status=200)
