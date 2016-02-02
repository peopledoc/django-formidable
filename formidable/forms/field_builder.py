# -*- coding: utf-8 -*-

from django import forms

from formidable.validators import ValidatorFactory, DateValidatorFactory
from formidable.forms import fields


class SkipField(Exception):
    pass


class FieldBuilder(object):

    widget_class = forms.TextInput
    field_class = forms.CharField
    validator_factory_class = ValidatorFactory

    def __init__(self, field):
        self.field = field
        self.validator_factory = self.validator_factory_class()

    def build(self, role=None):
        self.access = self.field.accesses.get(access_id=role) if role else None
        field_class = self.get_field_class()
        return field_class(**self.get_field_kwargs())

    def get_field_class(self):
        return self.field_class

    def get_field_kwargs(self):

        kwargs = {
            'required': self.get_required(),
            'label': self.get_label(),
            'help_text': self.get_helpText(),
            'validators': self.get_validators(),
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
        return {'attrs': self.get_widget_attrs()}

    def get_widget_attrs(self):
        return {'disabled': self.get_disabled()}

    def get_disabled(self):
        if self.access:
            return self.access.level == u'READONLY'

        return False

    def get_required(self):
        if self.access:

            if self.access.level == u'HIDDEN':
                raise SkipField()

            return self.access.level == u'REQUIRED'

        return False

    def get_label(self):
        return self.field.label

    def get_helpText(self):
        return self.field.helpText

    def get_validators(self):
        res = []
        for validation in self.field.validations.all():
            validator = self.validator_factory.produce(validation)
            res.append(validator)
        return res


class HelpTextBuilder(FieldBuilder):

    field_class = fields.HelpTextField


class TextFieldBuilder(FieldBuilder):
    pass


class ParagraphFieldBuilder(FieldBuilder):

    widget_class = forms.Textarea


class CheckboxFieldBuilder(FieldBuilder):

    widget_class = forms.CheckboxInput


class EmailFieldBuilder(FieldBuilder):

    field_class = forms.EmailField


class DateFieldBuilder(FieldBuilder):

    field_class = forms.DateField
    validator_factory_class = DateValidatorFactory


class IntegerFieldBuilder(FieldBuilder):

    field_class = forms.IntegerField


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


class CheckboxesFieldBuilder(ChoiceFieldBuilder):

    widget_class = forms.CheckboxSelectMultiple


class FormFieldFactory(object):

    field_map = {
        'text': TextFieldBuilder,
        'paragraph': ParagraphFieldBuilder,
        'dropdown': DropdownFieldBuilder,
        'checkbox': CheckboxFieldBuilder,
        'radios': RadioFieldBuilder,
        'checkboxes': CheckboxesFieldBuilder,
        'email': EmailFieldBuilder,
        'date': DateFieldBuilder,
        'number': IntegerFieldBuilder,
        'helpText': HelpTextBuilder,
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
