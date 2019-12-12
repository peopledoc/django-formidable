from collections import namedtuple
from django.test import TestCase
from formidable.validators import ValidatorFactory, DateValidatorFactory
try:
    from unittest import mock
except ImportError:
    import mock


class TestValidatorFactoryMapping(TestCase):
    def setUp(self):
        self.validation_named_tuple = namedtuple(
            'Validation', ['type', 'message', 'value']
        )
        self.validation_object = ValidatorFactory()

    @mock.patch('formidable.validators.ValidatorFactory.min_length')
    def test_min_length(self, mock_object):
        self.validation_object.produce(
            self.validation_named_tuple(
                type='MINLENGTH',
                value=20,
                message='message'
            )
        )

        assert mock_object.called

    @mock.patch('formidable.validators.ValidatorFactory.max_length')
    def test_max_length(self, mock_object):
        self.validation_object.produce(
            self.validation_named_tuple(
                type='MAXLENGTH',
                value=20,
                message='message'
            )
        )

        assert mock_object.called

    @mock.patch('formidable.validators.ValidatorFactory.regexp')
    def test_regexp(self, mock_object):
        self.validation_object.produce(
            self.validation_named_tuple(
                type='REGEXP',
                value='value',
                message='message'
            )
        )

        assert mock_object.called

    @mock.patch('formidable.validators.ValidatorFactory.gt')
    def test_gt(self, mock_object):
        self.validation_object.produce(
            self.validation_named_tuple(
                type='GT',
                value=20,
                message='message'
            )
        )

        assert mock_object.called

    @mock.patch('formidable.validators.ValidatorFactory.gte')
    def test_gte(self, mock_object):
        self.validation_object.produce(
            self.validation_named_tuple(
                type='GTE',
                value=20,
                message='message'
            )
        )

        assert mock_object.called

    @mock.patch('formidable.validators.ValidatorFactory.lt')
    def test_lt(self, mock_object):
        self.validation_object.produce(
            self.validation_named_tuple(
                type='LT',
                value=20,
                message='message'
            )
        )

        assert mock_object.called

    @mock.patch('formidable.validators.ValidatorFactory.lte')
    def test_lte(self, mock_object):
        self.validation_object.produce(
            self.validation_named_tuple(
                type='LTE',
                value=20,
                message='message'
            )
        )

        assert mock_object.called

    @mock.patch('formidable.validators.ValidatorFactory.eq')
    def test_eq(self, mock_object):
        self.validation_object.produce(
            self.validation_named_tuple(
                type='EQ',
                value=20,
                message='message'
            )
        )

        assert mock_object.called

    @mock.patch('formidable.validators.ValidatorFactory.neq')
    def test_neq(self, mock_object):
        self.validation_object.produce(
            self.validation_named_tuple(
                type='NEQ',
                value=20,
                message='message'
            )
        )

        assert mock_object.called


class TestDateValidatorFactoryMapping(TestCase):
    def setUp(self):
        self.validation_named_tuple = namedtuple(
            'Validation', ['type', 'message', 'value']
        )
        self.validation_object = DateValidatorFactory()

    @mock.patch('formidable.validators.DateLTValidator')
    def test_lt(self, mocked_validator):
        self.validation_object.produce(
            self.validation_named_tuple(
                type='LT',
                value=20,
                message='message'
            )
        )
        assert mocked_validator.called

    @mock.patch('formidable.validators.DateMaxValueValidator')
    def test_lte(self, mocked_validator):
        self.validation_object.produce(
            self.validation_named_tuple(
                type='LTE',
                value=20,
                message='message'
            )
        )
        assert mocked_validator.called

    @mock.patch('formidable.validators.DateGTValidator')
    def test_gt(self, mocked_validator):
        self.validation_object.produce(
            self.validation_named_tuple(
                type='GT',
                value=20,
                message='message'
            )
        )
        assert mocked_validator.called

    @mock.patch('formidable.validators.DateIsInFuture')
    def test_date_future(self, mocked_validator):
        self.validation_object.produce(
            self.validation_named_tuple(
                type='IS_DATE_IN_THE_FUTURE',
                value='20',
                message='message'
            )
        )
        assert mocked_validator.called
