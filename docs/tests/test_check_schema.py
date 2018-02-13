from jsonschema import Draft4Validator
from . import schema


def test_validate_schema():
    # First, check Schema
    assert Draft4Validator.check_schema(schema) is None
