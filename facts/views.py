from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

from facts.serializers import FactSerializer
from topics.models import Topic

class FactList(APIView):
    """
    Retrieve the stored facts for a given topic.
    """

    def get(self, request, topic_pk):
        topic = get_object_or_404(Topic, pk=topic_pk)
        facts = topic.fact_set
        serializer = FactSerializer(facts, many=True, context={'request': request})
        return Response(serializer.data)
