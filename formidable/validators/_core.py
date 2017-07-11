# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class FormidableValidator(object):
    """
    Core Formidable validator object
    """
    def to_formidable(self, field):
        return field.validations.create(**self.get_formidable_kwargs())

    def get_formidable_kwargs(self):
        """
        Return kewords arguments for validator ``create`` function.
        """
        return {
            'type': self.type, 'value': self.limit_value,
            'message': self.message,
        }
