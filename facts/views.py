from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from facts.serializers import FactSerializer, ReactionSerializer
from facts.models import Fact, FactReaction
from user_profile.models import Profile


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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @detail_route()
    def user(self, request, pk):
        user = get_object_or_404(Profile, pk=pk).user

        serializer = FactSerializer(user.fact_set, many=True)
        return Response(serializer.data)


class FactReactionViewSet(viewsets.ModelViewSet):
    serializer_class = ReactionSerializer
    queryset = FactReaction.objects.all()

    def get_queryset(self):
        if 'fact_id' in self.kwargs:
            return FactReaction.objects.filter(fact__id=self.kwargs['fact_id'])
        else:
            return FactReaction.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
