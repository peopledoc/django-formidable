# -*- coding: utf-8 -*-
"""
This module provides custom form fields in order to define a Formidable
object, as with a standard django form.

You can find most of the standard django fields :

.. autoclass:: CharField
    :members:

.. autoclass:: BooleanField
    :members:

.. autoclass:: NumberField
    :members:

.. autoclass:: FileField
    :members:

.. autoclass:: DateField
    :members:

.. autoclass:: MultipleChoiceField
    :members:

.. autoclass:: ChoiceField
    :members:


Extra fields are allowed to use with FormidableForm, the Format Field. These
kinds of fields allow us to define format inside the form:

.. autoclass:: TitleField

    Add a title inside the rendering.

.. autoclass:: HelpTextField

    Add a description inside the form, to comment a block of inputs or
    just to add some text.

.. autoclass:: SeparatorField

    Add separators between fields to separate blocks of fields, for example.

Each field comes with its own widget class. Via these classes, the type of
fields they deal with can be specified. If you want to override any with
your own fields, please look at :mod:`formidable.forms.widgets`.

"""

from __future__ import unicode_literals

from django.forms import fields

from formidable.accesses import get_accesses
from formidable.constants import EDITABLE
from formidable.exceptions import UnknownAccess
from formidable.forms import boundfield, widgets


class Field(object):

    widget = widgets.TextInput

    def __init__(self, accesses=None, default=None, *args, **kwargs):
        self.defaults = [default] if default is not None else []
        self.accesses = accesses or {}
        super(Field, self).__init__(*args, **kwargs)

    def to_formidable(self, form, order, slug):
        # First thing, check accesses are correct.
        self.check_accesses()
        # Generate kwargs for create fields
        label = self.label or slug
        kwargs = {
            'formidable': form, 'slug': slug, 'label': label,
            'help_text': self.help_text, 'order': order,
        }
        kwargs.update(self.get_extra_formidable_kwargs())
        widget = self.get_widget()
        field = widget.to_formidable(**kwargs)
        self.create_accesses(field)
        self.create_validators(field)
        self.create_defaults(field)
        return field

    def create_accesses(self, field):
        for access, level in self.get_complete_accesses().items():
            field.accesses.create(access_id=access, level=level)

    def create_defaults(self, field):
        for default in self.defaults:
            field.defaults.create(value=default)

    def create_validators(self, field):
        for validator in self.validators:
            if hasattr(validator, 'to_formidable'):
                validator.to_formidable(field)

    def get_complete_accesses(self):
        """
        Return an access dict with all the access-rights defined by the client.
        If access-rights are missing in the :attr:`accesses` they will be added
        with a default value of `EDITABLE`.
        If the access-right is unknown, an exception will be raised.
        """
        accesses = {}
        for access in get_accesses():
            if access.id not in self.accesses.keys():
                accesses[access.id] = EDITABLE
            else:
                accesses[access.id] = self.accesses[access.id]
        return accesses

    def check_accesses(self):
        accesses_id = [access.id for access in get_accesses()]
        for access in self.accesses.keys():
            if access not in accesses_id:
                raise UnknownAccess(access)

    def get_widget(self):
        return self.widget

    def get_extra_formidable_kwargs(self):
        return {}


class FormatField(Field, fields.Field):
    """
    Handles display information inside the form.

    The help_text attribute is removed automatically to handle display.

    The get_bound_field is defined here (must be implemented in a child class).
    The bound field is used to return the correct value to display.

    Normally, if help_text exists it's rendered inside a <span> tag,
    and labels are rendered in <label> tags.

    To avoid this, we override the label and the help_text attributes,
    setting them to blank values.
    """

    def __init__(self, *args, **kwargs):
        kwargs['help_text'] = ''
        super(FormatField, self).__init__(*args, **kwargs)


class HelpTextField(FormatField, fields.Field):
    """
    The help text field is just a field to show some text formatted in
    markdown (implemented in the render widget).
    Due to the method :meth:`Form._html_output`, we cannot override the
    mechanism to render the field correctly.
    """

    widget = widgets.HelpTextWidget

    def __init__(self, text, *args, **kwargs):
        self.text = text
        super(HelpTextField, self).__init__(*args, **kwargs)

    def get_bound_field(self, form, name):
        return boundfield.HelpTextBoundField(form, self, name)

    def get_extra_formidable_kwargs(self):
        return {'help_text': self.text}


class TitleField(Field, fields.Field):

    widget = widgets.TitleWidget

    def get_bound_field(self, form, name):
        return boundfield.TitleBoundField(form, self, name)


class SeparatorField(FormatField, fields.Field):

    widget = widgets.SeparatorWidget

    def get_bound_field(self, form, name):
        return boundfield.SeparatorBoundField(form, self, name)


class CharField(Field, fields.CharField):
    pass


class BooleanField(Field, fields.BooleanField):

    widget = widgets.CheckboxInput


class DateField(Field, fields.DateField):

    widget = widgets.DateInput


class NumberField(Field, fields.DecimalField):

    widget = widgets.NumberInput


class EmailField(Field, fields.EmailField):

    widget = widgets.EmailInput


class ItemField(Field):

    def __init__(self, defaults=None, *args, **kwargs):
        super(ItemField, self).__init__(*args, **kwargs)
        self.defaults = defaults or []

    def get_extra_formidable_kwargs(self):
        kwargs = super(ItemField, self).get_extra_formidable_kwargs()
        kwargs['items'] = self.choices
        return kwargs


class ChoiceField(ItemField, fields.ChoiceField):

    widget = widgets.Select


class MultipleChoiceField(ItemField, fields.MultipleChoiceField):

    widget = widgets.SelectMultiple


class FileField(Field, fields.FileField):

    widget = widgets.ClearableFileInput
