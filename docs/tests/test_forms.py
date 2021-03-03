from . import validator, _load_fixture


def test_empty_form():
    form = _load_fixture('0000_empty.json')
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 3
    # All of these errors are of type 'required'
    for error in errors:
        assert error.validator == 'required'
    id_error, label_error, description_error = errors
    assert id_error.message == "'id' is a required property"
    assert label_error.message == "'label' is a required property"
    assert description_error.message == "'description' is a required property"


def test_just_id():
    form = _load_fixture('0001_just_id.json')
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 2
    # All of these errors are of type 'required'
    for error in errors:
        assert error.validator == 'required'
    label_error, description_error = errors
    assert label_error.message == "'label' is a required property"
    assert description_error.message == "'description' is a required property"


def test_id_and_label():
    form = _load_fixture('0002_id_label.json')
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    # All of these errors are of type 'required'
    for error in errors:
        assert error.validator == 'required'
    assert len(errors) == 1
    description_error = errors[0]
    assert description_error.message == "'description' is a required property"


def test_id_not_integer():
    form = _load_fixture('0003_id_not_integer.json')
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 1
    id_error = errors[0]
    assert id_error.validator == "type"
    assert id_error.message == "'hello' is not of type 'integer'"


def test_id_and_label_and_description():
    form = _load_fixture('0004_id_label_description.json')
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0


def test_id_description_null():
    form = _load_fixture('0021_id_label_description_null.json')
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 1
    error = errors[0]
    assert error.validator == "type"
    assert error.message == "None is not of type 'string'"


def test_id_description_empty():
    form = _load_fixture('0022_id_label_description_empty.json')
    errors = sorted(validator.iter_errors(form), key=lambda e: e.path)
    assert len(errors) == 0
