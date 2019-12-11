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
    return request.session['role']
