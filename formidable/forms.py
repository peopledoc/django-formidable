# -*- coding: utf-8 -*-

from django import forms


class SkipField(Exception):
    pass


class BaseDynamicForm(forms.Form):
    pass


class FieldBuilder(object):

    widget_class = None
    field_class = None

    def __init__(self, field):
        self.field = field

    def build(self, role):
        self.role = role
        field_class = self.get_field_class()
        return field_class(**self.get_field_kwargs())

    def get_field_class(self):
        return self.field_class

    def get_field_kwargs(self):
        kwargs = {
            'required': self.is_required(),
            'label': self.get_label(),
        }
        widget = self.get_widget()
        if widget:
            kwargs['widget'] = self.get_widget()
        return kwargs

    def get_widget(self):
        klass = self.get_widget_class()
        if klass:
            return klass(**self.get_widget_kwargs())
        return None

    def get_widget_class(self):
        return self.widget_class

    def is_required(self):
        return self.field.accesses.filter(
            access_id=self.role, level=u'REQUIRED'
        ).exists()

    def get_label(self):
        return self.field.label

    def get_helptext(self):
        return self.field.helptext


class TextFieldBuilder(FieldBuilder):

    field_class = forms.CharField


class FormFieldFactory(object):

    field_map = {
        'text': TextFieldBuilder,
    }

    @classmethod
    def produce(cls, field, role=None):
        """
        Given a :class:`formidable.models.Fieldidable`, the method returns
        a :class:`django.forms.Field` instance according to the type_id,
        validations and rules.
        """
        builder = cls.field_map[field.type_id](field)
        return builder.build(role)


form_field_factory = FormFieldFactory()


def get_dynamic_form_class(formidable, role=None):

    fields = {}

    for field in formidable.fields.all():
        try:
            form_field = FormFieldFactory.produce(field, role)
        except SkipField:
            pass
        else:
            fields[field.slug] = form_field

    return type('DynamicForm', (BaseDynamicForm,), fields)
