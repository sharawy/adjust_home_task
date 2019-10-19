from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from rest_framework import generics

from .filters import MetricFilter
from .models import Metric
from .serializers import MetricSerializers


class MetricsView(generics.ListAPIView):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializers
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MetricFilter
