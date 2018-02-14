from copy import deepcopy
from . import validator, _load_fixture


def test_field_validations():
    form = _load_fixture('0017_fields_validations.json')
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0

    # An empty list should still validate
    form['fields'][0]['validations'] = []
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0

    # wrong type should trigger a type error
    form['fields'][0]['validations'] = "something"
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 1
    error = errors[0]
    assert error.validator == 'type'
    assert error.message == "'something' is not of type 'array'"


def _load_17_fields_validations():
    form = _load_fixture('0017_fields_validations.json')
    items = deepcopy(form['fields'][0]['validations'])
    item = deepcopy(items[0])
    return form, items, item


def test_field_validations_no_message():
    form, items, no_message = _load_17_fields_validations()
    # Removing the overwritten message shouldn't invalidate the field
    del no_message['message']
    form['fields'][0]['validations'] = [no_message]
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0


def test_field_validations_no_type():
    form, items, no_type = _load_17_fields_validations()
    del no_type['type']
    form['fields'][0]['validations'] = [no_type]
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 1
    error = errors[0]
    assert error.validator == 'required'
    assert error.message == "'type' is a required property"


def test_field_validations_no_value():
    form, items, no_value = _load_17_fields_validations()
    del no_value['value']
    form['fields'][0]['validations'] = [no_value]
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 1
    error = errors[0]
    assert error.validator == 'required'
    assert error.message == "'value' is a required property"

# TODO: field validation grids
# I don't know if it's possible to validate the grid.
#
# For the record, here's the grid:
# * text: MINLENGTH, MAXLENGTH, REGEXP
# * paragraph: MINLENGTH, MAXLENGTH, REGEXP
# * date: GT, GTE, LT, LTE, EQ, NEQ, IS_AGE_ABOVE (>=), IS_AGE_UNDER (<),
#   IS_DATE_IN_THE_PAST, IS_DATE_IN_THE_FUTURE
# * number: GT, GTE, LT, LTE, EQ, NEQ


availablele_validation_types = [
    'EQ',
    'GT',
    'GTE',
    'IS_AGE_ABOVE',
    'IS_AGE_UNDER',
    'IS_DATE_IN_THE_FUTURE',
    'IS_DATE_IN_THE_PAST',
    'LT',
    'LTE',
    'MAXLENGTH',
    'MINLENGTH',
    'NEQ',
    'REGEXP'
]


def test_field_validations_type_ok():
    form, items, values = _load_17_fields_validations()
    for validation_type in availablele_validation_types:
        values.update({"type": validation_type})
        form['fields'][0]['validations'] = [values]
        errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
        assert len(errors) == 0


def test_field_validations_wrong_type():
    form, items, values = _load_17_fields_validations()
    values.update({"type": 'UNKNOWN'})
    form['fields'][0]['validations'] = [values]
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 1
    error = errors[0]
    assert error.message == f"'UNKNOWN' is not one of {availablele_validation_types}"  # noqa
