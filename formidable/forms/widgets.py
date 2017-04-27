# -*- coding: utf-8 -*-
"""
Most of Django's widgets are defined here. These widgets are usable with
any fields defined in :mod:`formidable.forms.fields`. These widgets are here
in order to use with :class:`formidable.forms.FormidableForm` declaration.
Do not use them directly as normal widgets for rendering!

The main goal of the Widget class declaration is to provide a reliable type
of associated field.


.. autoclass:: FormidableWidget
    :members:

.. autoclass:: TextInput

.. autoclass:: Textarea

.. autoclass:: ItemsWidget

.. autoclass:: ItemsWidgetMultiple

.. autoclass:: Select

.. autoclass:: RadioSelect

.. autoclass:: SelectMultiple

.. autoclass:: CheckboxInput

.. autoclass:: CheckboxSelectMultiple

.. autoclass:: DateInput

.. autoclass:: NumberInput

.. autoclass:: ClearableFileInput

.. autoclass:: SeparatorWidget

.. autoclass:: TitleWidget

.. autoclass:: HelpTextWidget

"""

from __future__ import unicode_literals

from django.forms import widgets

from markdown import markdown


class FormidableWidget(widgets.Widget):
    """
    Base Widget definition, implements the basic method to create a field in a
    database, associated with a form.
    """

    type_id = None
    """define the type of the field """
    multiple = False
    """ If true, the widget is multiple selection items """

    def to_formidable(self, formidable, slug, label, help_text, order):
        """
        Create an association in database with the formidable reference object.
        :attr:`slug`, :attr:`label`, :attr:`help_text` come from the
        :class:`formidable.forms.fields.Field` associated object.
        """
        return formidable.fields.create(
            slug=slug, label=label, type_id=self.type_id,
            help_text=help_text, multiple=self.multiple,
            order=order
        )


class TextInput(FormidableWidget, widgets.TextInput):

    type_id = 'text'


class Textarea(FormidableWidget, widgets.Textarea):

    type_id = 'paragraph'


class ItemsWidget(FormidableWidget):

    def to_formidable(self, formidable, slug, label, help_text, order, items):
        field = super(ItemsWidget, self).to_formidable(
            formidable, slug, label, help_text, order
        )
        for order, item in enumerate(items):
            value, label = item
            field.items.create(value=value, label=label, order=order)
        return field


class ItemsWidgetMultiple(ItemsWidget):

    multiple = True


class Select(ItemsWidget, widgets.Select):

    type_id = 'dropdown'


class RadioSelect(ItemsWidget, widgets.RadioSelect):

    type_id = 'radios'


class SelectMultiple(ItemsWidgetMultiple, widgets.SelectMultiple):

    type_id = 'dropdown'


class CheckboxInput(FormidableWidget, widgets.CheckboxInput):

    type_id = 'checkbox'


class CheckboxSelectMultiple(ItemsWidgetMultiple,
                             widgets.CheckboxSelectMultiple):

    type_id = 'checkboxes'


class DateInput(FormidableWidget, widgets.DateInput):

    type_id = 'date'


class NumberInput(FormidableWidget, widgets.NumberInput):

    type_id = 'number'


class EmailInput(FormidableWidget, widgets.EmailInput):

    type_id = 'email'


class ClearableFileInput(FormidableWidget, widgets.ClearableFileInput):

    type_id = 'file'


class HelpTextWidget(FormidableWidget):

    type_id = 'help_text'
    input_type = 'help_text'

    def render(self, name, value, attrs=None):
        return markdown(value)


class TitleWidget(FormidableWidget):

    type_id = 'title'
    input_type = 'title'

    def __init__(self, tag='h4', *args, **kwargs):
        self.tag = tag
        super(TitleWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        tag = attrs.get('tag', None) or self.tag
        return '<{tag}>{value}</{tag}>'.format(
            tag=tag, value=value
        )


class SeparatorWidget(FormidableWidget):

    type_id = 'separator'
    input_type = 'separator'

    def render(self, name, value, attrs=None):
        return '<hr>'
