# -*- coding: utf-8 -*-
from django.db import models


class Formidable(models.Model):

    label = models.CharField(max_length=256)
    description = models.TextField()


class Fieldidable(models.Model):
    label = models.CharField(max_length=256)
    form = models.ForeignKey(Formidable, related_name='fields')
    type_id = models.CharField(max_length=256, choices=(('String', 'string'),))


class Rulesidable(models.Model):
    pass


class Validationidable(models.Model):
    pass
