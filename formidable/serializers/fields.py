# -*- coding: utf-8 -*-
from django.utils.functional import cached_property
from django.db.models import Prefetch


from rest_framework import serializers

from formidable import constants
from formidable.models import Field, Access
from formidable.serializers.items import ItemSerializer
from formidable.serializers.access import AccessSerializer
from formidable.serializers.validation import ValidationSerializer
from formidable.serializers.defaults import DefaultSerializer
from formidable.serializers.child_proxy import LazyChildProxy
from formidable.register import FieldSerializerRegister, load_serializer
from formidable.serializers.list import NestedListSerializer
from formidable.serializers.common import WithNestedSerializer

BASE_FIELDS = (
    'slug', 'label', 'type_id', 'placeholder', 'help_text',
    'accesses', 'validations', 'order', 'defaults'
)


field_register = FieldSerializerRegister.get_instance()


class FieldListSerializer(NestedListSerializer):

    field_id = 'slug'
    parent_name = 'form_id'

    def __init__(self, *args, **kwargs):
        kwargs['child'] = LazyChildProxy(field_register)
        return super(FieldListSerializer, self).__init__(*args, **kwargs)

    def validate(self, validated_data):
        """
        At this point all the data have been validated. We have to inject the
        order before the update/create method sorts the validated data
        by id.
        """
        for index, data in enumerate(validated_data):
            data['order'] = index

        return validated_data


class FieldSerializer(WithNestedSerializer):

    type_id = None

    items = ItemSerializer(many=True)
    accesses = AccessSerializer(many=True)
    validations = ValidationSerializer(many=True, required=False)
    # redifine here the order field just to take it at the save/update time
    # The order is automatically calculated, if the order is define in
    # incomming payload, it will be automatically overrided.
    order = serializers.IntegerField(write_only=True, required=False)
    defaults = DefaultSerializer(many=True, required=False)

    nested_objects = ['accesses', 'validations', 'defaults']

    class Meta:
        model = Field
        list_serializer_class = FieldListSerializer
        fields = '__all__'

    @cached_property
    def access_serializer(self):
        return self.fields['accesses']

    @cached_property
    def validations_serializer(self):
        return self.fields['validations']

    @cached_property
    def defaults_serializer(self):
        return self.fields['defaults']


class ListContextFieldSerializer(serializers.ListSerializer):

    def set_context(self, key, value):
        self._context[key] = value
        self.child._context[key] = value

    @property
    def role(self):
        return self._context['role']

    def get_attribute(self, instance):
        qs = super(ListContextFieldSerializer, self).get_attribute(instance)
        access_qs = Access.objects.filter(access_id=self.role)
        access_qs = access_qs.exclude(level=constants.HIDDEN)
        qs = qs.prefetch_related(Prefetch('accesses', queryset=access_qs))
        return qs

    def to_representation(self, fields):
        res = []
        for field in fields.order_by('order').all():
            if field.accesses.exists():
                res.append(self.child.to_representation(field))

        return res


class ContextFieldSerializer(serializers.ModelSerializer):

    disabled = serializers.SerializerMethodField()
    required = serializers.SerializerMethodField()
    validations = ValidationSerializer(many=True, required=False)
    items = ItemSerializer(many=True, required=False)
    defaults = DefaultSerializer(many=True, required=False)

    class Meta:
        list_serializer_class = ListContextFieldSerializer
        model = Field
        fields = (
            'slug', 'label', 'type_id', 'placeholder', 'help_text',
            'validations', 'disabled', 'required', 'multiple', 'items',
            'defaults',
        )

    @property
    def role(self):
        return self._context['role']

    def get_disabled(self, obj):
        return obj.accesses.get(access_id=self.role).level == \
            constants.READONLY

    def get_required(self, obj):
        return obj.accesses.get(access_id=self.role).level == \
            constants.REQUIRED


class FieldItemMixin(object):

    @cached_property
    def item_serializer(self):
        return self.fields['items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        field = super(FieldItemMixin, self).create(validated_data)
        self.item_serializer.create(field, items_data)
        return field

    def update(self, instance, validated_data):
        items_kwargs = validated_data.pop('items')
        field = super(FieldItemMixin, self).update(instance, validated_data)
        self.item_serializer.update(field.items, field, items_kwargs)
        return field


@load_serializer(field_register)
class TextFieldSerializer(FieldSerializer):

    type_id = 'text'

    class Meta(FieldSerializer.Meta):
        fields = BASE_FIELDS


@load_serializer(field_register)
class ParagraphFieldSerializer(TextFieldSerializer):

    type_id = 'paragraph'


@load_serializer(field_register)
class DropdownFieldSerializer(FieldItemMixin, FieldSerializer):

    type_id = 'dropdown'

    class Meta(FieldSerializer.Meta):
        fields = BASE_FIELDS + ('items', 'multiple')


@load_serializer(field_register)
class CheckboxFieldSerializer(FieldSerializer):

    type_id = 'checkbox'

    class Meta(FieldSerializer.Meta):
        fields = BASE_FIELDS


@load_serializer(field_register)
class CheckboxesFieldSerializer(FieldItemMixin, FieldSerializer):

    type_id = 'checkboxes'

    class Meta(FieldSerializer.Meta):
        fields = BASE_FIELDS + ('items',)


@load_serializer(field_register)
class RadiosFieldSerializer(FieldItemMixin, FieldSerializer):

    type_id = 'radios'

    class Meta(FieldSerializer.Meta):
        fields = BASE_FIELDS + ('items',)


@load_serializer(field_register)
class RadiosButtonsFieldSerializer(RadiosFieldSerializer):

    type_id = 'radios_buttons'


@load_serializer(field_register)
class FileFieldSerializer(FieldSerializer):

    type_id = 'file'

    class Meta(FieldSerializer.Meta):
        fields = BASE_FIELDS


@load_serializer(field_register)
class DateFieldSerializer(FieldSerializer):

    type_id = 'date'

    class Meta(FieldSerializer.Meta):
        fields = BASE_FIELDS


@load_serializer(field_register)
class EmailFieldSerializer(FieldSerializer):

    type_id = 'email'

    class Meta(FieldSerializer.Meta):
        fields = BASE_FIELDS


@load_serializer(field_register)
class NumberFieldSerializer(FieldSerializer):

    type_id = 'number'

    class Meta(FieldSerializer.Meta):
        fields = BASE_FIELDS


@load_serializer(field_register)
class HelpTextFieldSerializer(FieldSerializer):

    type_id = 'help_text'
    help_text = serializers.CharField(required=True)

    class Meta(FieldSerializer.Meta):
        # Just to remove "label" attribute
        fields = list(set(BASE_FIELDS) - set(['label']))


@load_serializer(field_register)
class TitleFieldSerializer(FieldSerializer):

    type_id = 'title'

    class Meta(FieldSerializer.Meta):
        # Just to remove "help_text" attribute
        fields = list(set(BASE_FIELDS) - set(['help_text']))


@load_serializer(field_register)
class SeparatorFieldSerializer(FieldSerializer):

    type_id = 'separator'

    class Meta(FieldSerializer.Meta):
        # Just to remove "help_text" attribute
        fields = list(set(BASE_FIELDS) - set(['label', 'help_text']))
