# -*- coding: utf-8 -*-
"""
Generic validators, i.e. not depending on a specific field type.
"""
from __future__ import absolute_import, unicode_literals

from django.core import validators
from django.utils.translation import ugettext_lazy as _

from ._core import FormidableValidator


class GTEValidator(FormidableValidator, validators.MinValueValidator):
    """
    Validate a field value that should be greater or equal to a value.
    """
    type = 'GTE'


class LTEValidator(FormidableValidator, validators.MaxValueValidator):
    """
    Validate a field value that should be lesser or equal to a value.
    """
    type = 'LTE'


class MaxLengthValidator(FormidableValidator, validators.MaxLengthValidator):
    """
    Validate a field value that should not be longer than a value.
    """
    type = 'MAXLENGTH'


class MinLengthValidator(FormidableValidator, validators.MinLengthValidator):
    """
    Validate a field value that should not be shorter than a value.
    """
    type = 'MINLENGTH'


class RegexValidator(FormidableValidator, validators.RegexValidator):
    """
    Validate a field value that should match a given regular expression.
    """
    type = 'REGEXP'

    def get_formidable_kwargs(self):
        return {
            'type': self.type, 'value': self.regex.pattern,
            'message': self.message,
        }


class GTValidator(FormidableValidator, validators.BaseValidator):
    """
    Validate a field value that should be greater than a value.
    """
    type = 'GT'

    message = _("Ensure this field is greater than %(limit_value)s")

    def clean(self, x):
        return x

    def compare(self, cleaned, limit_value):
        return cleaned <= limit_value


class LTValidator(FormidableValidator, validators.BaseValidator):
    """
    Validate a field value that should be lesser than a value.
    """
    type = 'LT'
    message = _("Ensure this field is less than %(limit_value)s")

    def clean(self, x):
        return x

    def compare(self, cleaned, limit_value):
        return cleaned >= limit_value


class EQValidator(FormidableValidator, validators.BaseValidator):
    """
    Validate a field value that should be equals to a value.
    """
    type = 'EQ'
    message = _("Ensure this field is equal to %(limit_value)s")

    def clean(self, x):
        return x

    def compare(self, cleaned, limit_value):
        limit_value = type(cleaned)(limit_value)
        return cleaned != limit_value


class NEQValidator(FormidableValidator, validators.BaseValidator):
    """
    Validate a field value that should be different than a value.
    """
    type = 'NEQ'
    message = _("Ensure this field is not equal to %(limit_value)s")

    def clean(self, x):
        return x

    def compare(self, cleaned, limit_value):
        limit_value = type(cleaned)(limit_value)
        return cleaned == limit_value
