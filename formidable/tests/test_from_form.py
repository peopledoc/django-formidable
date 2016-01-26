# -*- coding: utf-8 -*-
from django.test import TestCase

from formidable.models import Formidable
from formidable.forms import FormidableForm
from formidable.forms import fields, widgets


class FormTest(FormidableForm):

    mytext = fields.CharField(label=u'Name', accesses={
        'padawan': 'EDITABLE', 'jedi': 'REQUIRED', 'jedi-master': 'HIDDEN',
        'human': 'EDITABLE',
    })
    dropdown = fields.ChoiceField(
        choices=(('tutu', 'toto'), ('foo', 'bar')),
        accesses={'jedi': 'EDITABLE'}
    )


class TestFromDjangoForm(TestCase):

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
            field.items.filter(key=u'GUN', value=u'eagle').exists()
        )
        self.assertTrue(
            field.items.filter(key=u'SWORD', value=u'Andúril').exists()
        )

    def test_dropdown_mutiple_field(self):

        class MyForm(FormidableForm):
            mydropdown = fields.MultipleChoiceField(label=u'Weapons', choices=(
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
            field.items.filter(key=u'GUN', value=u'eagle').exists()
        )
        self.assertTrue(
            field.items.filter(key=u'SWORD', value=u'Andúril').exists()
        )
        self.assertTrue(field.multiple)

    def test_checkbox_field(self):

        class MyForm(FormidableForm):

            checkboxinput = fields.BooleanField(label=u'Do you agree ?')

        initial_count = Formidable.objects.count()
        form = MyForm.to_formidable(label=u'form-with-checkbox')
        self.assertEquals(initial_count + 1, Formidable.objects.count())
        self.assertTrue(form.pk)
        self.assertEquals(form.fields.count(), 1)
        self.assertTrue(form.fields.filter(
            slug=u'checkboxinput', type_id=u'checkbox', label='Do you agree ?'
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
        form = MyForm.to_formidable(label=u'form-with-checkbox')
        self.assertEquals(initial_count + 1, Formidable.objects.count())
        self.assertTrue(form.pk)
        self.assertEquals(form.fields.count(), 1)
        self.assertTrue(form.fields.filter(
            slug=u'checkboxinput', type_id=u'checkboxes', label='Beers ?',
        ).exists())
        field = form.fields.first()
        self.assertEquals(field.items.count(), 3)
        for key, value in choices:
            self.assertTrue(
                field.items.filter(key=key, value=value).exists()
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
