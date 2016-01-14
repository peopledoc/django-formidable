# -*- coding: utf-8 -*-

from django import forms
from django.test import TestCase

from formidable.models import Formidable


class TestDynamicForm(TestCase):

    def setUp(self):
        self.form = Formidable.objects.create(label=u'test',
                                              description=u'desc')
        self.text_field = self.form.fields.create(
            slug=u'text-input', type_id=u'text', label=u'mytext'
        )

    def test_text_input(self):
        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('text-input', form.fields)
        text = form.fields['text-input']
        self.assertEquals(text.required, False)
        self.assertEquals(type(text), forms.CharField)
        self.assertEquals(type(text.widget), forms.TextInput)

    def test_paragraph_input(self):
        self.form.fields.create(
            slug=u'area-input', type_id=u'paragraph', label=u'type a msg'
        )
        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('area-input', form.fields)
        text = form.fields['area-input']
        self.assertEquals(text.required, False)
        self.assertEquals(type(text), forms.CharField)
        self.assertEquals(type(text.widget), forms.Textarea)

    def test_dropdown_input(self):
        drop = self.form.fields.create(
            slug=u'weapons', type_id=u'dropdown', label=u'chose you weapon'
        )
        for key in ['sword', 'gun']:
            drop.items.create(key=key, value=key)

        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('weapons', form.fields)
        dropdown = form.fields['weapons']
        self.assertEquals(type(dropdown), forms.ChoiceField)
        self.assertEquals(type(dropdown.widget), forms.Select)
        self.assertTrue(dropdown.choices)
        self.assertEquals(len(dropdown.choices), 2)

    def test_dropdown_input_multiple(self):
        drop = self.form.fields.create(
            slug=u'multiple-weapons', type_id=u'dropdown',
            label=u'chose you weapon', multiple=True
        )
        for key in ['sword', 'gun']:
            drop.items.create(key=key, value=key)

        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('multiple-weapons', form.fields)
        dropdown = form.fields['multiple-weapons']
        self.assertEquals(type(dropdown), forms.ChoiceField)
        self.assertEquals(type(dropdown.widget), forms.SelectMultiple)
        self.assertTrue(dropdown.choices)
        self.assertEquals(len(dropdown.choices), 2)

    def test_radio_input(self):
        field = self.form.fields.create(
            slug=u'input-radio', type_id=u'radios',
            label=u'chose you weapon'
        )
        for key in ['sword', 'gun']:
            field.items.create(key=key, value=key)

        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('input-radio', form.fields)
        radio = form.fields['input-radio']
        self.assertEquals(type(radio), forms.ChoiceField)
        self.assertEquals(type(radio.widget), forms.RadioSelect)
        self.assertTrue(radio.choices)
        self.assertEquals(len(radio.choices), 2)

    def test_email_field(self):
        self.form.fields.create(
            slug=u'input-email', type_id=u'email', label=u'your email',
        )
        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('input-email', form.fields)
        email = form.fields['input-email']
        self.assertEquals(type(email), forms.EmailField)

    def test_date_field(self):
        self.form.fields.create(
            slug=u'input-date', type_id=u'date', label=u'your date',
        )
        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('input-date', form.fields)
        date = form.fields['input-date']
        self.assertEquals(type(date), forms.DateField)

    def test_number_field(self):
        self.form.fields.create(
            slug=u'input-number', type_id=u'number', label=u'your number',
        )
        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('input-number', form.fields)
        number = form.fields['input-number']
        self.assertEquals(type(number), forms.IntegerField)

    def test_required_field(self):
        self.text_field.accesses.create(access_id=u'human', level=u'REQUIRED')
        form_class = self.form.get_django_form_class(role=u'human')
        form = form_class()
        self.assertIn('text-input', form.fields)
        self.assertEquals(form.fields['text-input'].required, True)

    def test_editable_field(self):
        self.text_field.accesses.create(access_id=u'human', level=u'EDITABLE')
        form_class = self.form.get_django_form_class(role=u'human')
        form = form_class()
        self.assertIn('text-input', form.fields)
        self.assertEquals(form.fields['text-input'].required, False)

    def test_readonly_field(self):
        self.text_field.accesses.create(access_id=u'human', level=u'READONLY')
        form_class = self.form.get_django_form_class(role=u'human')
        form = form_class()
        self.assertIn('text-input', form.fields)
        field = form.fields['text-input']
        self.assertEquals(field.required, False)
        self.assertEquals(field.widget.attrs['disabled'], True)

    def test_hidden_field(self):
        self.text_field.accesses.create(access_id=u'human', level=u'HIDDEN')
        form_class = self.form.get_django_form_class(role=u'human')
        form = form_class()
        self.assertNotIn('text-input', form.fields)


class TestFormValidation(TestCase):

    def setUp(self):
        self.form = Formidable.objects.create(label=u'test',
                                              description=u'desc')
        self.text_field = self.form.fields.create(
            slug=u'text-input', type_id=u'text', label=u'mytext'
        )

    def test_min_length_ko(self):
        self.text_field.validations.create(type=u'MINLENGTH', value='5')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'text-input': '1234'})
        self.assertFalse(form.is_valid())

    def test_min_length_ok(self):
        self.text_field.validations.create(type=u'MINLENGTH', value='5')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'text-input': '12345'})
        self.assertTrue(form.is_valid())

    def test_max_length_ok(self):
        self.text_field.validations.create(type=u'MAXLENGTH', value='4')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'text-input': '12345'})
        self.assertFalse(form.is_valid())

    def test_max_length_ko(self):
        self.text_field.validations.create(type=u'MAXLENGTH', value='4')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'text-input': '123'})
        self.assertTrue(form.is_valid())

    def test_regex_ok(self):
        self.text_field.validations.create(type=u'REGEXP', value=r'^[0-9]+$')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'text-input': '12345'})
        self.assertTrue(form.is_valid())

    def test_regex_ko(self):
        self.text_field.validations.create(type=u'REGEXP', value=r'^[0-9]+$')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'text-input': 'abcd1234'})
        self.assertFalse(form.is_valid())

    def test_regexp_max_length(self):
        self.text_field.validations.create(type=u'REGEXP', value=r'^[0-9]+$')
        self.text_field.validations.create(type=u'MINLENGTH', value='5')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'text-input': '1234'})
        self.assertFalse(form.is_valid())
        form = form_class(data={'text-input': '1234abcdef'})
        self.assertFalse(form.is_valid())
        form = form_class(data={'text-input': '123456789'})
        self.assertTrue(form.is_valid())

    def test_gt_ok(self):
        number = self.form.fields.create(
            slug=u'input-number', type_id=u'number', label=u'your number',
        )
        number.validations.create(type=u'GT', value='21')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-number': '42'})
        self.assertTrue(form.is_valid())

    def test_gt_ko(self):
        number = self.form.fields.create(
            slug=u'input-number', type_id=u'number', label=u'your number',
        )
        number.validations.create(type=u'GT', value='21')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-number': '21'})
        self.assertFalse(form.is_valid())
        form = form_class(data={'input-number': '20'})
        self.assertFalse(form.is_valid())

    def test_gte_ok(self):
        number = self.form.fields.create(
            slug=u'input-number', type_id=u'number', label=u'your number',
        )
        number.validations.create(type=u'GTE', value='21')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-number': '21'})
        self.assertTrue(form.is_valid())
