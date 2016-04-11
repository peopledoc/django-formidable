# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.exceptions import ValidationError, ImproperlyConfigured

from formidable.forms.validations.presets import ConfirmationPresets


class FakeArgument(object):

    def __init__(self, slug, field_id=None, value=None):
        self.slug = slug
        self.value = value
        self.field_id = field_id


class PresetsTestCase(TestCase):

    def test_confirmation_ok_value(self):
        args = [
            FakeArgument('left', field_id='name'),
            FakeArgument('right', value='toto')
        ]
        rule = ConfirmationPresets(args)
        cleaned_data = {'name': 'toto'}
        self.assertTrue(rule(cleaned_data))

    def test_confirmation_ok_field(self):
        args = [
            FakeArgument('left', field_id='password'),
            FakeArgument('right', field_id='confirm_password')
        ]
        rule = ConfirmationPresets(args)
        cleaned_data = {'password': 'toto', 'confirm_password': 'toto'}
        self.assertTrue(rule(cleaned_data))

    def test_confirmation_ko_value(self):
        args = [
            FakeArgument('left', field_id='name'),
            FakeArgument('right', value='toto')
        ]
        rule = ConfirmationPresets(args)
        cleaned_data = {'name': 'tutu'}
        with self.assertRaises(ValidationError):
            rule(cleaned_data)

    def test_confirmation_ko_field(self):
        args = [
            FakeArgument('left', field_id='password'),
            FakeArgument('right', field_id='confirm_password')
        ]
        rule = ConfirmationPresets(args)
        cleaned_data = {'password': 'toto', 'confirm_password': 'tutu'}
        with self.assertRaises(ValidationError):
            self.assertTrue(rule(cleaned_data))

    def test_missing_left_operand(self):
        args = [
            FakeArgument('right', field_id='confirm_password')
        ]
        rule = ConfirmationPresets(args)
        cleaned_data = {'password': 'toto', 'confirm_password': 'tutu'}
        with self.assertRaises(ImproperlyConfigured):
            self.assertTrue(rule(cleaned_data))

    def test_missing_right_operand(self):
        args = [
            FakeArgument('left', field_id='password'),
        ]
        rule = ConfirmationPresets(args)
        cleaned_data = {'password': 'toto', 'confirm_password': 'tutu'}
        with self.assertRaises(ImproperlyConfigured):
            self.assertTrue(rule(cleaned_data))
