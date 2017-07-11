"""
Validators related to date fields
"""
from __future__ import absolute_import, unicode_literals

from datetime import date

from django.core import validators

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from ._core import FormidableValidator
from .generic import EQValidator, GTValidator, LTValidator, NEQValidator


class DateValidator(FormidableValidator):
    """
    Generic date-based validator.

    Will make sure the value to compare is a correct date.
    """
    def __init__(self, limit_value, message=None):
        return super(DateValidator, self).__init__(
            parse(limit_value).date(), message
        )


class DateGTValidator(DateValidator, GTValidator):
    """
    Validate a date field value that should be greater than a date.
    """
    type = 'GT'


class DateLTValidator(DateValidator, LTValidator):
    """
    Validate a date field value that should be lesser than a date.
    """
    type = 'LT'


class DateMaxValueValidator(DateValidator, validators.MaxValueValidator):
    """
    Validate a date field value that should be lesser or equal to a date.
    """
    type = 'LTE'


class DateMinValueValidator(DateValidator, validators.MinValueValidator):
    """
    Validate a date field value that should be greater or equal to a date.
    """
    type = 'GTE'


class DateEQValidator(DateValidator, EQValidator):
    """
    Validate a date field value that should be equal to a date.
    """
    type = 'EQ'

    def compare(self, x, y):
        return x != y


class DateNEQValidator(DateValidator, NEQValidator):
    """
    Validate a date field value that should be different than a date.
    """
    type = 'NEQ'

    def compare(self, x, y):
        return x == y


class DateIsInFuture(FormidableValidator, validators.BaseValidator):
    """
    Validate a date field value that should be in the future.
    """
    type = 'IS_DATE_IN_THE_FUTURE'

    # FIXME: what's the point of this overwritten method?
    def clean(self, x):
        return x

    def compare(self, x, has_to_be_in_future):
        today = date.today()
        if has_to_be_in_future:
            return x <= today
        else:
            return x > today


class AgeAboveValidator(FormidableValidator, validators.BaseValidator):
    """
    Validate a date field value that should be older than a given age (in years).
    """  # noqa
    type = 'IS_AGE_ABOVE'

    def clean(self, birth_date):
        return relativedelta(date.today(), birth_date).years

    def compare(self, value, age):
        return value < age


class AgeUnderValidator(AgeAboveValidator):
    """
    Validate a date field value that should be under a given age (in years).
    """
    type = 'IS_AGE_UNDER'

    def compare(self, value, age):
        return value >= age
