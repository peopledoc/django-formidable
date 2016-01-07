# -*- coding: utf-8 -*-
from django.db import models

from formidable.register import FieldSerializerRegister


class Formidable(models.Model):

    label = models.CharField(max_length=256)
    description = models.TextField()


class Fieldidable(models.Model):

    class Meta:
        unique_together = (('slug', 'form'),)

    slug = models.CharField(max_length=256)
    label = models.CharField(max_length=256)
    form = models.ForeignKey(Formidable, related_name='fields')
    type_id = models.CharField(
        max_length=256,
        choices=FieldSerializerRegister.get_instance().to_choices()
    )
    placeholder = models.CharField(max_length=256, null=True, blank=True)
    helptext = models.TextField(null=True, blank=True)
    default = models.TextField(null=True, blank=True)
    multiple = models.BooleanField(default=False)


class Item(models.Model):
    field = models.ForeignKey(Fieldidable, related_name='items')
    key = models.CharField(max_length=256)
    value = models.CharField(max_length=256)


class Access(models.Model):

    class Meta:
        unique_together = (('field', 'access_id'),)

    field = models.ForeignKey(Fieldidable, related_name='accesses')
    access_id = models.CharField(max_length=128)
    level = models.CharField(max_length=128, choices=(
        ('REQUIRED', 'REQUIRED'), ('EDITABLE', 'EDITABLE'),
        ('HIDDEN', 'HIDDEN'), ('READONLY', 'READONLY'),
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
