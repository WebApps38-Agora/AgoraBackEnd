from collections import defaultdict
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, viewsets

from metrics.models import ArticleReaction, HighlightedReaction
from metrics.serializers import (ArticleMetric, ArticleMetricsSerializer,
                                 ArticleReactionSerializer,
                                 HighlightedReactionSerializer)
from topics.models import Article
from utils.fenwick_tree import FenwickTree


class ArticleReactionViewset(viewsets.ModelViewSet):
    queryset = ArticleReaction.objects.all()
    serializer_class = ArticleReactionSerializer


class HighlightedReactionViewset(viewsets.ModelViewSet):
    queryset = HighlightedReaction.objects.all()
    serializer_class = HighlightedReactionSerializer


class ArticleHighlightedMetricsAPIView(generics.RetrieveAPIView):
    """
    Retrieve %s of article bias/facts/opinions/etc from highlighted reactions
    """
    queryset = HighlightedReaction.objects.all()
    serializer_class = ArticleMetricsSerializer
    lookup_field = "article"

    def get_object(self):
        article_pk = self.kwargs[self.lookup_field]
        article = get_object_or_404(Article, pk=article_pk)
        reactions = self.get_queryset().filter(article=article_pk)

        bias = FenwickTree(article.content_len)
        fact = FenwickTree(article.content_len)
        fake = FenwickTree(article.content_len)

        for reaction in reactions:
            react = reaction.get_reaction_display()

            if react is "Bias":
                bias.add_range(reaction.location, reaction.content_end)
            elif react is "Fact":
                fact.add_range(reaction.location, reaction.content_end)
            elif react is "Fake":
                fake.add_range(reaction.location, reaction.content_end)

        reaction_counts = defaultdict(int)

        for idx in range(article.content_len):
            reactions_here = {
                "bias": bias[idx],
                "fact": fact[idx],
                "fake": fake[idx],
            }

            max_value = max(reactions_here.values())

            if not max_value == 0:
                maximums = [
                    k for k, v in reactions_here.items() if v == max_value
                ]

                if len(maximums) == 1:
                    reaction_counts[maximums[0]] += 1

        reaction_counts = {
            k: (v / article.content_len) * 100
            for k, v in reaction_counts.items()
        }

        return ArticleMetric(**reaction_counts)


class ArticleMetricsViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    """
    Retrieve %s of article bias/facts/opinions/etc from article-wide reactions
    """
    queryset = ArticleReaction.objects.all()
    serializer_class = ArticleMetricsSerializer
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
