from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication

from metrics.models import ArticleReaction
from metrics.serializers import (ArticleMetric, ArticleMetricsSerializer,
                                 ArticleReactionSerializer)
from topics.models import Article


class ArticleMetricsViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    """
    Retrieve %s of article bias/facts/opinions/etc from article-wide reactions
    """
    queryset = ArticleReaction.objects.all()
    serializer_class = ArticleMetricsSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_field = "article"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ArticleMetricsSerializer
        else:
            return ArticleReactionSerializer

    def get_object(self):
        article_pk = self.kwargs[self.lookup_field]
        article = get_object_or_404(Article, pk=article_pk)
        metric = self.get_queryset().filter(
            article=article
        ).aggregate(
            bias=Avg("bias_percent"),
            fact=Avg("fact_percent"),
            fake=Avg("fake_percent"),
        )

        return ArticleMetric(**metric)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
