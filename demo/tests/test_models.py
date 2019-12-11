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


class FieldItemTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.formidable = FormTest.to_formidable(label='label')

    def test_label_field_size(self):
        field = self.formidable.fields.get(slug='dropdown')
        field.items.create(
            value='hello',
            label="hello" * 800,
            order=42,
        )

    def test_value_field_size(self):
        field = self.formidable.fields.get(slug='dropdown')
        my_field = field.items.create(
            value='hello' * 800,
            label="hello" * 800,
            order=42,
        )
        my_field = field.items.get(pk=my_field.pk)
        self.assertEqual(my_field.value, 'hello' * 800)
        self.assertEqual(my_field.label, 'hello' * 800)


class UnicodeTestCase(TestCase):

    def setUp(self):
        super().setUp()
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
