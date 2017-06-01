from rest_framework import viewsets

from metrics.models import Reaction
from metrics.serializers import ReactionSerializer


class ReactionViewset(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
