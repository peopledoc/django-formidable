# -*- coding: utf-8 -*-

from django.forms import fields

from formidable.forms import widgets
from formidable.accesses import get_accesses, AccessUnknow


class Field(object):

    widget = widgets.TextInput

    def __init__(self, accesses=None, *args, **kwargs):
        self.accesses = accesses or {}
        super(Field, self).__init__(*args, **kwargs)

    def to_formidable(self, form, slug):
        # First thing, check accesses are correct.
        self.check_accesses()
        # Generate kwargs for create fields
        label = self.label or slug
        kwargs = {
            'formidable': form, 'slug': slug, 'label': label,
            'help_text': self.help_text,
        }
        kwargs.update(self.get_extra_formidable_kwargs())
        widget = self.get_widget()
        field = widget.to_formidable(**kwargs)
        self.create_accesses(field)
        self.create_validators(field)

    def create_accesses(self, field):
        for access, level in self.get_complete_accesses().items():
            field.accesses.create(access_id=access, level=level)

    def create_validators(self, field):
        for validator in self.validators:
            if hasattr(validator, 'to_formidable'):
                validator.to_formidable(field)

    def get_complete_accesses(self):
        """
        Return a access dict with all the access defines by client.
        If access is missing in the :attr:`accesses` it will be added
        with default value `EDITABLE`.
        If access is unknow an exception is raised.
        """
        accesses = {}
        for access in get_accesses():
            if access.id not in self.accesses.keys():
                accesses[access.id] = u'EDITABLE'
            else:
                accesses[access.id] = self.accesses[access.id]
        return accesses

    def check_accesses(self):
        accesses_id = [access.id for access in get_accesses()]
        for access in self.accesses.keys():
            if access not in accesses_id:
                raise AccessUnknow(access)

    def get_widget(self):
        return self.widget

    def get_extra_formidable_kwargs(self):
        return {}


class HelpTextField(Field, fields.Field):

    widget = widgets.HelpTextWidget

    def __init__(self, help_text, *args, **kwargs):
        kwargs['label'] = ''
        kwargs['help_text'] = help_text
        super(HelpTextField, self).__init__(*args, **kwargs)

    def prepare_value(self, *args):
        return self.help_text


class CharField(Field, fields.CharField):
    pass


class ItemField(Field):

    def get_extra_formidable_kwargs(self):
        kwargs = super(ItemField, self).get_extra_formidable_kwargs()
        kwargs['items'] = self.choices
        return kwargs


class ChoiceField(ItemField, fields.ChoiceField):

    widget = widgets.Select


class MultipleChoiceField(ItemField, fields.MultipleChoiceField):

    widget = widgets.SelectMultiple


class BooleanField(Field, fields.BooleanField):

    widget = widgets.CheckboxInput


class DateField(Field, fields.DateField):

    widget = widgets.DateInput


class IntegerField(Field, fields.IntegerField):

    widget = widgets.NumberInput
