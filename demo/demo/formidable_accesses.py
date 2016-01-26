# -*- coding: utf-8 -*-

from formidable.accesses import AccessObject


def get_accesses():
    return [
        AccessObject(id=key, label=key)
        for key in [u'padawan', 'jedi', 'jedi-master', 'human']
    ]


def get_context(request, kwargs):
    return request.session['role']
