# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.exceptions import ValidationError, ImproperlyConfigured

from formidable.forms.validations.presets import ConfirmationPresets


class FakeArgument(object):

    def __init__(self, slug, value, type):
        self.slug = slug
        self.value = value
        self.type = type


class PresetsTestCase(TestCase):

    def test_confirmation_ok_value(self):
        args = [
            FakeArgument('left', 'name', 'field'),
            FakeArgument('right', 'toto', 'value')
        ]
        rule = ConfirmationPresets(args)
        cleaned_data = {'name': 'toto'}
        self.assertTrue(rule(cleaned_data))

    def test_confirmation_ok_field(self):
        args = [
            FakeArgument('left', 'password', 'field'),
            FakeArgument('right', 'confirm_password', 'field')
        ]
        rule = ConfirmationPresets(args)
        cleaned_data = {'password': 'toto', 'confirm_password': 'toto'}
        self.assertTrue(rule(cleaned_data))

    def test_confirmation_ko_value(self):
        args = [
            FakeArgument('left', 'name', 'field'),
            FakeArgument('right', 'toto', 'value')
        ]
        rule = ConfirmationPresets(args)
        cleaned_data = {'name': 'tutu'}
        with self.assertRaises(ValidationError):
            rule(cleaned_data)

    def test_confirmation_ko_field(self):
        args = [
            FakeArgument('left', 'password', 'field'),
            FakeArgument('right', 'confirm_password', 'field')
        ]
        rule = ConfirmationPresets(args)
        cleaned_data = {'password': 'toto', 'confirm_password': 'tutu'}
        with self.assertRaises(ValidationError):
            self.assertTrue(rule(cleaned_data))

    def test_missing_left_operand(self):
        args = [
            FakeArgument('right', 'confirm_password', 'field')
        ]
        rule = ConfirmationPresets(args)
        cleaned_data = {'password': 'toto', 'confirm_password': 'tutu'}
        with self.assertRaises(ImproperlyConfigured):
            self.assertTrue(rule(cleaned_data))

    def test_missing_right_operand(self):
        args = [
            FakeArgument('left', 'password', 'field'),
        ]
        rule = ConfirmationPresets(args)
        cleaned_data = {'password': 'toto', 'confirm_password': 'tutu'}
        with self.assertRaises(ImproperlyConfigured):
            self.assertTrue(rule(cleaned_data))
