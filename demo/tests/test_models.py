# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TestCase

from formidable import constants
from formidable.forms import fields, FormidableForm


class FormTest(FormidableForm):
    title = fields.TitleField(label='Jedi Onboarding')
    helptext = fields.HelpTextField(text='youhou')
    mytext = fields.CharField(label='Name', accesses={
        'padawan': constants.EDITABLE,
        'jedi': constants.REQUIRED,
        'jedi-master': constants.HIDDEN,
        'human': constants.EDITABLE,
    })
    dropdown = fields.ChoiceField(
        choices=(('tutu', 'toto'), ('foo', 'bar')),
        accesses={'jedi': 'EDITABLE'}
    )


class UnicodeTestCase(TestCase):

    def setUp(self):
        super(UnicodeTestCase, self).setUp()
        self.formidable = FormTest.to_formidable(label='label')

    def test_formidable(self):
        self.assertEqual(str(self.formidable), 'label')

    def test_field(self):
        field = self.formidable.fields.get(slug='title')
        self.assertEqual(str(field), 'Jedi Onboarding')

    def test_default(self):
        field = self.formidable.fields.get(slug='title')
        default = field.defaults.create(value='Value')
        self.assertEqual(str(default), 'Value')

    def test_item(self):
        field = self.formidable.fields.get(slug='dropdown')
        self.assertEqual(field.items.all().count(), 2)
        tutu, foo = field.items.all()
        self.assertEqual(str(tutu), 'toto: tutu')
        self.assertEqual(str(foo), 'bar: foo')

    def test_access(self):
        field = self.formidable.fields.get(slug='mytext')
        self.assertEqual(field.accesses.all().count(), 5)

        human, jedi, jedi_master, padawan, robot = field.accesses.all().order_by('access_id')  # noqa
        self.assertEqual(str(human), 'human: EDITABLE')
        self.assertEqual(str(jedi), 'jedi: REQUIRED')
        self.assertEqual(str(jedi_master), 'jedi-master: HIDDEN')
        self.assertEqual(str(padawan), 'padawan: EDITABLE')
        self.assertEqual(str(robot), 'robot: EDITABLE')

    def test_validation(self):
        field = self.formidable.fields.get(slug='dropdown')
        validation = field.validations.create(value='Value', type='Type')
        self.assertEqual(str(validation), 'Value: Type')

    def test_preset(self):
        preset = self.formidable.presets.create(slug='slug')
        self.assertEqual(str(preset), 'slug')

    def test_preset_argument(self):
        preset = self.formidable.presets.create(slug='slug')

        argument = preset.arguments.create(slug='slug', value='Value')
        self.assertEqual(str(argument), 'slug: value Value')

        argument.field_id = '12345'
        self.assertEqual(str(argument), 'slug: field #12345')
