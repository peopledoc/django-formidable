# -*- coding: utf-8 -*-
"""
.. autofunction:: get_accesses
    members
"""
import importlib

from django.conf import settings


class AccessObject(object):
    def __init__(self, id, label, description=''):
        self.id = id
        self.label = label
        self.description = description

    def __unicode__(self):
        return u'{}: {}'.format(self.id, self.label)


def get_accesses():
    """
    Load the method defined in the settings :attr:`ACCESS_LOADER`, and excute
    it in order to return the result.
    The method has to return a list of Access object, the method check that.
    """
    module, meth_name = settings.FORMIDABLE_ACCESSES_LOADER.rsplit('.', 1)
    mod = importlib.import_module(module, [meth_name])
    meth = getattr(mod, meth_name)
    res = meth()
    assert type(res) == list, u'FORMIDABLE_ACCESS_LOADER has to return a list'
    for access in res:
        assert type(access) == AccessObject, u'access must be AccessObject'
    return res
