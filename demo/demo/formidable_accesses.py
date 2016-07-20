# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from formidable.accesses import AccessObject


def get_accesses():
    return [
        AccessObject(id=key, label=key)
        for key in ['padawan', 'jedi', 'jedi-master', 'human']
    ]


def get_context(request, kwargs):
    return request.session['role']
