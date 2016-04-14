# -*- coding: utf-8 -*-

from django.forms import fields

from formidable.forms import widgets, boundfield
from formidable.accesses import get_accesses, AccessUnknow


class Field(object):

    widget = widgets.TextInput

    def __init__(self, accesses=None, *args, **kwargs):
        self.accesses = accesses or {}
        super(Field, self).__init__(*args, **kwargs)

    def to_formidable(self, form, order, slug):
        # First thing, check accesses are correct.
        self.check_accesses()
        # Generate kwargs for create fields
        label = self.label or slug
        kwargs = {
            'formidable': form, 'slug': slug, 'label': label,
            'help_text': self.help_text, 'order': order,
        }
        kwargs.update(self.get_extra_formidable_kwargs())
        widget = self.get_widget()
        field = widget.to_formidable(**kwargs)
        self.create_accesses(field)
        self.create_validators(field)
        return field

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


class FormatField(Field, fields.Field):
    """
    Format Field just here to handle display information inside the form.
    The help_text attribut is removed automatically to handle a display.

    The get_bound_field is define here (has to be implemented in daughter
    class). Basically, the bound field is here just to retur the good
    value to display.


    In deed, in the method, if help_text exists it's render under a <span>
    balise, and the label under <label> balise.
    We don't want something like that.
    To avoid this, we override the label and the help_text attribut,
    to it at None value.
    """

    def __init__(self, *args, **kwargs):
        kwargs['help_text'] = ''
        super(FormatField, self).__init__(*args, **kwargs)


class HelpTextField(FormatField, fields.Field):
    """
    The help text field is just a field to show some text formatted in
    markdown (implemented in the render widget).
    Du to the method :meth:`Form._html_output`, we cannot override the
    mechanism  to render the field correctly.
    """

    widget = widgets.HelpTextWidget

    def __init__(self, text, *args, **kwargs):
        self.text = text
        super(HelpTextField, self).__init__(*args, **kwargs)

    def get_bound_field(self, form, name):
        return boundfield.HelpTextBoundField(form, self, name)

    def get_extra_formidable_kwargs(self):
        return {'help_text': self.text}


class TitleField(Field, fields.Field):

    widget = widgets.TitleWidget

    def get_bound_field(self, form, name):
        return boundfield.TitleBoundField(form, self, name)


class SeparatorField(FormatField, fields.Field):

    widget = widgets.SeparatorWidget

    def get_bound_field(self, form, name):
        return boundfield.SeparatorBoundField(form, self, name)


class CharField(Field, fields.CharField):
    pass


class BooleanField(Field, fields.BooleanField):

    widget = widgets.CheckboxInput


class DateField(Field, fields.DateField):

    widget = widgets.DateInput


class IntegerField(Field, fields.IntegerField):

    widget = widgets.NumberInput


class ItemField(Field):

    def get_extra_formidable_kwargs(self):
        kwargs = super(ItemField, self).get_extra_formidable_kwargs()
        kwargs['items'] = self.choices
        return kwargs


class ChoiceField(ItemField, fields.ChoiceField):

    widget = widgets.Select


class MultipleChoiceField(ItemField, fields.MultipleChoiceField):

    widget = widgets.SelectMultiple


class FileField(Field, fields.FileField):

    widget = widgets.ClearableFileInput
