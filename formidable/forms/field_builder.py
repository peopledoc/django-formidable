# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from formidable.forms import fields
from formidable.utils import import_object
from formidable.validators import DateValidatorFactory, ValidatorFactory


class SkipField(Exception):
    pass


class FieldBuilder(object):
    field_class = forms.CharField
    widget_class = None
    validator_factory_class = ValidatorFactory

    def __init__(self, field):
        self.field = field
        # used to detect a field type (dict or a Django model)
        # and chose how to get properties (e.g. field.label or field['label'])
        self.field_is_dict = isinstance(field, dict)
        self.validator_factory = self.validator_factory_class()

    def build(self, role=None):
        self.access = self.get_accesses(role)
        field_class = self.get_field_class()

        if self.field_is_dict:
            params = self.field.get('parameters')
        else:
            params = getattr(self.field, 'parameters', None)

        instance = field_class(**self.get_field_kwargs(
            default_widget_class=field_class.widget))

        if params:
            setattr(instance, '__formidable_field_parameters', params)
        return instance

    def get_accesses(self, role):
        if role and not self.field_is_dict:
            # The role is previously "prefetch" in order to avoid database
            # hit, we don't use a get() method in queryset.
            qs = self.field.accesses.all()
            if len(qs):
                return qs[0]
        return None

    def get_field_class(self):
        return self.field_class

    def get_field_kwargs(self, default_widget_class):

        kwargs = {
            'required': self.get_required(),
            'label': self.get_label(),
            'help_text': self.get_help_text(),
            'validators': self.get_validators(),
            'disabled': self.get_disabled(),
        }

        kwargs['widget'] = self.get_widget(default_widget_class)

        return kwargs

    def get_widget(self, default_widget_class):
        widget_class = self.get_widget_class() or default_widget_class
        return widget_class(**self.get_widget_kwargs())

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
        if self.field_is_dict:
            return self.field.get('disabled', False)

        if self.access:
            return self.access.level == 'READONLY'

        return False

    def get_required(self):
        if self.field_is_dict:
            return self.field['required']

        if self.access:
            if self.access.level == 'HIDDEN':
                raise SkipField()
            return self.access.level == 'REQUIRED'

        return False

    def get_label(self):
        if self.field_is_dict:
            return self.field.get('label')
        return self.field.label

    def get_help_text(self):
        if self.field_is_dict:
            return self.field.get('description', '')
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
        if self.field_is_dict:
            return self.field['validations']
        return self.field.validations.all()


class FileFieldBuilder(FieldBuilder):

    field_class = forms.FileField


class HelpTextBuilder(FieldBuilder):

    field_class = fields.HelpTextField

    def get_field_kwargs(self, default_widget_class):
        kwargs = super(HelpTextBuilder, self).get_field_kwargs(
            default_widget_class
        )
        kwargs['text'] = kwargs.pop('help_text')
        return kwargs


class TitleFieldBuilder(FieldBuilder):

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

    def get_field_kwargs(self, default_widget_class):
        kwargs = super(ChoiceFieldBuilder, self).get_field_kwargs(
            default_widget_class
        )
        kwargs['choices'] = self.get_choices()
        return kwargs

    def get_choices(self):
        if self.field_is_dict:
            for item in self.field.get('items', []):
                yield item['value'], item['label']
        else:
            for item in self.field.items.all():
                yield item.value, item.label


class DropdownFieldBuilder(ChoiceFieldBuilder):

    widget_class = forms.Select

    @property
    def is_multiple(self):
        """
        Return True if dropdown field is multiple
        (works for the ORM object and the dict)
        :return: bool
        """
        return (self.field['multiple']
                if self.field_is_dict else self.field.multiple)

    def get_field_class(self):
        if self.is_multiple:
            return forms.MultipleChoiceField
        return super(DropdownFieldBuilder, self).get_field_class()

    def get_widget_class(self):
        if self.is_multiple:
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
        'title': TitleFieldBuilder,
        'separator': SeparatorBuilder,
        'file': FileFieldBuilder,
    }

    def __init__(self, field_map=None):
        self.map = self.field_map.copy()
        self.add_extra_fields()
        self.map.update(field_map or {})

    def add_extra_fields(self):
        # If the settings is not set, skip this step.
        if not hasattr(settings, 'FORMIDABLE_EXTERNAL_FIELD_BUILDERS'):
            return
        extra = getattr(settings, 'FORMIDABLE_EXTERNAL_FIELD_BUILDERS', {})
        # If empty or None
        if not extra:
            return

        for key, classpath in extra.items():
            field_builder_class = import_object(classpath)
            if not issubclass(field_builder_class, FieldBuilder):
                raise ImproperlyConfigured(
                    "{} is not of a subclass of `FieldBuiler`".format(
                        classpath))
            self.map[key] = field_builder_class

    def produce(self, field, role=None):
        """
        Given a :class:`formidable.models.Field`, return a
        :class:`django.forms.Field` instance according to the type_id,
        validations and rules.
        """
        type_id = self.get_type_id(field)
        builder = self.map[type_id](field)
        return builder.build(role)

    def get_type_id(self, field):
        if isinstance(field, dict):
            return field['type_id']
        return field.type_id


form_field_factory = FormFieldFactory()
