from rest_framework import serializers

from .models import Metric


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    https://stackoverflow.com/questions/23643204/django-rest-framework-dynamically-return-subset-of-fields
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class MetricSerializers(DynamicFieldsModelSerializer):
    cpi = serializers.DecimalField(max_digits=10, decimal_places=2,
                                   required=False)

    class Meta:
        model = Metric
        fields = ('id', 'date', 'channel', 'country', 'os', 'impressions',
                  'clicks', 'installs', 'spend', 'revenue', 'cpi')
