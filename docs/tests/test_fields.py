from collections import deque
from copy import deepcopy
from . import validator, _load_fixture


def test_wrong_type_fields_int():
    form = _load_fixture('0010_wrong_type_field_int.json')
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 1
    fields_error = errors[0]
    assert fields_error.path == deque(['fields'])
    assert fields_error.validator == 'type'
    assert fields_error.message == "42 is not of type 'array'"


def test_wrong_type_fields_dict():
    form = _load_fixture('0010_wrong_type_field_dict.json')
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 1
    fields_error = errors[0]
    assert fields_error.path == deque(['fields'])
    assert fields_error.validator == 'type'
    assert fields_error.message == "{'hello': 'world'} is not of type 'array'"


def test_empty_fields():
    form = _load_fixture('0011_empty_fields.json')
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0


def test_field_empty_object():
    form = _load_fixture('0012_fields_empty_object.json')
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 6
    for error in errors:
        assert error.validator == 'required'
    (id_error, slug_error, label_error, type_id_error,
     description_error, accesses_error) = errors
    assert id_error.message == "'id' is a required property"
    assert slug_error.message == "'slug' is a required property"
    assert label_error.message == "'label' is a required property"
    assert type_id_error.message == "'type_id' is a required property"
    assert description_error.message == "'description' is a required property"
    assert accesses_error.message == "'accesses' is a required property"


def test_field_missing_property():
    form = _load_fixture('0012_fields_ok.json')
    for item in ('id', 'slug', 'label', 'type_id', 'description', 'accesses'):
        _form = deepcopy(form)
        del _form['fields'][0][item]
        errors = sorted(validator.iter_errors(_form), key=lambda e: e.path)
        assert len(errors) == 1
        error = errors[0]
        assert error.validator == 'required'
        assert error.message == "'{}' is a required property".format(item)


available_types = [
    'title', 'helpText', 'fieldset', 'fieldsetTable', 'separation',
    'checkbox', 'checkboxes', 'dropdown', 'radios', 'radiosButtons',
    'text', 'paragraph', 'file', 'date', 'email', 'number'
]


def test_field_type_id_ok():
    form = _load_fixture('0011_empty_fields.json')
    for type_id in available_types:
        _form = deepcopy(form)
        _form['fields'] = [
                  {
                    "id": 1,
                    "label": "My Field",
                    "slug": "my-field",
                    "type_id": type_id,
                    "description": "This is a boring description",
                    "accesses": []
                  }
        ]
        errors = sorted(validator.iter_errors(_form), key=lambda e: e.path)
        assert len(errors) == 0


def test_field_wrong_type_id():
    form = _load_fixture('0011_empty_fields.json')
    _form = deepcopy(form)
    _form['fields'] = [
              {
                "id": 1,
                "label": "My Field",
                "slug": "my-field",
                "type_id": 'unknown',
                "description": "This is a boring description",
                "accesses": []
              }
    ]
    errors = sorted(validator.iter_errors(_form), key=lambda e: e.path)
    assert len(errors) == 1
    error = errors[0]
    assert error.validator == 'enum'
    assert error.message == "'unknown' is not one of {}".format(
        available_types)


def test_fields_ok():
    form = _load_fixture('0012_fields_ok.json')
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0


def test_fields_placeholder():
    form = _load_fixture('0013_fields_placeholder.json')
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0
    form['fields'][0]['placeholder'] = 42
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 1
    error = errors[0]
    assert error.validator == 'type'
    assert error.message == "42 is not of type 'string'"


def test_fields_multiple():
    form = _load_fixture('0014_fields_multiple.json')
    # Should be ok here
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0
    # Changing the value to another boolean
    form['fields'][0]['multiple'] = False
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0

    # Changing the value to a wrong type
    form['fields'][0]['multiple'] = "something"
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 1
    error = errors[0]
    assert error.validator == 'type'
    assert error.message == "'something' is not of type 'boolean'"


def test_fields_items():
    form = _load_fixture('0015_fields_items.json')
    # Should be ok here
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0

    # Changing the value to an empty list
    form['fields'][0]['items'] = []
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0

    # Changing the value to a wrong type
    form['fields'][0]['items'] = "something"
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 1
    error = errors[0]
    assert error.validator == 'type'
    assert error.message == "'something' is not of type 'array'"


def _load_15_fields_items():
    form = _load_fixture('0015_fields_items.json')
    items = deepcopy(form['fields'][0]['items'])
    item = deepcopy(items[0])
    return form, items, item


def test_fields_items_validation_no_description():
    form, items, no_description = _load_15_fields_items()
    del no_description['description']
    form['fields'][0]['items'] = [no_description]
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0


def test_fields_items_validation_no_value():
    form, items, no_value = _load_15_fields_items()
    del no_value['value']
    form['fields'][0]['items'] = [no_value]
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 1
    error = errors[0]
    assert error.validator == 'required'
    assert error.message == "'value' is a required property"


def test_fields_items_validation_no_label():
    form, items, no_label = _load_15_fields_items()
    del no_label['label']
    form['fields'][0]['items'] = [no_label]
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 1
    error = errors[0]
    assert error.validator == 'required'
    assert error.message == "'label' is a required property"


def test_fields_items_validation_wrong_types():
    form, items, item = _load_15_fields_items()
    for key in ('label', 'value', 'description'):
        wrong_types = deepcopy(item)
        wrong_types[key] = 42
        form['fields'][0]['items'] = [wrong_types]
        errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
        assert len(errors) == 1
        error = errors[0]
        assert error.validator == 'type'
        assert error.message == "42 is not of type 'string'"


def test_field_accesses():
    form = _load_fixture('0016_fields_accesses.json')
    # Should be ok here
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0

    # Changing the value to an empty list
    form['fields'][0]['accesses'] = []
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0

    # Changing the value to a wrong type
    form['fields'][0]['accesses'] = "something"
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 1
    error = errors[0]
    assert error.validator == 'type'
    assert error.message == "'something' is not of type 'array'"


def _load_16_fields_accesses():
    form = _load_fixture('0016_fields_accesses.json')
    items = deepcopy(form['fields'][0]['accesses'])
    item = deepcopy(items[0])
    return form, items, item


def test_field_accesses_validation_no_access():
    form, items, no_access_id = _load_16_fields_accesses()
    del no_access_id['access_id']
    form['fields'][0]['accesses'] = [no_access_id]
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 1
    error = errors[0]
    assert error.validator == 'required'
    assert error.message == "'access_id' is a required property"


def test_field_accesses_validation_no_level():
    form, items, no_level = _load_16_fields_accesses()
    del no_level['level']
    form['fields'][0]['accesses'] = [no_level]
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 1
    error = errors[0]
    assert error.validator == 'required'
    assert error.message == "'level' is a required property"


def test_field_accesses_validation_wrong_level():
    form, items, wrong_level = _load_16_fields_accesses()
    wrong_level['level'] = 'UNBELIEVABLE'
    form['fields'][0]['accesses'] = [wrong_level]
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 1
    error = errors[0]
    assert error.validator == 'enum'
    levels = ['REQUIRED', 'EDITABLE', 'HIDDEN', 'READONLY']
    assert error.message == f"'UNBELIEVABLE' is not one of {levels}"


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
# 1. don't know if it's possible to validate the grid.
# 2. at least it should be possible to build an enum with available values.
#
# Here they are:
# * text: MINLENGTH, MAXLENGTH, REGEXP
# * paragraph: MINLENGTH, MAXLENGTH, REGEXP
# * date: GT, GTE, LT, LTE, EQ, NEQ, IS_AGE_ABOVE (>=), IS_AGE_UNDER (<),
#   IS_DATE_IN_THE_PAST, IS_DATE_IN_THE_FUTURE
# * number: GT, GTE, LT, LTE, EQ, NEQ


def _load_18_fields_defaults():
    form = _load_fixture('0018_fields_defaults.json')
    field = form['fields'][0]
    return form, field


def test_fields_defaults():
    form, field = _load_18_fields_defaults()
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0


def test_fields_defaults_empty():
    form, field = _load_18_fields_defaults()
    # Empty arrays should work
    field['defaults'] = []
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0


def test_fields_defaults_wrong_type():
    form, field = _load_18_fields_defaults()
    # Wrong type in array
    for value in (42, True, None):
        field['defaults'] = [value]
        errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
        assert len(errors) == 1
        error = errors[0]
        assert error.validator == 'type'
        assert error.message == f"{value} is not of type 'string'"


def test_fields_defaults_bad_type():
    form, field = _load_18_fields_defaults()
    # Plain wrong type
    field['defaults'] = "something"
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 1
    error = errors[0]
    assert error.validator == 'type'
    assert error.message == "'something' is not of type 'array'"
