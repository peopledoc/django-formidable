# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TestCase
from django.core.exceptions import ValidationError, ImproperlyConfigured

from formidable.forms.validations.presets import (
    ConfirmationPresets, ComparisonPresets
)
from formidable.models import PresetArg


class PresetsTestCase(TestCase):

    def test_confirmation_ok_value(self):
        args = [
            PresetArg(slug='left', field_id='name'),
            PresetArg(slug='right', value='toto')
        ]
        rule = ConfirmationPresets(args)
        cleaned_data = {'name': 'toto'}
        self.assertTrue(rule(cleaned_data))

    def test_confirmation_ok_field(self):
        args = [
            PresetArg(slug='left', field_id='password'),
            PresetArg(slug='right', field_id='confirm_password')
        ]
        rule = ConfirmationPresets(args)
        cleaned_data = {'password': 'toto', 'confirm_password': 'toto'}
        self.assertTrue(rule(cleaned_data))

    def test_confirmation_ko_value(self):
        args = [
            PresetArg(slug='left', field_id='name'),
            PresetArg(slug='right', value='toto')
        ]
        rule = ConfirmationPresets(args)
        cleaned_data = {'name': 'tutu'}
        with self.assertRaises(ValidationError):
            rule(cleaned_data)

    def test_confirmation_ko_field(self):
        args = [
            PresetArg(slug='left', field_id='password'),
            PresetArg(slug='right', field_id='confirm_password')
        ]
        rule = ConfirmationPresets(args)
        cleaned_data = {'password': 'toto', 'confirm_password': 'tutu'}
        with self.assertRaises(ValidationError):
            self.assertTrue(rule(cleaned_data))

    def test_missing_left_operand(self):
        args = [
            PresetArg(slug='right', field_id='confirm_password')
        ]
        with self.assertRaises(ImproperlyConfigured):
            ConfirmationPresets(args)

    def test_missing_right_operand(self):
        args = [
            PresetArg(slug='left', field_id='password'),
        ]
        with self.assertRaises(ImproperlyConfigured):
            ConfirmationPresets(args)

    def test_comparison_eq_ok(self):
        args = [
            PresetArg(slug='left', field_id='hours'),
            PresetArg(slug='operator', value='eq'),
            PresetArg(slug='right', field_id='hours-2')
        ]
        rule = ComparisonPresets(args)
        cleaned_data = {'hours': 12, 'hours-2': 12}
        self.assertTrue(rule(cleaned_data))

    def test_comparison_eq_ko(self):
        args = [
            PresetArg(slug='left', field_id='hours'),
            PresetArg(slug='operator', value='eq'),
            PresetArg(slug='right', field_id='hours-2')
        ]
        rule = ComparisonPresets(args)
        cleaned_data = {'hours': 11, 'hours-2': 12}
        with self.assertRaises(ValidationError):
            self.assertTrue(rule(cleaned_data))

    def test_comparison_neq_ok(self):
        args = [
            PresetArg(slug='left', field_id='hours'),
            PresetArg(slug='operator', value='neq'),
            PresetArg(slug='right', field_id='hours-2')
        ]
        rule = ComparisonPresets(args)
        cleaned_data = {'hours': 12, 'hours-2': 11}
        self.assertTrue(rule(cleaned_data))

    def test_comparison_neq_ko(self):
        args = [
            PresetArg(slug='left', field_id='hours'),
            PresetArg(slug='operator', value='neq'),
            PresetArg(slug='right', field_id='hours-2')
        ]
        rule = ComparisonPresets(args)
        cleaned_data = {'hours': 12, 'hours-2': 12}
        with self.assertRaises(ValidationError):
            self.assertTrue(rule(cleaned_data))
