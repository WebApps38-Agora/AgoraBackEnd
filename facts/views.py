from django.shortcuts import get_object_or_404

from rest_framework import mixins, generics, viewsets
from rest_framework.response import Response

from facts.serializers import FactSerializer, ReactionSerializer
from facts.models import Fact, Reaction
from topics.models import Topic

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
