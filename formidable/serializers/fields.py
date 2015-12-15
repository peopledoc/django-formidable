# -*- coding: utf-8 -*-
from rest_framework import serializers

from formidable.models import Fieldidable
from formidable.serializers.items import ItemSerializer


class FieldListSerializer(serializers.ListSerializer):

    def __init__(self, *args, **kwargs):
        kwargs['child'] = LazyChildProxy()
        return super(FieldListSerializer, self).__init__(*args, **kwargs)


class FieldidableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fieldidable
        list_serializer_class = FieldListSerializer
        fields = (
            'id', 'label', 'type_id', 'placeholder', 'helptext', 'default',
        )


class TextFieldSerializer(FieldidableSerializer):
    pass


class DropdownFieldSerializer(FieldidableSerializer):

    items = ItemSerializer(many=True)

    class Meta(FieldidableSerializer.Meta):
        fields = FieldidableSerializer.Meta.fields + ('items',)


register = {
    'dropdown': DropdownFieldSerializer,
    'text': TextFieldSerializer,
}


def call_right_serializer(meth):

    def _wrapper(self, instance, *args, **kwargs):

        serializer = self.get_right_serializer(instance)
        meth_name = getattr(serializer, meth.__name__)
        return meth_name(instance, *args, **kwargs)

    return _wrapper


def call_all_serializer(meth):

    def _wrapper(self, *args, **kwargs):

        for serializer in self.get_all_serializer():
            meth_name = getattr(serializer, meth.__name__)
            return meth_name(*args, **kwargs)

    return _wrapper


class LazyChildProxy(object):

    def __init__(self):
        self.register = {key: value() for key, value in register.iteritems()}

    def get_right_serializer(self, instance):
        return self.register[instance.type_id]

    def get_all_serializer(self):
        return [serializer for serializer in self.register.values()]

    @call_right_serializer
    def to_representation(self, instance):
        pass

    @call_all_serializer
    def bind(self, *args, **kwargs):
        pass
