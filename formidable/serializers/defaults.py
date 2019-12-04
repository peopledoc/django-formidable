from formidable.models import Default
from formidable.security import get_clean_function
from formidable.serializers.list import NestedListSerializerDummyUpdate
from rest_framework import serializers


class DefaultListSerializer(NestedListSerializerDummyUpdate):

    field_id = 'value'
    parent_name = 'field_id'


class DefaultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Default
        list_serializer_class = DefaultListSerializer
        fields = ('value',)

    def to_internal_value(self, data):
        # NOTE: for some reason, data equals to the value.
        # FIXME: investigate a bit further why.
        data = {'value': data}
        data = super().to_internal_value(data)
        return data

    def to_representation(self, instance):
        return instance.value

    def validate_value(self, value):
        if not value:
            return value
        return get_clean_function()(value)
