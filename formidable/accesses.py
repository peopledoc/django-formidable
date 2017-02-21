# -*- coding: utf-8 -*-
"""
.. autofunction:: get_accesses
    members
"""

from __future__ import unicode_literals

import importlib

from django.conf import settings

import six


class PreviewMode:
    """
    constants for AccessObject preview_as parameter
    """
    FORM = 'FORM'
    TABLE = 'TABLE'


class AccessObject(object):
    """
    This class is used to build roles that will be checked in fields accesses

    Depending on the type of role (e.g., API or end-user), `preview_as` is
    used by the UI to render a preview of a form as a table
    (`PreviewMode.TABLE`) or as a form (`PreviewMode.FORM`).
    """
    def __init__(self, id, label, description='', preview_as=None):
        self.id = id
        self.label = label
        self.description = description
        self.preview_as = preview_as or PreviewMode.FORM

    def __unicode__(self):
        return ('{access.id}: {access.label} [preview_as={access.preview_as}]'
                .format(access=self))


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
        assert type(access) == AccessObject, 'access must be AccessObject'
    return res


def get_context(request, kwargs):
    module, meth_name = settings.FORMIDABLE_CONTEXT_LOADER.rsplit('.', 1)
    if six.PY3:
        mod = importlib.import_module(module)
    else:
        mod = importlib.import_module(module, [meth_name])
    meth = getattr(mod, meth_name)
    return meth(request, kwargs)
