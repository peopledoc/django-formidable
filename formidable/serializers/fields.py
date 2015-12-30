# -*- coding: utf-8 -*-
from django.db.models import Q
from django.utils.functional import cached_property


from rest_framework import serializers

from formidable.models import Fieldidable
from formidable.serializers.items import ItemSerializer
from formidable.serializers.access import AccessSerializer
from formidable.serializers.child_proxy import LazyChildProxy
from formidable.register import FieldSerializerRegister, load_serializer

BASE_FIELDS = (
    'slug', 'label', 'type_id', 'placeholder', 'helptext', 'default',
    'accesses',
)


field_register = FieldSerializerRegister.get_instance()


class FieldListSerializer(serializers.ListSerializer):

    def __init__(self, *args, **kwargs):
        kwargs['child'] = LazyChildProxy(field_register)
        return super(FieldListSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data, form_id):

        for attrs in validated_data:
            attrs['form_id'] = form_id
            self.child.create(attrs)

    def update(self, fields, validated_data, form_id):
        slugs = [data['slug'] for data in validated_data]

        # delete field with slug which are not in payload anymore
        Fieldidable.objects.filter(
            ~Q(slug__in=slugs), form_id=form_id
        ).delete()

        fields = list(fields.all())

        for index, data in enumerate(validated_data):
            slug = data['slug']
            qs = Fieldidable.objects.filter(slug=slug, form_id=form_id)
            data['form_id'] = form_id
            if qs.exists():
                instance = fields[index]
                self.child.update(instance, data)
            else:
                self.child.create(data)


class FieldidableSerializer(serializers.ModelSerializer):

    type_id = None

    items = ItemSerializer(many=True)
    accesses = AccessSerializer(many=True)

    class Meta:
        model = Fieldidable
        list_serializer_class = FieldListSerializer
        fields = '__all__'

    @cached_property
    def access_serializer(self):
        return self.fields['accesses']

    def create(self, validated_data):
        accesses_data = validated_data.pop('accesses')
        field = super(FieldidableSerializer, self).create(validated_data)
        self.access_serializer.create(accesses_data, field)
        return field

    def update(self, instance, validated_data):
        accesses_data = validated_data.pop('accesses')
        field = super(FieldidableSerializer, self).update(
            instance, validated_data
        )
        self.access_serializer.update(field.accesses, accesses_data, field)
        return field


class FieldItemMixin(object):

    @cached_property
    def item_serializer(self):
        return self.fields['items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        field = super(FieldItemMixin, self).create(validated_data)
        self.item_serializer.create(items_data, field.id)
        return field

    def update(self, instance, validated_data):
        items_kwargs = validated_data.pop('items')
        field = super(FieldItemMixin, self).update(instance, validated_data)
        self.item_serializer.update(field.items, items_kwargs, field.id)
        return field


@load_serializer(field_register)
class TextFieldSerializer(FieldidableSerializer):

    type_id = 'text'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS


@load_serializer(field_register)
class ParagraphFieldSerializer(TextFieldSerializer):

    type_id = 'paragraph'


@load_serializer(field_register)
class DropdownFieldSerializer(FieldItemMixin, FieldidableSerializer):

    type_id = 'dropdown'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS + ('items', 'multiple')


@load_serializer(field_register)
class CheckboxFieldSerializer(FieldItemMixin, FieldidableSerializer):

    type_id = 'checkbox'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS + ('items',)


@load_serializer(field_register)
class CheckboxesFieldSerializer(FieldItemMixin, FieldidableSerializer):

    type_id = 'checkboxes'

    class Meta(FieldidableSerializer):
        fields = BASE_FIELDS + ('items', 'multiple')


@load_serializer(field_register)
class RadiosFieldSerializer(FieldItemMixin, FieldidableSerializer):

    type_id = 'radios'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS + ('items', 'multiple')


@load_serializer(field_register)
class RadiosButtonsFieldSerializer(RadiosFieldSerializer):

    type_id = 'radiosButtons'


@load_serializer(field_register)
class FileFieldSerializer(FieldidableSerializer):

    type_id = 'file'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS


@load_serializer(field_register)
class DateFieldSerializer(FieldidableSerializer):

    type_id = 'date'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS


@load_serializer(field_register)
class EmailFieldSerializer(FieldidableSerializer):

    type_id = 'email'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS


@load_serializer(field_register)
class NumberFieldSerializer(FieldidableSerializer):

    type_id = 'number'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS
