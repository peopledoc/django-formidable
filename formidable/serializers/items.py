# -*- coding: utf-8 -*-

from django.db.models import Q

from rest_framework import serializers
from rest_framework.utils import html
from rest_framework.serializers import ValidationError
from rest_framework.settings import api_settings

from formidable.models import Item


class DictItemSerializer(serializers.ListSerializer):

    def to_representation(self, items):
        return {
            item.key: item.value for item in items.all()
        }

    def to_internal_value(self, data):
        """
        Dicts of native values <- Dict of primitive datatypes.
        """
        if html.is_html_input(data):
            data = html.parse_html_list(data)

        if not isinstance(data, dict):
            message = self.error_messages['not_a_dict'].format(
                input_type=type(data).__name__
            )
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            })

        if not self.allow_empty and len(data) == 0:
            message = self.error_messages['empty']
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            })

        ret = []
        errors = []

        for key, value in data.iteritems():
            item = {'key': key, 'value': value}
            try:
                validated = self.child.run_validation(item)
            except ValidationError as exc:
                errors.append(exc.detail)
            else:
                ret.append(validated)
                errors.append({})

        if any(errors):
            raise ValidationError(errors)

        return ret

    def create(self, validated_data, field_id):

        for data in validated_data:
            data['field_id'] = field_id
            self.child.create(data)

    def update(self, items, validated_data, field_id):

        keys = [data['key'] for data in validated_data]
        Item.objects.filter(~Q(key__in=keys), field_id=field_id).delete()

        items = list(items.all())

        for index, data in enumerate(validated_data):
            qs = Item.objects.filter(
                key=data['key'], field_id=field_id
            )
            data = validated_data[index]
            data['field_id'] = field_id
            if qs.exists():
                self.child.update(items[index], data)
            else:
                self.child.create(data)


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        list_serializer_class = DictItemSerializer
        fields = ('key', 'value')
