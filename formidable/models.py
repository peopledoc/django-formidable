# -*- coding: utf-8 -*-
from django.db import models

from formidable.register import FieldSerializerRegister


class Formidable(models.Model):

    label = models.CharField(max_length=256)
    description = models.TextField()

    def get_django_form_class(self, role=None):
        from formidable.forms import get_dynamic_form_class
        return get_dynamic_form_class(self, role)

    def get_next_field_order(self):
        """
        Get the next order to set on the field to arrive.
        Try to avoid use this method for performance reason.
        """
        agg = self.fields.aggregate(models.Max('order'))
        return agg['order__max'] + 1 if agg['order__max'] is not None else 0


class Fieldidable(models.Model):

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
    default = models.TextField(null=True, blank=True)
    multiple = models.BooleanField(default=False)
    order = models.IntegerField()


class Item(models.Model):
    field = models.ForeignKey(Fieldidable, related_name='items')
    key = models.CharField(max_length=256)
    value = models.CharField(max_length=256)

    def __unicode__(self):
        return u'{}: {}'.format(self.key, self.value)


class Access(models.Model):

    class Meta:
        unique_together = (('field', 'access_id'),)

    field = models.ForeignKey(Fieldidable, related_name='accesses')
    access_id = models.CharField(max_length=128)
    level = models.CharField(max_length=128, choices=(
        ('REQUIRED', 'Required'), ('EDITABLE', 'Editable'),
        ('HIDDEN', 'Hidden'), ('READONLY', 'Readonly'),
    ))
    display = models.CharField(max_length=128, null=True, blank=True, choices=(
        ('FORM', 'Form'),
        ('TABLE', 'Table'),
    ))


class Validationidable(models.Model):
    field = models.ForeignKey(Fieldidable, related_name='validations')
    value = models.CharField(max_length=256)
    type = models.CharField(max_length=256)
    message = models.TextField(blank=True, null=True)


class Preset(models.Model):
    form = models.ForeignKey(Formidable, related_name='presets')
    slug = models.CharField(max_length=128)
    message = models.TextField()


class PresetArg(models.Model):
    preset = models.ForeignKey(Preset, related_name='arguments')
    value = models.CharField(max_length=128)
    type = models.CharField(max_length=64, choices=(
        ('field', 'field'), ('value', 'value'),
    ))
