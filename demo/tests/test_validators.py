# -*- coding: utf-8 -*-
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

    def test_min_length(self):
        mock_object = mock.Mock()
        ValidatorFactory.min_length = mock_object
        self.validation_object.produce(
            self.validation_named_tuple(
                type='MINLENGTH',
                value=20,
                message='message'
            )
        )

        assert mock_object.called

    def test_max_length(self):
        mock_object = mock.Mock()
        ValidatorFactory.max_length = mock_object

        self.validation_object.produce(
            self.validation_named_tuple(
                type='MAXLENGTH',
                value=20,
                message='message'
            )
        )

        assert mock_object.called

    def test_regexp(self):
        mock_object = mock.Mock()
        ValidatorFactory.regexp = mock_object

        self.validation_object.produce(
            self.validation_named_tuple(
                type='REGEXP',
                value='value',
                message='message'
            )
        )

        assert mock_object.called

    def test_gt(self):
        mock_object = mock.Mock()
        ValidatorFactory.gt = mock_object

        self.validation_object.produce(
            self.validation_named_tuple(
                type='GT',
                value=20,
                message='message'
            )
        )

        assert mock_object.called

    def test_gte(self):
        mock_object = mock.Mock()
        ValidatorFactory.gte = mock_object

        self.validation_object.produce(
            self.validation_named_tuple(
                type='GTE',
                value=20,
                message='message'
            )
        )

        assert mock_object.called

    def test_lt(self):
        mock_object = mock.Mock()
        ValidatorFactory.lt = mock_object

        self.validation_object.produce(
            self.validation_named_tuple(
                type='LT',
                value=20,
                message='message'
            )
        )

        assert mock_object.called

    def test_lte(self):
        mock_object = mock.Mock()
        ValidatorFactory.lte = mock_object

        self.validation_object.produce(
            self.validation_named_tuple(
                type='LTE',
                value=20,
                message='message'
            )
        )

        assert mock_object.called

    def test_eq(self):
        mock_object = mock.Mock()
        ValidatorFactory.eq = mock_object

        self.validation_object.produce(
            self.validation_named_tuple(
                type='EQ',
                value=20,
                message='message'
            )
        )

        assert mock_object.called

    def test_neq(self):
        mock_object = mock.Mock()
        ValidatorFactory.neq = mock_object

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
