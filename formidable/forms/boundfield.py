# -*- coding: utf-* -*-

from django.forms import forms


class FormatBoundField(forms.BoundField):
    """
    The format field skip completly the rendering with the label attribut
    in the form level (i.e => form.as_p() doesn't have to generate any label
    for format field).
    This boundfield has this main goal.
    """

    def __init__(self, *args, **kwargs):
        super(FormatBoundField, self).__init__(*args, **kwargs)
        # This attribut is used to generated (or not) the final label
        # with html balise. We force the label to None to avoid the label
        # generation
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
