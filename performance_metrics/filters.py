from django.db.models import Sum, ExpressionWrapper, F, FloatField
from django_filters.rest_framework import DateFromToRangeFilter, CharFilter, FilterSet, DateFilter

from .models import Metric


class MetricFilter(FilterSet):
    date_from = DateFilter(field_name='date', lookup_expr='gte')
    date_to = DateFilter(field_name='date', lookup_expr='lte')
    grouping_by = CharFilter(method='group_by_filter')

    class Meta:
        model = Metric
        fields = ('date', 'channel', 'country', 'os')
        group_by_fields = ('date', 'channel', 'country', 'os')
        aggregated_fields = ('impressions', 'clicks', 'installs',
                             'spend', 'revenue')

    def get_group_by_fields(self):
        if self.Meta.group_by_fields:
            return self.Meta.group_by_fields
        else:
            return ()

    def get_aggregating_fields(self):
        if self.Meta.aggregated_fields:
            return self.Meta.aggregated_fields
        else:
            return ()

    def group_by_filter(self, queryset, name, value):
        fields = set(self.get_group_by_fields())
        aggregated_fields = self.get_aggregating_fields()
        params = set([x.strip().lower() for x in value.split(',')])
        matching = fields & params
        if matching:
            annotated_fields = {aggr_field: Sum(aggr_field)
                                for aggr_field in aggregated_fields}
            annotated_fields['cpi'] = ExpressionWrapper(F('spend') / F('installs'),
                                                        output_field=FloatField())
            return queryset.values(*matching).annotate(**annotated_fields)
        return queryset
