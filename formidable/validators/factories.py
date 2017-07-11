# -*- coding: utf-8 -*-
"""
Validator factories will be used in a field-builder context.
"""
from __future__ import absolute_import, unicode_literals

from decimal import Decimal

from django.core import validators

from .date import (
    AgeAboveValidator, AgeUnderValidator, DateEQValidator, DateGTValidator,
    DateIsInFuture, DateLTValidator, DateMaxValueValidator,
    DateMinValueValidator, DateNEQValidator
)
from .generic import EQValidator, GTValidator, LTValidator, NEQValidator


class ValidatorFactory(object):
    """
    Generic validator factory.

    It's used in a generic field builder context.
    It'll describe the available validators for this field and will map their
    types with the appropriate method, which will call instantiate the
    appropriate Validator object.
    """
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
        limit_value = Decimal(limit_value)
        return validators.MinLengthValidator(limit_value, message)

    def max_length(self, limit_value, message):
        limit_value = Decimal(limit_value)
        return validators.MaxLengthValidator(limit_value, message)

    def regexp(self, value, message):
        return validators.RegexValidator(regex=value, message=message)

    def gt(self, value, message):
        return GTValidator(Decimal(value), message)

    def gte(self, value, message):
        return validators.MinValueValidator(Decimal(value), message)

    def lt(self, value, message):
        return LTValidator(Decimal(value), message)

    def lte(self, value, message):
        return validators.MaxValueValidator(Decimal(value), message)

    def eq(self, value, message):
        return EQValidator(value, message)

    def neq(self, value, message):
        return NEQValidator(value, message)

    def produce(self, validation):
        type_, msg, value = self.extract_validation_attribute(validation)
        meth = self.maps[type_]
        return meth(self, value, msg)

    def extract_validation_attribute(self, validation):
        """
        Return the tuple of validation type, validation msg, validation value
        """
        return validation.type, validation.message or None, validation.value


class DateValidatorFactory(ValidatorFactory):
    """
    Date validator factory.

    It's used in a date-based field builder context.

    It'll work exactly like :class:`ValidatorFactory`, except that it'll:

    * add date-specific validators,
    * overwrite some validation methods using date-specific validators.
    """

    maps = ValidatorFactory.maps.copy()
    maps['IS_DATE_IN_THE_FUTURE'] = lambda self, x, y=None: self.future_date(
        x, y
    )
    maps['IS_AGE_ABOVE'] = lambda self, x, y=None: self.age_above(x, y)
    maps['IS_AGE_UNDER'] = lambda self, x, y=None: self.age_under(x, y)

    def lt(self, value, message):
        return DateLTValidator(value, message)

    def lte(self, value, message):
        return DateMaxValueValidator(value, message)

    def gt(self, value, message):
        return DateGTValidator(value, message)

    def gte(self, value, message):
        return DateMinValueValidator(value, message)

    def eq(self, value, message):
        return DateEQValidator(value, message)

    def neq(self, value, message):
        return DateNEQValidator(value, message)

    def future_date(self, value, message):
        return DateIsInFuture(value.lower() == 'true', message)

    def age_above(self, value, message):
        return AgeAboveValidator(int(value), message)

    def age_under(self, value, message):
        return AgeUnderValidator(int(value), message)
