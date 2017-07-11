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

    type = 'IS_AGE_ABOVE'

    def clean(self, birth_date):
        return relativedelta(date.today(), birth_date).years

    def compare(self, value, age):
        return value < age


class AgeUnderValidator(AgeAboveValidator):

    type = 'IS_AGE_UNDER'

    def compare(self, value, age):
        return value >= age
