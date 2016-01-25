# -*- coding: utf-8 -*-

from django.forms import widgets


class FormidableWidget(widgets.Widget):

    type_id = None
    multiple = False

    def to_formidable(self, formidable, slug, label, help_text):
        return formidable.fields.create(
            slug=slug, label=label, type_id=self.type_id,
            helptext=help_text, multiple=self.multiple
        )


class TextInput(FormidableWidget, widgets.TextInput):

    type_id = 'text'


class Textarea(FormidableWidget, widgets.Textarea):

    type_id = 'paragraph'


class WidgetWithItems(FormidableWidget):

    def to_formidable(self, formidable, slug, label, help_text, items):
        field = super(WidgetWithItems, self).to_formidable(
            formidable, slug, label, help_text
        )
        for key, value in items:
            field.items.create(key=key, value=value)
        return field


class WidgetWithItemsMultiple(WidgetWithItems):

    multiple = True


class Select(WidgetWithItems, widgets.Select):

    type_id = 'dropdown'


class CheckboxInput(FormidableWidget, widgets.CheckboxInput):

    type_id = u'checkbox'
