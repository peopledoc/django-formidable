# -*- coding: utf-8 -*-
from django.db import models

from formidable.register import SerializerRegister


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
        choices=SerializerRegister.get_instance().to_choices()
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
    level = models.CharField(max_length=128)


class Rulesidable(models.Model):
    pass


class Validationidable(models.Model):
    pass
