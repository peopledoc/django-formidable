# -*- coding: utf-8 -*-

from django.core import validators
from django.utils.translation import ugettext_lazy as _


class MaxOrEqualValueValidator(validators.MaxValueValidator):

    message = _("Ensure this value is less than %(limit_value)s.")

    def compare(self, a, b):
        return a >= b


class MinOrEqualValueValidator(validators.MinValueValidator):

    message = _("Ensure this value is greater than %(limit_value)s.")

    def compare(self, a, b):
        return a <= b


class ValidatorFactory(object):

    maps = {
        'MINLENGTH': lambda self, x, y=None: self.min_length(x, y),
        'MAXLENGTH': lambda self, x, y=None: self.max_length(x, y),
        'REGEXP': lambda self, x, y=None: self.regexp(x, y),
        'GT': lambda self, x, y=None: self.gt(x, y),
        'GTE': lambda self, x, y=None: self.gte(x, y),
        'LT': lambda self, x, y=None: self.lt(x, y),
        'LTE': lambda self, x, y=None: self.lte(x, y),
        'EQ': lambda self, x, y=None: self.eq(x, y),
        'NEQ': lambda self, x, y=None: self.neq(x, y),
    }

    def min_length(self, limit_value, message):
        limit_value = int(limit_value)
        return validators.MinLengthValidator(limit_value, message)

    def max_length(self, limit_value, message):
        limit_value = int(limit_value)
        return validators.MaxLengthValidator(limit_value, message)

    def regexp(self, value, message):
        return validators.RegexValidator(regex=value, message=message)

    def gt(self, value, message):
        return validators.MaxValueValidator(value, message)

    def gte(self, value, message):
        return MaxOrEqualValueValidator(value, message)

    def lt(self, value, message):
        return validators.MinValueValidator(value, message)

    def lte(self, value, message):
        return MinOrEqualValueValidator(value, message)

    def produce(self, validation):
        meth = self.maps[validation.type]
        msg = validation.message or None
        return meth(self, validation.value, msg)
