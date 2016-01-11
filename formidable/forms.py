# -*- coding: utf-8 -*-

from django import forms


class SkipField(Exception):
    pass


class BaseDynamicForm(forms.Form):
    pass


class FieldBuilder(object):

    widget_class = None
    field_class = forms.CharField

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
            'required': self.get_required(),
            'label': self.get_label(),
            'help_text': self.get_helptext(),
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

    def get_widget_kwargs(self):
        return {}

    def get_required(self):
        if self.role is None:
            return False

        access = self.field.accesses.get(access_id=self.role)

        if access.level == u'HIDDEN':
            raise SkipField()

        return access.level == u'REQUIRED'

    def get_label(self):
        return self.field.label

    def get_helptext(self):
        return self.field.helptext


class TextFieldBuilder(FieldBuilder):
    pass


class ParagraphFieldBuilder(FieldBuilder):

    widget_class = forms.Textarea


class CheckboxFieldBuilder(FieldBuilder):

    widget_class = forms.CheckboxInput


class ChoiceFieldBuilder(FieldBuilder):

    field_class = forms.ChoiceField

    def get_field_kwargs(self):
        kwargs = super(ChoiceFieldBuilder, self).get_field_kwargs()
        kwargs['choices'] = self.get_choices()
        return kwargs

    def get_choices(self):
        return [(item.key, item.value) for item in self.field.items.all()]


class DropdownFieldBuilder(ChoiceFieldBuilder):

    widget_class = forms.Select

    def get_widget_class(self):
        if self.field.multiple:
            return forms.SelectMultiple
        return super(DropdownFieldBuilder, self).get_widget_class()


class RadioFieldBuilder(ChoiceFieldBuilder):

    widget_class = forms.RadioSelect


class FormFieldFactory(object):

    field_map = {
        'text': TextFieldBuilder,
        'paragraph': ParagraphFieldBuilder,
        'dropdown': DropdownFieldBuilder,
        'checkbox': CheckboxFieldBuilder,
        'radios': RadioFieldBuilder,
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