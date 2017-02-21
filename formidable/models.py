# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models

from formidable import constants
from formidable.register import FieldSerializerRegister


class Formidable(models.Model):

    label = models.CharField(max_length=256)
    description = models.TextField()

    def get_django_form_class(self, role=None, field_factory=None):
        """
        Return the django form class associated with the formidable definition.
        If no role_id is provided all the fields are fetched with an
        ``EDITABLE`` access-right.
        :params role: Fetch defined access for the specified role.
        :params field_factory: Instance of Custom field factory if needed.
        :params field_map: Custom Field Builder used by the field_factory.
        """
        from formidable.forms import get_dynamic_form_class
        return get_dynamic_form_class(self, role, field_factory)

    def get_next_field_order(self):
        """
        Get the next order to set on the field to arrive.
        Try to avoid using this method for performance reasons.
        """
        agg = self.fields.aggregate(models.Max('order'))
        return agg['order__max'] + 1 if agg['order__max'] is not None else 0

    @staticmethod
    def from_json(definition_schema, **kwargs):
        """
        Proxy static method to create an instance of ``Formidable`` more
        easily with a given ``definition_schema``.

        :params definition_schema: Schema in JSON/dict

        >>> Formidable.from_json(definition_schema)
        <Formidable: Formidable object>

        """
        from formidable.serializers import FormidableSerializer

        serializer = FormidableSerializer(data=definition_schema)
        if serializer.is_valid():
            return serializer.save(**kwargs)

        raise ValidationError(serializer.errors)

    def __str__(self):
        return '{formidable.label}'.format(formidable=self)


class Field(models.Model):

    class Meta:
        unique_together = (('slug', 'form'))

    slug = models.CharField(max_length=256)
    label = models.CharField(max_length=256)
    form = models.ForeignKey(Formidable, related_name='fields')
    type_id = models.CharField(
        max_length=256,
        choices=FieldSerializerRegister.get_instance().to_choices()
    )
    placeholder = models.CharField(max_length=256, null=True, blank=True)
    help_text = models.TextField(null=True, blank=True)
    multiple = models.BooleanField(default=False)
    order = models.IntegerField()

    def get_next_order(self):
        """
        Get the next order to set on the item to arrive.
        Try to avoid using this method for performance reasons.
        """
        agg = self.items.aggregate(models.Max('order'))
        return agg['order__max'] + 1 if agg['order__max'] is not None else 0

    def __str__(self):
        return '{field.label}'.format(field=self)


class Default(models.Model):

    value = models.CharField(max_length=256)
    field = models.ForeignKey(Field, related_name='defaults')

    def __str__(self):
        return '{default.value}'.format(default=self)


class Item(models.Model):
    field = models.ForeignKey(Field, related_name='items')
    value = models.CharField(max_length=256)
    label = models.CharField(max_length=256)
    order = models.IntegerField()
    help_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{item.label}: {item.value}'.format(item=self)


class Access(models.Model):

    class Meta:
        unique_together = (('field', 'access_id'),)

    field = models.ForeignKey(Field, related_name='accesses')
    access_id = models.CharField(max_length=128)
    level = models.CharField(max_length=128, choices=(
        (constants.REQUIRED, 'Required'), (constants.EDITABLE, 'Editable'),
        (constants.HIDDEN, 'Hidden'), (constants.READONLY, 'Readonly'),
    ))

    def __str__(self):
        return '{access.access_id}: {access.level}'.format(
            access=self)


class Validation(models.Model):
    field = models.ForeignKey(Field, related_name='validations')
    value = models.CharField(max_length=256)
    type = models.CharField(max_length=256)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{validation.value}: {validation.type}'.format(
            validation=self)


class Preset(models.Model):
    form = models.ForeignKey(Formidable, related_name='presets')
    slug = models.CharField(max_length=128)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{preset.slug}'.format(preset=self)


class PresetArg(models.Model):
    preset = models.ForeignKey(Preset, related_name='arguments')
    slug = models.CharField(max_length=128)
    value = models.CharField(max_length=128, null=True, blank=True)
    field_id = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        if self.field_id:
            return '{preset_arg.slug}: field #{preset_arg.field_id}'.format(
                preset_arg=self)
        return '{preset_arg.slug}: value {preset_arg.value}'.format(
            preset_arg=self)
