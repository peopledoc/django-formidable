# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class PresetsRegister(dict):
    pass


presets_register = PresetsRegister()


class PresetsMetaClass(type):

    def __new__(mcls, name, base, attrs):
        klass = super(PresetsMetaClass, mcls).__new__(mcls, name, base, attrs)
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


class PresetFieldArgument(PresetArgument):

    type_ = 'field'


class PresetValueArgument(PresetArgument):

    type_ = 'value'


class PresetFieldOrValueArgument(PresetArgument):

    def get_types(self):
        return ['field', 'value']


class Presets(object):

    slug = None
    label = None
    description = None
    default_message = None

    __metaclass__ = PresetsMetaClass

    class MetaParameters(object):
        pass


class ConfirmationPresets(Presets):

    slug = 'confirmation'
    label = 'Confirmation'
    description = "Be sure two fields are exacly the same value"
    default_message = "{left} are not equals to {right}"
