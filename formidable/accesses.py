# -*- coding: utf-8 -*-
"""
.. autofunction:: get_accesses
    members
"""
import six
import importlib

from django.conf import settings


class AccessUnknow(Exception):
    pass


class AccessObject(object):
    def __init__(self, id, label, description=''):
        self.id = id
        self.label = label
        self.description = description

    def __unicode__(self):
        return u'{}: {}'.format(self.id, self.label)


def get_accesses():
    """
    Load the method defined in the settings :attr:`ACCESS_LOADER`, and execute
    it in order to return the result.
    The method checks to ensure it returns a list of Access objects.
    """
    module, meth_name = settings.FORMIDABLE_ACCESS_RIGHTS_LOADER.rsplit(
        '.', 1
    )
    if six.PY3:
        mod = importlib.import_module(module)
    else:
        mod = importlib.import_module(module, [meth_name])
    meth = getattr(mod, meth_name)
    res = meth()
    assert type(res) == list, 'FORMIDABLE_ACCESS_RIGHTS_LOADER has to return a list'  # noqa
    for access in res:
        assert type(access) == AccessObject, u'access must be AccessObject'
    return res


def get_context(request, kwargs):
    module, meth_name = settings.FORMIDABLE_CONTEXT_LOADER.rsplit('.', 1)
    if six.PY3:
        mod = importlib.import_module(module)
    else:
        mod = importlib.import_module(module, [meth_name])
    meth = getattr(mod, meth_name)
    return meth(request, kwargs)
