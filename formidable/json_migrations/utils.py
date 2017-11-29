from copy import deepcopy

from formidable import constants


def get_access_from_context_field(field):
    if field is None:
        return constants.HIDDEN
    if field['disabled']:
        return constants.READONLY
    if field['required']:
        return constants.REQUIRED
    return constants.EDITABLE


def uncontextualize_field(field, role):
    new_field = deepcopy(field)
    access = get_access_from_context_field(field)
    del new_field['disabled']
    del new_field['required']
    new_field['accesses'] = [{'access_id': role, 'level': access}]
    return new_field


def add_fields(ref_fields, new_fields):
    current_field = 0

    for field in new_fields:
        for index, ref_field in enumerate(ref_fields):
            if field['slug'] == ref_field['slug']:
                # no need to insert a new field :
                # update accesses and move the cursor
                ref_field['accesses'].extend(field['accesses'])
                current_field = index + 1
                break
        else:
            # we need to insert field at the right position
            ref_fields.insert(current_field, field)
            current_field += 1


def merge_context_forms(forms):
    # forms: role => ContextForm
    # remove version from context if exists
    version = forms.pop('version', None)

    roles = list(forms.keys())

    if {'description', 'fields', 'label', 'id'}.issubset(roles):
        # If these keys are in the forms, the form is already
        # uncontextualized.
        return forms

    # Formidable and ContextForm JSON formats only differs by the field
    # attribute (and some missing attributes in ContextForm). We can copy
    # everything and overwrite `fields`.
    form = deepcopy(forms[roles[0]])
    fields = []
    for role in roles:
        add_fields(fields,
                   [uncontextualize_field(field, role)
                    for field in forms[role]['fields']])

    # fix missing accesses in `fields`
    for role in roles:
        for field in fields:
            if role not in [a['access_id'] for a in field['accesses']]:
                field['accesses'].append(
                    {'access_id': role, 'level': constants.HIDDEN}
                )
    form['fields'] = fields

    # set saved version if exists
    if version is not None:
        form['version'] = version

    return form
