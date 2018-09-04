# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from formidable.accesses import AccessObject, PreviewMode


def get_accesses():
    return [
        AccessObject(id='padawan', label='padawan'),
        AccessObject(id='jedi', label='jedi'),
        AccessObject(id='jedi-master', label='jedi-master'),
        AccessObject(id='human', label='human'),
        AccessObject(id='robot', label='robot', preview_as=PreviewMode.TABLE),
    ]


def get_context(request, kwargs):
    """
    Return the value of the role for the request

    For the sake of the demo, the role value can be set using the Django
    session or the "GET" argument.

    example: "http://localhost:8000/api/forms/1/validate?role=jedi"
    """
    return request.session.get('role') or request.GET.get('role')
