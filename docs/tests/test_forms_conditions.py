from copy import deepcopy

from . import validator, _load_fixture


def test_simple_condition():
    form = _load_fixture('0020_simple_condition.json')
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0

    # An empty list should still validate
    form['conditions'] = []
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0

    # wrong type should trigger a type error
    form['conditions'] = "something"
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 1
    error = errors[0]
    assert error.validator == 'type'
    assert error.message == "'something' is not of type 'array'"


def _load_20_simple_condition():
    form = _load_fixture('0020_simple_condition.json')
    condition = deepcopy(form['conditions'][0])
    return form, condition


def test_simple_condition_validation_no_name():
    form, no_name = _load_20_simple_condition()
    # FIXME: this should fail validation ; name should be mandatory.
    del no_name['name']
    form['conditions'] = [no_name]
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0


def test_simple_condition_validation_no_fields():
    form, no_fields = _load_20_simple_condition()
    # FIXME: this should fail validation ; field IDs should be mandatory.
    del no_fields['field_ids']
    form['conditions'] = [no_fields]
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0


def test_simple_condition_validation_fields_empty():
    form, fields_empty = _load_20_simple_condition()
    # FIXME: this should fail validation ; field IDs should not be empty.
    fields_empty['field_ids'] = []
    form['conditions'] = [fields_empty]
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0


def test_simple_condition_validation_no_tests():
    form, no_tests = _load_20_simple_condition()
    # FIXME: this should fail validation ; tests should be mandatory.
    del no_tests['tests']
    form['conditions'] = [no_tests]
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0


def test_simple_condition_validation_empty_tests():
    form, empty_tests = _load_20_simple_condition()
    # FIXME: this should fail validation ; tests should not be empty.
    empty_tests['tests'] = []
    form['conditions'] = [empty_tests]
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0


def test_simple_condition_validation_no_action():
    form, no_action = _load_20_simple_condition()
    # FIXME: this should fail validation ; it should have an action property.
    del no_action['action']
    form['conditions'] = [no_action]
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0


def _load_20_simple_condition_test():
    form = _load_fixture('0020_simple_condition.json')
    condition = deepcopy(form['conditions'][0])
    condition_test = deepcopy(condition['tests'][0])
    return form, condition, condition_test


def test_simple_condition_test_wrong_type():
    form, condition, condition_test = _load_20_simple_condition_test()

    # wrong type for test
    wrong_type_condition = deepcopy(condition)
    wrong_type_condition['tests'] = "something"
    form['conditions'] = [wrong_type_condition]
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 1
    error = errors[0]
    assert error.validator == 'type'
    assert error.message == "'something' is not of type 'array'"


def test_simple_condition_test_no_field_id():
    form, condition, no_field_id = _load_20_simple_condition_test()
    # FIXME: this should fail validation ; it should have a field_id property.
    # Remove field_id
    del no_field_id['field_id']
    no_field_id_condition = deepcopy(condition)
    no_field_id_condition['tests'] = [no_field_id]
    form['conditions'] = [no_field_id_condition]
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0


def test_simple_condition_test_no_op():
    form, condition, no_op = _load_20_simple_condition_test()
    # FIXME: this should fail validation ; it should have an operator.
    # Remove operator
    del no_op['operator']
    no_op_condition = deepcopy(condition)
    no_op_condition['tests'] = [no_op]
    form['conditions'] = [no_op_condition]
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0


def test_simple_condition_test_bad_op():
    form, condition, bad_op = _load_20_simple_condition_test()
    # Change operator to a wrong value
    bad_op['operator'] = "meh"
    bad_op_condition = deepcopy(condition)
    bad_op_condition['tests'] = [bad_op]
    form['conditions'] = [bad_op_condition]
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 1
    error = errors[0]
    assert error.validator == 'enum'
    assert error.message == "'meh' is not one of ['eq']"


def test_simple_condition_test_no_values():
    form, condition, no_values = _load_20_simple_condition_test()
    # FIXME: this should fail validation ; it should have a value.
    # Remove values
    del no_values['values']
    no_values_condition = deepcopy(condition)
    no_values_condition['tests'] = [no_values]
    form['conditions'] = [no_values_condition]
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0
