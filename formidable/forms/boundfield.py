# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.forms import forms


class FormatBoundField(forms.BoundField):
    """
    The format field skips the rendering with the label attribute
    in the form level (i.e => form.as_p() doesn't have to generate any label
    for format field).
    This boundfield has this main goal.
    """

    def __init__(self, *args, **kwargs):
        super(FormatBoundField, self).__init__(*args, **kwargs)
        # This attribute is used to generate (or not) the final label
        # with html tags. We force the label to None to avoid the label
        # generation:
        self.label = None


class HelpTextBoundField(FormatBoundField):

    def value(self):
        return self.field.text


class TitleBoundField(FormatBoundField):

    def value(self):
        return self.field.label


class SeparatorBoundField(FormatBoundField):

    def value(self):
        return None
