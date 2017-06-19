from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from metrics.models import ArticleReaction
from metrics.serializers import (ArticleMetric, ArticleMetricsSerializer,
                                 ArticleReactionSerializer)
from topics.models import Article
from user_profile.models import Profile


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

        bias = article.bias

        return ArticleMetric(bias=bias)

    def perform_create(self, serializer):
        metric = serializer.save(owner=self.request.user)
        metric.article.update_bias(metric.bias)

    @detail_route(methods=["get"])
    def user(self, request, article):
        user = get_object_or_404(Profile, pk=article).user

        serializer = ArticleReactionSerializer(
            user.articlereaction_set,
            many=True
        )

        return Response(serializer.data)
