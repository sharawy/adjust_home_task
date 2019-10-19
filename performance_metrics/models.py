from django.db import models
from django.db.models import ExpressionWrapper, F, FloatField


class MetricManager(models.Manager):
    def get_queryset(self):
        q = super(MetricManager, self).get_queryset()
        annotated_fields = self.get_default_annotated_fields()
        return q.annotate(**annotated_fields)

    @staticmethod
    def get_default_annotated_fields():
        return {'cpi': ExpressionWrapper(F('spend') / F('installs'),
                                         output_field=FloatField())}


class Metric(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)
    channel = models.CharField(max_length=50)
    country = models.CharField(max_length=2)
    os = models.CharField(max_length=50)
    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    installs = models.IntegerField(default=0)
    spend = models.DecimalField(max_digits=10, decimal_places=2)
    revenue = models.DecimalField(max_digits=10, decimal_places=2)

    objects = MetricManager()
