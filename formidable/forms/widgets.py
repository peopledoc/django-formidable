# -*- coding: utf-8 -*-

from django.forms import widgets


class FormidableWidget(widgets.Widget):

    type_id = None

    def to_formidable(self, formidable, slug, label):
        return formidable.fields.create(
            slug=slug, label=label, type_id=self.type_id
        )


class TextInput(FormidableWidget, widgets.TextInput):

    type_id = 'text'
