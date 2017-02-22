# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from collections import OrderedDict

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.translation import ugettext_lazy as _

import six

from formidable.models import Preset


class PresetsRegister(dict):

    def build_rules(self, form):
        return list(self.gen_rules(form))

    def gen_rules(self, form):
        for preset in form.presets.all():
            klass = self[preset.slug]
            yield klass(preset.arguments.all(), message=preset.message)


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

    def __init__(self, label, slug=None, order=None,
                 help_text='', placeholder='', items=None):
        self.slug = slug
        self.label = label
        self.help_text = help_text
        self.placeholder = placeholder
        self.types = self.get_types()
        self.has_items = items is not None
        self.items = items or {}
        self.order = order

    def get_types(self):
        return [self.__class__.type_]

    def set_slug(self, slug):
        """
        Set a slug only if the original slug is not already previously set.
        """
        if self.slug is None:
            self.slug = slug

    def get_value(self, arguments, fields):

        for arg in arguments:
            if arg.slug == self.slug:
                if arg.field_id:
                    return fields[arg.field_id]
                return arg.value

        raise ImproperlyConfigured(
            _('{slug} is missing').format(slug=self.slug)
        )

    def to_formidable(self, preset, arguments):

        for arg in arguments:
            if arg.slug == self.slug:
                arg.preset = preset
                arg.save()
                return arg

        raise ImproperlyConfigured(
            '{slug} is missing'.format(slug=self.slug)
        )


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

    def __init__(self, arguments, message=None):
        self.arguments = arguments
        self.message = message or self.default_message

    def __call__(self, cleaned_data):
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
            _('Compare to'), help_text=_('compare with'), order=1
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
