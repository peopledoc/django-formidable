# -*- coding: utf-8 -*-
"""
Validators
==========

.. autoclass: GTEValidator
    :members:

"""

from __future__ import unicode_literals

from datetime import date

from django.core import validators
from django.utils.translation import ugettext_lazy as _

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta


class FormidableValidator(object):

    def to_formidable(self, field):
        return field.validations.create(**self.get_formidable_kwargs())

    def get_formidable_kwargs(self):
        return {
            'type': self.type, 'value': self.limit_value,
            'message': self.message,
        }


class GTEValidator(FormidableValidator, validators.MinValueValidator):

    type = 'GTE'


class LTEValidator(FormidableValidator, validators.MaxValueValidator):

    type = 'LTE'


class MaxLengthValidator(FormidableValidator, validators.MaxLengthValidator):

    type = 'MAXLENGTH'


class MinLengthValidator(FormidableValidator, validators.MinLengthValidator):

    type = 'MINLENGTH'


class RegexValidator(FormidableValidator, validators.RegexValidator):

    type = 'REGEXP'

    def get_formidable_kwargs(self):
        return {
            'type': self.type, 'value': self.regex.pattern,
            'message': self.message,
        }


class GTValidator(FormidableValidator, validators.BaseValidator):

    type = 'GT'

    message = _("Ensure this field is greater than %(limit_value)s")

    def clean(self, x):
        return x

    def compare(self, cleaned, limit_value):
        return cleaned <= limit_value


class LTValidator(FormidableValidator, validators.BaseValidator):

    type = 'LT'
    message = _("Ensure this field is less than %(limit_value)s")

    def clean(self, x):
        return x

    def compare(self, cleaned, limit_value):
        return cleaned >= limit_value


class EQValidator(FormidableValidator, validators.BaseValidator):

    type = 'EQ'
    message = _("Ensure this field is equal to %(limit_value)s")

    def clean(self, x):
        return x

    def compare(self, cleaned, limit_value):
        limit_value = type(cleaned)(limit_value)
        return cleaned != limit_value


class NEQValidator(FormidableValidator, validators.BaseValidator):

    type = 'NEQ'
    message = _("Ensure this field is not equal to %(limit_value)s")

    def clean(self, x):
        return x

    def compare(self, cleaned, limit_value):
        limit_value = type(cleaned)(limit_value)
        return cleaned == limit_value


class DateValidator(FormidableValidator):

    def __init__(self, limit_value, message=None):
        return super(DateValidator, self).__init__(
            parse(limit_value).date(), message
        )


class DateGTValidator(DateValidator, GTValidator):

    type = 'GT'


class DateLTValidator(DateValidator, LTValidator):

    type = 'LT'


class DateMaxValueValidator(DateValidator, validators.MaxValueValidator):

    type = 'LTE'


class DateMinValueValidator(DateValidator, validators.MinValueValidator):

    type = 'GTE'


class DateEQValidator(DateValidator, EQValidator):

    type = 'EQ'

    def compare(self, x, y):
        return x != y


class DateNEQValidator(DateValidator, NEQValidator):

    type = 'NEQ'

    def compare(self, x, y):
        return x == y


class DateIsInFuture(FormidableValidator, validators.BaseValidator):

    type = 'IS_DATE_IN_THE_FUTURE'

    def clean(self, x):
        return x

    def compare(self, x, has_to_be_in_future):
        today = date.today()
        if has_to_be_in_future:
            return x <= today
        else:
            return x > today


class AgeAboveValidator(FormidableValidator, validators.BaseValidator):

    type = 'IS_AGE_ABOVE'

    def clean(self, birth_date):
        return relativedelta(date.today(), birth_date).years

    def compare(self, value, age):
        return value < age


class AgeUnderValidator(AgeAboveValidator):

    type = 'IS_AGE_UNDER'

    def compare(self, value, age):
        return value >= age


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
        return GTValidator(int(value), message)

    def gte(self, value, message):
        return validators.MinValueValidator(int(value), message)

    def lt(self, value, message):
        return LTValidator(int(value), message)

    def lte(self, value, message):
        return validators.MaxValueValidator(int(value), message)

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
