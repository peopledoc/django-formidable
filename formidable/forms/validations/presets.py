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

    def __init__(self, definition):
        self.definition = "youhou"
