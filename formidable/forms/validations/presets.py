# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ValidationError, ImproperlyConfigured


class PresetsRegister(dict):

    def build_rules(self, form):
        rules = []
        for preset in form.presets.all():
            klass = self[preset.slug]
            instance = klass(preset.arguments.all())
            rules.append(instance)
        return rules


presets_register = PresetsRegister()


class PresetsMetaClass(type):
    """
    Build a new class of Presets.
    Check if all needed attribute are declared inside the class
    (slug, label, description, default_message) and Parameters
    define through MetaParameters inside class.
    Collect all object declared as arguments on put it inside a specific
    dictionary (as declared_field in django form).
    Finally, register the built class with its slug in presets_register.
    """

    def __new__(mcls, name, base, attrs):
        needs = [
            'slug', 'label', 'description', 'default_message', 'MetaParameters'
        ]
        for attr in needs:
            if attr not in attrs:
                raise ValidationError("You need to specify {} in {}".format(
                    attr, name
                ))
            if attrs[attr] is None:
                raise ValidationError(
                    "Do not accept None value for {} in {}".format(attr, name)
                )

        _declared_arguments = {}

        # Separeted the arguments to injected inside a specific dictionary
        for slug, arg in attrs['MetaParameters'].__dict__.items():
            if isinstance(arg, PresetArgument):
                arg.set_slug(slug)
                _declared_arguments[slug] = arg

        attrs['_declared_arguments'] = _declared_arguments
        klass = super(PresetsMetaClass, mcls).__new__(mcls, name, base, attrs)
        if attrs['slug']:
            presets_register[klass.slug] = klass
        return klass


class PresetArgument(object):

    def __init__(self, label, slug=None, help_text='', placeholder=''):
        self.slug = slug
        self.label = label
        self.help_text = help_text
        self.placeholder = placeholder
        self.types = self.get_types()

    def get_types(self):
        return [self.__class__.type_]

    def set_slug(self, slug):
        """
        Set a slug only if the original slug is no set before
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
            '{} is missing'.format(self.slug)
        )


class PresetFieldArgument(PresetArgument):

    type_ = 'field'


class PresetValueArgument(PresetArgument):

    type_ = 'value'


class PresetFieldOrValueArgument(PresetArgument):

    def get_types(self):
        return ['field', 'value']


class Presets(object):

    slug = ''
    label = ''
    description = ''
    default_message = ''

    __metaclass__ = PresetsMetaClass

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


class ConfirmationPresets(Presets):

    slug = 'confirmation'
    label = 'Confirmation'
    description = "Be sure two fields are exacly the same value"
    default_message = "{left} are not equals to {right}"

    class MetaParameters:
        left = PresetFieldArgument('Reference', help_text='field to compare')
        right = PresetFieldOrValueArgument(
            'Compare to', help_text='compare with'
        )

    def run(self, left, right):
        return left == right
