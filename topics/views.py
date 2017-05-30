from rest_framework import viewsets
from topics.models import Article, Paper, Topic
from topics.serializers import (ArticleSerializer, PaperSerializer,
                                TopicSerializer)


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for articles
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class PaperViewSet(viewsets.ModelViewSet):
    """
    API endpoint for paper
    """
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer


class TopicViewSet(viewsets.ModelViewSet):
    """
    API endpoint for topics
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
