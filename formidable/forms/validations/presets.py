# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from collections import OrderedDict

from django.core.exceptions import (
    FieldError, ImproperlyConfigured, ValidationError
)
from django.utils.translation import ugettext_lazy as _

import six

from formidable.models import Preset, PresetArg


class PresetsRegister(dict):

    def build_rules(self, form, fields):
        return list(self.gen_rules(form, fields))

    def gen_rules(self, form, fields):
        for preset in form.presets.all():
            klass = self[preset.slug]
            try:
                yield klass(preset.arguments.all(),
                            fields=fields, message=preset.message)
            except FieldError:
                # preset defined on a field that is filtered (current role
                # does not match the accesses)
                pass

    def build_rules_from_schema(self, schema):
        rules = []
        for preset in schema.get('presets', []):
            klass = self[preset['preset_id']]
            arguments = self.get_arguments_from_schema(preset.get(
                'arguments', []
            ))
            rules.append(klass(arguments, message=preset['message']))

        return rules

    def get_arguments_from_schema(self, arguments):
        args = []
        for argument in arguments:
            args.append(PresetArg(**argument))
        return args


presets_register = PresetsRegister()


class PresetsMetaClass(type):
    """
    Build a new class of Presets.
    Check that all needed attributes are declared inside the class
    (slug, label, description, default_message) and that Parameters
    are defined through MetaParameters inside the class.
    Collect all objects declared as arguments and put them inside a specific
    dictionary (as with declared_field in a Django form).
    Finally, register the built class with its slug in presets_register.
    """

    def __new__(mcls, name, base, attrs):
        needs = [
            'slug', 'label', 'description', 'default_message', 'MetaParameters'
        ]
        for attr in needs:
            if attr not in attrs:
                raise ValidationError(
                    _("You need to specify {attr} in {name}").format(
                        attr=attr, name=name)
                )
            if attrs[attr] is None:
                raise ValidationError(
                    _("Empty value not accepted for {attr} in {name}").format(
                        attr=attr, name=name)
                )

        # Separate the arguments to inject inside a specific dictionary
        current_args = []
        for slug, arg in attrs['MetaParameters'].__dict__.items():
            if isinstance(arg, PresetArgument):
                arg.set_slug(slug)
                current_args.append((slug, arg))
        current_args.sort(key=lambda x: x[1].order)
        _declared_arguments = OrderedDict(current_args)

        attrs['_declared_arguments'] = _declared_arguments
        klass = super(PresetsMetaClass, mcls).__new__(mcls, name, base, attrs)
        if attrs['slug']:
            presets_register[klass.slug] = klass
        return klass


class PresetArgument(object):

    def __init__(self, label, slug=None, order=None, cast_value_with=None,
                 help_text='', placeholder='', items=None):
        self.slug = slug
        self.label = label
        self.help_text = help_text
        self.placeholder = placeholder
        self.types = self.get_types()
        self.has_items = items is not None
        self.items = items or {}
        self.order = order
        self.cast_value_with = cast_value_with

    def get_types(self):
        return [self.__class__.type_]

    def set_slug(self, slug):
        """
        Set a slug only if the original slug is not already previously set.
        """
        if self.slug is None:
            self.slug = slug

    def get_value(self, arguments, data):
        arg = arguments[self.slug]
        if arg.field_id:
            return data[arg.field_id]
        return arg.value

    def to_formidable(self, preset, arguments):

        arg = arguments[self.slug]
        arg.preset = preset
        arg.save()
        return arg


class PresetFieldArgument(PresetArgument):

    type_ = 'field'


class PresetValueArgument(PresetArgument):

    type_ = 'value'


class PresetFieldOrValueArgument(PresetArgument):

    def get_types(self):
        return ['field', 'value']


class Presets(six.with_metaclass(PresetsMetaClass)):

    slug = ''
    label = ''
    description = ''
    default_message = ''

    class MetaParameters:
        pass

    def __init__(self, arguments, fields=None, message=None):
        self.message = message or self.default_message
        # Check if `arguments` match `self._declared_arguments`
        decl_args_set = set(self._declared_arguments.keys())
        args_set = {a.slug for a in arguments}
        missing_args = decl_args_set - args_set
        if missing_args:
            raise ImproperlyConfigured(
                _('Missing presets arguments : {}').format(
                    ', '.join(missing_args))
                )
        extra_args = args_set - decl_args_set
        if extra_args:
            raise ImproperlyConfigured(
                _('Extra presets arguments : {}').format(
                    ', '.join(extra_args))
                )
        self.arguments = {arg.slug: arg for arg in arguments}

        if fields is not None:
            # Check if `arguments` references to fields are valid
            required_fields = {
                a.field_id
                for a in self.arguments.values()
                if a.field_id
            }
            missing_fields = required_fields - set(fields.keys())
            if missing_fields:
                raise FieldError(
                    _('Bad field references in presets : {}').format(
                        ', '.join(missing_fields))
                    )
            # Value conversions
            for arg_name, arg in self._declared_arguments.items():
                instance = self.arguments[arg_name]
                if arg.cast_value_with and instance.value is not None:
                    field_name = self.arguments[arg.cast_value_with].field_id
                    reference_field = fields[field_name]
                    instance.value = reference_field.to_python(instance.value)

    def has_empty_fields(self, cleaned_data):
        def is_empty_value(data):
            return (data is None or
                    (isinstance(data, six.string_types) and not data))

        used_fields = {a.field_id
                       for a in self.arguments.values() if a.field_id}
        # we do not filter out required fields because they can't be empty
        return any(
            is_empty_value(cleaned_data.get(name, None))
            for name in used_fields
        )

    def __call__(self, cleaned_data):
        if self.has_empty_fields(cleaned_data):
            # We skip rules using empty fields
            # If the fields were required then it is already reported in
            # form.errors. If the fields were not required, then it is not
            # useful to report an error
            return True
        kwargs = self.collect_kwargs(cleaned_data)
        if not self.run(**kwargs):
            raise ValidationError(self.get_message(kwargs))
        return True

    def collect_kwargs(self, cleaned_data):
        kwargs = {}
        for arg in self._declared_arguments.values():
            kwargs[arg.slug] = arg.get_value(self.arguments, cleaned_data)
        return kwargs

    def get_message(self, kwargs):
        return self.message.format(**kwargs)

    def to_formidable(self, form):
        preset = Preset.objects.create(
            form=form,
            slug=self.slug,
            message=self.message
        )
        for arg in self._declared_arguments.values():
            arg.to_formidable(preset, self.arguments)


class ConfirmationPresets(Presets):

    slug = 'confirmation'
    label = _('Confirmation')
    description = _("Ensure both fields are identical")
    default_message = _("{left} is not equal to {right}")

    class MetaParameters:
        left = PresetFieldArgument(
            _('Reference'), help_text=_('field to compare'), order=0
        )
        right = PresetFieldOrValueArgument(
            _('Compare to'), help_text=_('compare with'), order=1,
            cast_value_with='left'
        )

    def run(self, left, right):
        return left == right


class ComparisonPresets(Presets):

    slug = 'comparison'
    label = _('Comparison')
    description = _("Compare two fields with standard operation")
    default_message = _("{left} is not {operator} to {right}")

    mapper = {
        'eq': lambda x, y: x == y,
        'neq': lambda x, y: x != y,
        'gt': lambda x, y: x > y,
        'gte': lambda x, y: x >= y,
        'lt': lambda x, y: x < y,
        'lte': lambda x, y: x <= y,
    }

    class MetaParameters:
        left = PresetFieldArgument(_('Reference'), order=0)
        operator = PresetValueArgument(_('Operator'), items={
            'eq': '=', 'lt': '<', 'lte': '<=', 'gt': '>',
            'gte': '>=', 'neq': '!='
        }, order=1)
        right = PresetFieldArgument(_('Compare to'), order=2)

    def run(self, left, operator, right):
        meth = self.mapper[operator]
        return meth(left, right)
