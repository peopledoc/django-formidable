# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from formidable.register import FieldSerializerRegister
from formidable import constants


class Formidable(models.Model):

    label = models.CharField(max_length=256)
    description = models.TextField()

    def get_django_form_class(self, role=None, field_factory=None):
        """
        Return the django form class associated with the formidable definition.
        If no role_id is provided all the fields are fetched with an
        ``EDITABLE`` access-right.
        :params role: Fetch defined access for the specified role.
        :params field_factory: Custom field factory if needed.
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


class Default(models.Model):

    value = models.CharField(max_length=256)
    field = models.ForeignKey(Field, related_name='defaults')


class Item(models.Model):
    field = models.ForeignKey(Field, related_name='items')
    value = models.CharField(max_length=256)
    label = models.CharField(max_length=256)
    order = models.IntegerField()
    help_text = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'{}: {}'.format(self.key, self.value)


class Access(models.Model):

    class Meta:
        unique_together = (('field', 'access_id'),)

    field = models.ForeignKey(Field, related_name='accesses')
    access_id = models.CharField(max_length=128)
    level = models.CharField(max_length=128, choices=(
        (constants.REQUIRED, 'Required'), (constants.EDITABLE, 'Editable'),
        (constants.HIDDEN, 'Hidden'), (constants.READONLY, 'Readonly'),
    ))
    display = models.CharField(max_length=128, null=True, blank=True, choices=(
        ('FORM', 'Form'),
        ('TABLE', 'Table'),
    ))


class Validation(models.Model):
    field = models.ForeignKey(Field, related_name='validations')
    value = models.CharField(max_length=256)
    type = models.CharField(max_length=256)
    message = models.TextField(blank=True, null=True)


class Preset(models.Model):
    form = models.ForeignKey(Formidable, related_name='presets')
    slug = models.CharField(max_length=128)
    message = models.TextField(null=True, blank=True)


class PresetArg(models.Model):
    preset = models.ForeignKey(Preset, related_name='arguments')
    slug = models.CharField(max_length=128)
    value = models.CharField(max_length=128, null=True, blank=True)
    field_id = models.CharField(max_length=128, null=True, blank=True)

    def __unicode__(self):
        if self.field_id:
            return '{} : field {}'.format(self.slug, self.field_id)
        return '{} : value {}'.format(self.slug, self.value)
