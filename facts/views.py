from rest_framework import viewsets

from facts.serializers import FactSerializer, ReactionSerializer
from facts.models import Fact, Reaction

class FactViewSet(viewsets.ModelViewSet):
    """
    Retrieve the stored facts for a given topic.
    """
    serializer_class = FactSerializer
    queryset = Fact.objects.all()

    def get_queryset(self):
        if 'topic_id' in self.kwargs:
           return Fact.objects.filter(topic__id=self.kwargs['topic_id'])
        else:
           return Fact.objects.all()


class ReactionViewSet(viewsets.ModelViewSet):
    serializer_class = ReactionSerializer
    queryset = Reaction.objects.all()

    def get_queryset(self):
        if 'fact_id' in self.kwargs:
           return Reaction.objects.filter(fact__id=self.kwargs['fact_id'])
        else:
           return Reaction.objects.all()
