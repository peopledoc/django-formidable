# -*- coding: utf-8 -*-

from django.core import validators


class ValidatorFactory(object):

    maps = {
        'MINLENGTH': lambda self, x, y=None: self.min_length(x, y),
        'MAXLENGTH': lambda self, x, y=None: self.max_length(x, y),
        'REGEXP': lambda self, x, y=None: self.regexp(x, y),
    }

    def min_length(self, limit_value, message):
        limit_value = int(limit_value)
        return validators.MinLengthValidator(limit_value, message)

    def max_length(self, limit_value, message):
        limit_value = int(limit_value)
        return validators.MaxLengthValidator(limit_value, message)

    def regexp(self, value, message):
        return validators.RegexValidator(regex=value, message=message)

    def produce(self, validation):
        meth = self.maps[validation.type]
        msg = validation.message or None
        return meth(self, validation.value, msg)
