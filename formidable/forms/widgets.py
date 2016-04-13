# -*- coding: utf-8 -*-

from django.forms import widgets

from markdown import markdown


class FormidableWidget(widgets.Widget):

    type_id = None
    multiple = False

    def to_formidable(self, formidable, slug, label, help_text, order):
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
            key, value = item
            field.items.create(key=key, value=value, order=order)
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

    type_id = u'checkbox'


class CheckboxSelectMultiple(ItemsWidgetMultiple,
                             widgets.CheckboxSelectMultiple):

    type_id = u'checkboxes'


class DateInput(FormidableWidget, widgets.DateInput):

    type_id = u'date'


class NumberInput(FormidableWidget, widgets.NumberInput):

    type_id = u'number'


class HelpTextWidget(FormidableWidget):

    type_id = u'help_text'

    def render(self, name, value, attrs=None):
        return markdown(value)


class TitleWidget(FormidableWidget):

    type_id = u'title'

    def __init__(self, balise='h4', *args, **kwargs):
        self.balise = balise
        super(TitleWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        balise = attrs.get('balise', None) or self.balise
        return u'<{balise}>{value}</{balise}>'.format(
            balise=balise, value=value
        )


class SeparatorWidget(FormidableWidget):

    type_id = 'separator'

    def render(self, name, value, attrs=None):
        return '<tr>'
