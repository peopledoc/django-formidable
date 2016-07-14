# -*- coding: utf-8 -*-
from django.test import TestCase

from formidable.models import Formidable
from formidable.forms import FormidableForm
from formidable.forms import fields, widgets
from formidable import validators


class FormTest(FormidableForm):

    title = fields.TitleField(label=u'Jedi Onboarding')
    helptext = fields.HelpTextField(text=u'youhou')
    mytext = fields.CharField(label=u'Name', accesses={
        'padawan': 'EDITABLE', 'jedi': 'REQUIRED', 'jedi-master': 'HIDDEN',
        'human': 'EDITABLE',
    })
    dropdown = fields.ChoiceField(
        choices=(('tutu', 'toto'), ('foo', 'bar')),
        accesses={'jedi': 'EDITABLE'}
    )


class TestFromDjangoForm(TestCase):

    def test_order_create(self):
        form = FormTest.to_formidable(label=u'label')
        self.assertTrue(
            form.fields.filter(slug='title', order=0).exists()
        )
        self.assertTrue(
            form.fields.filter(slug='helptext', order=1).exists()
        )
        self.assertTrue(
            form.fields.filter(slug='mytext', order=2).exists()
        )
        self.assertTrue(
            form.fields.filter(slug='dropdown', order=3).exists()
        )

    def test_regex_validators(self):
        class MyForm(FormidableForm):

            mytext = fields.CharField(
                label=u'text', validators=[validators.RegexValidator(
                    regex=r'^[0-9]\w+'
                )]
            )

        form = MyForm.to_formidable(label=u'with-validators')
        self.assertTrue(form.pk)
        self.assertTrue(form.fields.filter(slug='mytext').exists())
        field = form.fields.first()
        self.assertEquals(field.validations.count(), 1)
        valid = field.validations.first()
        self.assertEquals(valid.type, u'REGEXP')
        self.assertEquals(valid.value, r'^[0-9]\w+')

    def test_max_length_validators(self):
        class MyForm(FormidableForm):

            mytext = fields.CharField(
                label=u'text', validators=[validators.MaxLengthValidator(5)]
            )

        form = MyForm.to_formidable(label=u'with-validators')
        self.assertTrue(form.pk)
        self.assertTrue(form.fields.filter(slug='mytext').exists())
        field = form.fields.first()
        self.assertEquals(field.validations.count(), 1)
        valid = field.validations.first()
        self.assertEquals(valid.type, u'MAXLENGTH')
        self.assertEquals(valid.value, u'5')

    def test_min_length_validators(self):
        class MyForm(FormidableForm):

            mytext = fields.CharField(
                label=u'text', validators=[validators.MinLengthValidator(5)]
            )

        form = MyForm.to_formidable(label=u'with-validators')
        self.assertTrue(form.pk)
        self.assertTrue(form.fields.filter(slug='mytext').exists())
        field = form.fields.first()
        self.assertEquals(field.validations.count(), 1)
        valid = field.validations.first()
        self.assertEquals(valid.type, u'MINLENGTH')
        self.assertEquals(valid.value, u'5')

    def test_gt_validator(self):

        class MyForm(FormidableForm):

            mynumber = fields.IntegerField(
                label=u'number', validators=[validators.GTValidator(5)]
            )

        form = MyForm.to_formidable(label=u'with-validators')
        self.assertTrue(form.pk)
        self.assertTrue(form.fields.filter(slug='mynumber').exists())
        field = form.fields.first()
        self.assertEquals(field.validations.count(), 1)
        valid = field.validations.first()
        self.assertEquals(valid.type, u'GT')
        self.assertEquals(valid.value, u'5')

    def test_lt_validator(self):

        class MyForm(FormidableForm):

            mynumber = fields.IntegerField(
                label=u'number', validators=[validators.LTValidator(5)]
            )

        form = MyForm.to_formidable(label=u'with-validators')
        self.assertTrue(form.pk)
        self.assertTrue(form.fields.filter(slug='mynumber').exists())
        field = form.fields.first()
        self.assertEquals(field.validations.count(), 1)
        valid = field.validations.first()
        self.assertEquals(valid.type, u'LT')
        self.assertEquals(valid.value, u'5')

    def test_gte_validator(self):

        class MyForm(FormidableForm):

            mynumber = fields.IntegerField(
                label=u'number', validators=[validators.GTEValidator(5)]
            )

        form = MyForm.to_formidable(label=u'with-validators')
        self.assertTrue(form.pk)
        self.assertTrue(form.fields.filter(slug='mynumber').exists())
        field = form.fields.first()
        self.assertEquals(field.validations.count(), 1)
        valid = field.validations.first()
        self.assertEquals(valid.type, u'GTE')
        self.assertEquals(valid.value, u'5')

    def test_lte_validator(self):

        class MyForm(FormidableForm):

            mynumber = fields.IntegerField(
                label=u'number', validators=[validators.LTEValidator(5)]
            )

        form = MyForm.to_formidable(label=u'with-validators')
        self.assertTrue(form.pk)
        self.assertTrue(form.fields.filter(slug='mynumber').exists())
        field = form.fields.first()
        self.assertEquals(field.validations.count(), 1)
        valid = field.validations.first()
        self.assertEquals(valid.type, u'LTE')
        self.assertEquals(valid.value, u'5')

    def test_eq_validator(self):

        class MyForm(FormidableForm):

            mynumber = fields.IntegerField(
                label=u'number', validators=[validators.EQValidator(5)]
            )

        form = MyForm.to_formidable(label=u'with-validators')
        self.assertTrue(form.pk)
        self.assertTrue(form.fields.filter(slug='mynumber').exists())
        field = form.fields.first()
        self.assertEquals(field.validations.count(), 1)
        valid = field.validations.first()
        self.assertEquals(valid.type, u'EQ')
        self.assertEquals(valid.value, u'5')

    def test_neq_validator(self):

        class MyForm(FormidableForm):

            mynumber = fields.IntegerField(
                label=u'number', validators=[validators.NEQValidator(5)]
            )

        form = MyForm.to_formidable(label=u'with-validators')
        self.assertTrue(form.pk)
        self.assertTrue(form.fields.filter(slug='mynumber').exists())
        field = form.fields.first()
        self.assertEquals(field.validations.count(), 1)
        valid = field.validations.first()
        self.assertEquals(valid.type, u'NEQ')
        self.assertEquals(valid.value, u'5')

    def test_futur_date(self):

        class MyForm(FormidableForm):

            mydate = fields.DateField(
                validators=[validators.DateIsInFuture(False)]
            )

        form = MyForm.to_formidable(label=u'with-validators')
        self.assertTrue(form.pk)
        self.assertTrue(form.fields.filter(slug='mydate').exists())
        field = form.fields.first()
        self.assertEquals(field.validations.count(), 1)
        valid = field.validations.first()
        self.assertEquals(valid.type, u'IS_DATE_IN_THE_FUTURE')
        self.assertEquals(valid.value, u'False')

    def test_is_age_above(self):

        class MyForm(FormidableForm):

            mydate = fields.DateField(
                validators=[validators.AgeAboveValidator(21)]
            )

        form = MyForm.to_formidable(label=u'with-validators')
        self.assertTrue(form.pk)
        self.assertTrue(form.fields.filter(slug='mydate').exists())
        field = form.fields.first()
        self.assertEquals(field.validations.count(), 1)
        valid = field.validations.first()
        self.assertEquals(valid.type, u'IS_AGE_ABOVE')
        self.assertEquals(valid.value, '21')

    def test_is_age_under(self):

        class MyForm(FormidableForm):

            mydate = fields.DateField(
                validators=[validators.AgeUnderValidator(21)]
            )

        form = MyForm.to_formidable(label=u'with-validators')
        self.assertTrue(form.pk)
        self.assertTrue(form.fields.filter(slug='mydate').exists())
        field = form.fields.first()
        self.assertEquals(field.validations.count(), 1)
        valid = field.validations.first()
        self.assertEquals(valid.type, u'IS_AGE_UNDER')
        self.assertEquals(valid.value, '21')

    def test_accesses(self):
        form = FormTest.to_formidable(label=u'with-accesses')
        self.assertTrue(form.pk)
        self.assertTrue(form.fields.filter(slug='mytext').exists())
        field = form.fields.get(slug='mytext')
        self.assertEquals(4, field.accesses.count())
        self.assertTrue(form.fields.filter(slug='dropdown').exists())
        field = form.fields.get(slug='dropdown')
        self.assertEquals(4, field.accesses.count())
        self.assertTrue(field.accesses.filter(
            access_id='jedi', level=u'EDITABLE').exists()
        )

    def test_text_field(self):

        class MyForm(FormidableForm):
            mytext = fields.CharField(label='My Text')

        initial_count = Formidable.objects.count()
        form = MyForm.to_formidable(label=u'tutu')
        self.assertEquals(initial_count + 1, Formidable.objects.count())
        self.assertTrue(form.fields.filter(
            slug=u'mytext', type_id=u'text', label='My Text'
        ).exists())

    def test_integer_field(self):

        class MyForm(FormidableForm):
            number_children = fields.IntegerField(label='Your Children Number')

        initial_count = Formidable.objects.count()
        form = MyForm.to_formidable(label=u'tutu')
        self.assertEquals(initial_count + 1, Formidable.objects.count())
        self.assertTrue(form.fields.filter(
            slug=u'number_children', type_id=u'number',
        ).exists())

    def test_dropdown_field(self):

        class MyForm(FormidableForm):
            mydropdown = fields.ChoiceField(label=u'Weapons', choices=(
                ('GUN', 'eagle'), ('SWORD', u'Andúril'))
            )

        initial_count = Formidable.objects.count()
        form = MyForm.to_formidable(label=u'form-with-dropdown')
        self.assertEquals(initial_count + 1, Formidable.objects.count())
        self.assertTrue(form.pk)
        self.assertEquals(form.fields.count(), 1)
        self.assertTrue(form.fields.filter(
            slug=u'mydropdown', type_id=u'dropdown', label='Weapons'
        ).exists())
        field = form.fields.first()
        self.assertEquals(field.items.count(), 2)
        self.assertTrue(
            field.items.filter(value='GUN', label='eagle').exists()
        )
        self.assertTrue(
            field.items.filter(value='SWORD', label='Andúril').exists()
        )

    def test_dropdown_mutiple_field(self):

        class MyForm(FormidableForm):
            mydropdown = fields.MultipleChoiceField(label='Weapons', choices=(
                ('GUN', 'eagle'), ('SWORD', 'Andúril'))
            )

        initial_count = Formidable.objects.count()
        form = MyForm.to_formidable(label=u'form-with-dropdown')
        self.assertEquals(initial_count + 1, Formidable.objects.count())
        self.assertTrue(form.pk)
        self.assertEquals(form.fields.count(), 1)
        self.assertTrue(form.fields.filter(
            slug=u'mydropdown', type_id=u'dropdown', label='Weapons',
            multiple=True
        ).exists())
        field = form.fields.first()
        self.assertEquals(field.items.count(), 2)
        self.assertTrue(
            field.items.filter(value='GUN', label='eagle').exists()
        )
        self.assertTrue(
            field.items.filter(value='SWORD', label='Andúril').exists()
        )
        self.assertTrue(field.multiple)

    def test_checkbox_field(self):

        class MyForm(FormidableForm):

            checkboxinput = fields.BooleanField(label=u'Do you agree ?')

        initial_count = Formidable.objects.count()
        form = MyForm.to_formidable(label='form-with-checkbox')
        self.assertEquals(initial_count + 1, Formidable.objects.count())
        self.assertTrue(form.pk)
        self.assertEquals(form.fields.count(), 1)
        self.assertTrue(form.fields.filter(
            slug='checkboxinput', type_id='checkbox', label='Do you agree ?'
        ).exists())

    def test_checkbox_multiple_field(self):

        choices = (
            ('BELGIUM', 'Chouffe'), ('GERMANY', 'Paulaner'),
            ('FRANCE', 'Antidote')
        )

        class MyForm(FormidableForm):

            checkboxinput = fields.MultipleChoiceField(
                label=u'Beers ?', choices=choices,
                widget=widgets.CheckboxSelectMultiple
            )

        initial_count = Formidable.objects.count()
        form = MyForm.to_formidable(label='form-with-checkbox')
        self.assertEquals(initial_count + 1, Formidable.objects.count())
        self.assertTrue(form.pk)
        self.assertEquals(form.fields.count(), 1)
        self.assertTrue(form.fields.filter(
            slug='checkboxinput', type_id='checkboxes', label='Beers ?',
        ).exists())
        field = form.fields.first()
        self.assertEquals(field.items.count(), 3)
        for key, value in choices:
            self.assertTrue(
                field.items.filter(value=key, label=value).exists()
            )
        self.assertTrue(field.multiple)

    def test_date_field(self):

        class MyForm(FormidableForm):

            dateinput = fields.DateField(label=u'Birth Date')

        initial_count = Formidable.objects.count()
        form = MyForm.to_formidable(label=u'form-with-date')
        self.assertEquals(initial_count + 1, Formidable.objects.count())
        self.assertTrue(form.pk)
        self.assertEquals(form.fields.count(), 1)
        self.assertTrue(form.fields.filter(
            slug=u'dateinput', type_id=u'date', label='Birth Date',
        ).exists())
        self.assertFalse(form.fields.first().multiple)

    def test_radio_select(self):

        class MyForm(FormidableForm):

            radioinput = fields.ChoiceField(label=u'Apero ?', choices=(
                ('Yes', 'Oui'), ('No', 'Non'),
            ), widget=widgets.RadioSelect)

        initial_count = Formidable.objects.count()
        form = MyForm.to_formidable(label=u'form-with-radios')
        self.assertEquals(initial_count + 1, Formidable.objects.count())
        self.assertTrue(form.pk)
        self.assertEquals(form.fields.count(), 1)
        self.assertTrue(form.fields.filter(
            slug=u'radioinput', type_id=u'radios', label='Apero ?',
        ).exists())
        self.assertFalse(form.fields.first().multiple)

    def test_help_text(self):

        class MyForm(FormidableForm):

            helptext = fields.HelpTextField(text=u'My Help Text')

        initial_count = Formidable.objects.count()
        form = MyForm.to_formidable(label=u'form-with-helptex')
        self.assertEquals(initial_count + 1, Formidable.objects.count())
        self.assertTrue(form.pk)
        self.assertEquals(form.fields.count(), 1)
        self.assertTrue(form.fields.filter(
            slug=u'helptext', type_id=u'help_text', help_text='My Help Text',
        ).exists())

    def test_separator(self):
        class MyForm(FormidableForm):

            sepa = fields.SeparatorField()

        initial_count = Formidable.objects.count()
        form = MyForm.to_formidable(label=u'form-with-separator')
        self.assertEquals(initial_count + 1, Formidable.objects.count())
        self.assertTrue(form.pk)
        self.assertEquals(form.fields.count(), 1)
        self.assertTrue(form.fields.filter(
            slug=u'sepa', type_id=u'separator').exists()
        )

    def test_title(self):

        class MyForm(FormidableForm):

            title = fields.TitleField(label=u'Hello')

        initial_count = Formidable.objects.count()
        form = MyForm.to_formidable(label=u'form-with-title')
        self.assertEquals(initial_count + 1, Formidable.objects.count())
        self.assertTrue(form.pk)
        self.assertEquals(form.fields.count(), 1)
        self.assertTrue(form.fields.filter(
            slug=u'title', type_id=u'title', label='Hello',
        ).exists())

    def test_file_field(self):

        class MyForm(FormidableForm):

            myfile = fields.FileField(label='social-health-care')

        initial_count = Formidable.objects.count()
        form = MyForm.to_formidable(label=u'form-with-file')
        self.assertEquals(initial_count + 1, Formidable.objects.count())
        self.assertTrue(form.pk)
        self.assertEquals(form.fields.count(), 1)
        self.assertTrue(form.fields.filter(
            slug=u'myfile', type_id=u'file', label='social-health-care',
        ).exists())

    def test_without_label(self):

        class MyForm(FormidableForm):

            myfile = fields.FileField(label='social-health-care')

        with self.assertRaises(ValueError):
            MyForm.to_formidable()


class CreationForm(FormidableForm):
    first_name = fields.CharField()


class TestEditForm(TestCase):

    def setUp(self):
        super(TestEditForm, self).setUp()
        self.formidable = CreationForm.to_formidable(
            label='create', description='my creation form'
        )

    def test_edit_label(self):
        self.formidable = CreationForm.to_formidable(
            label='edit', instance=self.formidable
        )
        self.assertEqual(self.formidable.label, 'edit')
        self.assertEqual(self.formidable.description, 'my creation form')

    def test_edit_description(self):
        self.formidable = CreationForm.to_formidable(
            description='my edit', instance=self.formidable)
        self.assertEqual(self.formidable.label, 'create')
        self.assertEqual(self.formidable.description, 'my edit')

    def test_edit_desc_label(self):
        self.formidable = CreationForm.to_formidable(
            description='my edit', label='edit', instance=self.formidable
        )
        self.assertEqual(self.formidable.description, 'my edit')
        self.assertEqual(self.formidable.label, 'edit')

    def test_edit_fields(self):

        class EditForm(FormidableForm):
            first_name = fields.CharField()
            last_name = fields.CharField()

        form = EditForm.to_formidable(instance=self.formidable)
        self.assertEqual(form.pk, self.formidable.pk)
        self.assertEqual(form.fields.count(), 2)
        self.assertTrue(self.formidable.fields.filter(
            slug='last_name').exists())
