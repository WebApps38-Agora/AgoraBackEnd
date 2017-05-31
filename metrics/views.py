from rest_framework import viewsets

from metrics.models import Metric
from metrics.serializers import MetricSerializer


class MetricViewset(viewsets.ModelViewSet):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer
