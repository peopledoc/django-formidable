# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms

from formidable.forms import fields
from formidable.validators import DateValidatorFactory, ValidatorFactory


class SkipField(Exception):
    pass


class FieldBuilder(object):

    field_class = forms.CharField
    widget_class = None
    validator_factory_class = ValidatorFactory

    def __init__(self, field):
        self.field = field
        self.validator_factory = self.validator_factory_class()

    def build(self, role=None):
        self.access = self.get_accesses(role)
        field_class = self.get_field_class()
        return field_class(**self.get_field_kwargs())

    def get_accesses(self, role):
        if role:
            # The role is previously "prefetch" in order to avoid database
            # hit, we don't use a get() method in queryset.
            return self.field.accesses.all()[0]
        return None

    def get_field_class(self):
        return self.field_class

    def get_field_kwargs(self):

        kwargs = {
            'required': self.get_required(),
            'label': self.get_label(),
            'help_text': self.get_help_text(),
            'validators': self.get_validators(),
        }

        widget = self.get_widget()

        if widget:
            kwargs['widget'] = self.get_widget()

        return kwargs

    def get_widget(self):
        widget_class = self.get_widget_class()
        if widget_class:
            return widget_class(**self.get_widget_kwargs())
        return None

    def get_widget_class(self):
        return self.widget_class

    def get_widget_kwargs(self):
        return {'attrs': self.get_widget_attrs()}

    def get_widget_attrs(self):
        attrs = {}

        if self.get_disabled():
            attrs['disabled'] = True

        return attrs

    def get_disabled(self):
        if self.access:
            return self.access.level == 'READONLY'

        return False

    def get_required(self):
        if self.access:

            if self.access.level == 'HIDDEN':
                raise SkipField()

            return self.access.level == 'REQUIRED'

        return False

    def get_label(self):
        return self.field.label

    def get_help_text(self):
        return self.field.help_text

    def get_validators(self):
        return list(self.gen_validators())

    def gen_validators(self):
        for validation in self.get_validations():
            yield self.validator_factory.produce(validation)

    def get_validations(self):
        """
        return iterator over field validation
        """
        return self.field.validations.all()


class FileFieldBuilder(FieldBuilder):

    field_class = forms.FileField


class HelpTextBuilder(FieldBuilder):

    field_class = fields.HelpTextField

    def get_field_kwargs(self):
        kwargs = super(HelpTextBuilder, self).get_field_kwargs()
        kwargs['text'] = kwargs.pop('help_text')
        return kwargs


class TitleFielBuilder(FieldBuilder):

    field_class = fields.TitleField


class SeparatorBuilder(FieldBuilder):

    field_class = fields.SeparatorField


class TextFieldBuilder(FieldBuilder):

    widget_class = forms.TextInput


class ParagraphFieldBuilder(FieldBuilder):

    widget_class = forms.Textarea


class CheckboxFieldBuilder(FieldBuilder):

    field_class = forms.BooleanField


class EmailFieldBuilder(FieldBuilder):

    field_class = forms.EmailField


class DateFieldBuilder(FieldBuilder):

    field_class = forms.DateField
    validator_factory_class = DateValidatorFactory


class NumberFieldBuilder(FieldBuilder):

    field_class = forms.DecimalField


class ChoiceFieldBuilder(FieldBuilder):

    field_class = forms.ChoiceField

    def get_field_kwargs(self):
        kwargs = super(ChoiceFieldBuilder, self).get_field_kwargs()
        kwargs['choices'] = self.get_choices()
        return kwargs

    def get_choices(self):
        return [(item.value, item.label) for item in self.field.items.all()]


class DropdownFieldBuilder(ChoiceFieldBuilder):

    widget_class = forms.Select

    def get_field_class(self):
        if self.field.multiple:
            return forms.MultipleChoiceField
        return super(DropdownFieldBuilder, self).get_field_class()

    def get_widget_class(self):
        if self.field.multiple:
            return forms.SelectMultiple
        return super(DropdownFieldBuilder, self).get_widget_class()


class RadioFieldBuilder(ChoiceFieldBuilder):

    widget_class = forms.RadioSelect


class CheckboxesFieldBuilder(ChoiceFieldBuilder):

    field_class = forms.MultipleChoiceField
    widget_class = forms.CheckboxSelectMultiple


class FormFieldFactory(object):

    field_map = {
        'text': TextFieldBuilder,
        'paragraph': ParagraphFieldBuilder,
        'dropdown': DropdownFieldBuilder,
        'checkbox': CheckboxFieldBuilder,
        'radios': RadioFieldBuilder,
        'radios_buttons': RadioFieldBuilder,
        'checkboxes': CheckboxesFieldBuilder,
        'email': EmailFieldBuilder,
        'date': DateFieldBuilder,
        'number': NumberFieldBuilder,
        'help_text': HelpTextBuilder,
        'title': TitleFielBuilder,
        'separator': SeparatorBuilder,
        'file': FileFieldBuilder,
    }

    def __init__(self, field_map=None):
        self.map = self.field_map.copy()
        self.map.update(field_map or {})

    def produce(self, field, role=None):
        """
        Given a :class:`formidable.models.Fieldidable`, return a
        :class:`django.forms.Field` instance according to the type_id,
        validations and rules.
        """
        type_id = self.get_type_id(field)
        builder = self.map[type_id](field)
        return builder.build(role)

    def get_type_id(self, field):
        return field.type_id


form_field_factory = FormFieldFactory()
