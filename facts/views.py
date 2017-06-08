from django.shortcuts import get_object_or_404

from rest_framework import mixins, generics
from rest_framework.response import Response

from facts.serializers import FactSerializer
from facts.models import Fact
from topics.models import Topic

class FactList(mixins.CreateModelMixin,
               generics.GenericAPIView):
    """
    Retrieve the stored facts for a given topic.
    """
    serializer_class = FactSerializer
    queryset = Fact.objects.all()


    def get(self, request, topic_pk):
        topic = get_object_or_404(Topic, pk=topic_pk)
        facts = topic.fact_set
        serializer = FactSerializer(facts, many=True, context={'request': request})
        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
