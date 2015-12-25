# -*- coding: utf-8 -*-
from django.db.models import Q
from django.utils.functional import cached_property


from rest_framework import serializers

from formidable.models import Fieldidable
from formidable.serializers.items import ItemSerializer
from formidable.register import SerializerRegister, load_serializer

BASE_FIELDS = (
    'slug', 'label', 'type_id', 'placeholder', 'helptext', 'default',
)


class FieldListSerializer(serializers.ListSerializer):

    def __init__(self, *args, **kwargs):
        kwargs['child'] = LazyChildProxy()
        return super(FieldListSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data, form_id):

        for attrs in validated_data:
            attrs['form_id'] = form_id
            self.child.create(attrs)

    def update(self, fields, validated_data, form_id):

        self.delete([data['slug'] for data in validated_data])

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

    def delete(self, slugs):
        return Fieldidable.objects.filter(~Q(slug__in=slugs)).delete()


class FieldidableSerializer(serializers.ModelSerializer):

    type_id = None

    items = ItemSerializer(many=True)

    class Meta:
        model = Fieldidable
        list_serializer_class = FieldListSerializer

        fields = '__all__'


class FieldItemMixin(object):

    @cached_property
    def item_serializer(self):
        return self.fields['items']

    def create(self, validated_data):
        items_kwargs = validated_data.pop('items')
        field = super(FieldItemMixin, self).create(validated_data)
        self.item_serializer.create(items_kwargs, field.id)
        return field

    def update(self, instance, validated_data):
        items_kwargs = validated_data.pop('items')
        field = super(FieldItemMixin, self).update(instance, validated_data)
        self.item_serializer.update(field.items, items_kwargs, field.id)
        return field


@load_serializer
class TextFieldSerializer(FieldidableSerializer):

    type_id = 'text'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS


@load_serializer
class ParagraphFieldSerializer(TextFieldSerializer):

    type_id = 'paragraph'


@load_serializer
class DropdownFieldSerializer(FieldItemMixin, FieldidableSerializer):

    type_id = 'dropdown'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS + ('items', 'multiple')


@load_serializer
class CheckboxFieldSerializer(FieldItemMixin, FieldidableSerializer):

    type_id = 'checkbox'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS + ('items',)


@load_serializer
class CheckboxesFieldSerializer(FieldItemMixin, FieldidableSerializer):

    type_id = 'checkboxes'

    class Meta(FieldidableSerializer):
        fields = BASE_FIELDS + ('items', 'multiple')


@load_serializer
class RadiosFieldSerializer(FieldItemMixin, FieldidableSerializer):

    type_id = 'radios'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS + ('items', 'multiple')


@load_serializer
class RadiosButtonsFieldSerializer(RadiosFieldSerializer):

    type_id = 'radiosButtons'


@load_serializer
class FileFieldSerializer(FieldidableSerializer):

    type_id = 'file'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS


@load_serializer
class DateFieldSerializer(FieldidableSerializer):

    type_id = 'date'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS


@load_serializer
class EmailFieldSerializer(FieldidableSerializer):

    type_id = 'email'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS


@load_serializer
class NumberFieldSerializer(FieldidableSerializer):

    type_id = 'number'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS


def call_right_serializer_by_instance(meth):

    def _wrapper(self, instance, *args, **kwargs):

        serializer = self.get_right_serializer(instance.type_id)
        meth_name = getattr(serializer, meth.__name__)
        return meth_name(instance, *args, **kwargs)

    return _wrapper


def call_right_serializer_by_attrs(meth):

    def _wrapper(self, attrs, *args, **kwargs):

        serializer = self.get_right_serializer(attrs['type_id'])
        meth_name = getattr(serializer, meth.__name__)
        return meth_name(attrs, *args, **kwargs)

    return _wrapper


def call_all_serializer(meth):

    def _wrapper(self, *args, **kwargs):

        for serializer in self.get_all_serializer():
            meth_name = getattr(serializer, meth.__name__)
            return meth_name(*args, **kwargs)

    return _wrapper


class LazyChildProxy(object):

    def __init__(self):
        register = SerializerRegister.get_instance()
        self.register = {key: value() for key, value in register.iteritems()}

    def get_right_serializer(self, type_id):
        return self.register[type_id]

    def get_all_serializer(self):
        return [serializer for serializer in self.register.values()]

    @call_right_serializer_by_instance
    def to_representation(self, instance):
        pass

    @call_all_serializer
    def bind(self, *args, **kwargs):
        pass

    @call_right_serializer_by_attrs
    def run_validation(self):
        pass

    @call_right_serializer_by_attrs
    def create(self, attrs):
        pass

    @call_right_serializer_by_instance
    def update(self, instance, validated_data):
        pass
