# -*- coding: utf-8 -*-
from django.db import models

from formidable.serializers.register import SerializerRegister


class Formidable(models.Model):

    label = models.CharField(max_length=256)
    description = models.TextField()


class Fieldidable(models.Model):
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


class Rulesidable(models.Model):
    pass


class Validationidable(models.Model):
    pass
