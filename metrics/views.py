from collections import defaultdict
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets

from metrics.models import Reaction
from metrics.serializers import (ArticleMetric, ArticleMetricsSerializer,
                                 ReactionSerializer)
from topics.models import Article
from utils.fenwick_tree import FenwickTree


class ReactionViewset(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer


class ArticleMetricsAPIView(generics.RetrieveAPIView):
    """
    Retrieve %s of article bias/facts/opinions/etc.
    """
    queryset = Reaction.objects.all()
    serializer_class = ArticleMetricsSerializer
    lookup_field = "article"

    def get_object(self):
        article_pk = self.kwargs[self.lookup_field]
        article = get_object_or_404(Article, pk=article_pk)
        reactions = self.get_queryset().filter(article=article_pk)

        bias = FenwickTree(article.content_len)
        fact = FenwickTree(article.content_len)
        fake = FenwickTree(article.content_len)
        opinion = FenwickTree(article.content_len)

        for reaction in reactions:
            react = reaction.get_reaction_display()

            if react is "Bias":
                bias.add_range(reaction.location, reaction.content_end)
            elif react is "Fact":
                fact.add_range(reaction.location, reaction.content_end)
            elif react is "Fake":
                fake.add_range(reaction.location, reaction.content_end)
            elif react is "Opinion":
                opinion.add_range(reaction.location, reaction.content_end)

        reaction_counts = defaultdict(int)

        for idx in range(article.content_len):
            reactions_here = {
                "bias": bias[idx],
                "fact": fact[idx],
                "fake": fake[idx],
                "opinion": fake[idx],
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
