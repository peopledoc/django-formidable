# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import os
import io

from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase
import django_perf_rec
from freezegun import freeze_time

from formidable.constants import REQUIRED, EDITABLE, READONLY, HIDDEN
from formidable.models import Formidable
from formidable.forms import FormidableForm, widgets, fields


class TestDynamicForm(TestCase):

    def setUp(self):
        self.form = Formidable.objects.create(label='test',
                                              description='desc')
        self.text_field = self.form.fields.create(
            slug='text-input', type_id='text', label='mytext',
            order=self.form.get_next_field_order()
        )

    def test_field_order(self):
        _1 = self.form.fields.create(slug='text', type_id='text', order=1)
        _2 = self.form.fields.create(slug='text2', type_id='text', order=2)
        _3 = self.form.fields.create(slug='text3', type_id='text', order=3)
        form_class = self.form.get_django_form_class()
        ordered_fields = ['text-input', 'text', 'text2', 'text3']
        for index, field_name in enumerate(form_class.declared_fields.keys()):
            self.assertEqual(ordered_fields[index], field_name)
        _1.order = 3
        _1.save()
        _2.order = 1
        _2.save()
        _3.order = 0
        _3.save()
        self.text_field.order = 2
        self.text_field.save()
        ordered_fields = ['text3', 'text2', 'text-input', 'text']
        form_class = self.form.get_django_form_class()
        for index, field_name in enumerate(form_class.declared_fields.keys()):
            self.assertEqual(ordered_fields[index], field_name)

    def test_text_input(self):
        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('text-input', form.fields)
        text = form.fields['text-input']
        self.assertEquals(text.required, False)
        self.assertEquals(type(text), forms.CharField)
        self.assertEquals(type(text.widget), forms.TextInput)

    def test_help_text(self):
        self.form.fields.create(
            slug='my-helptext', type_id='help_text',
            help_text='Here a Heptext',
            order=self.form.get_next_field_order()
        )
        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('my-helptext', form.fields)
        text = form.fields['my-helptext']
        self.assertEquals(type(text), fields.HelpTextField)
        self.assertEquals(type(text.widget), widgets.HelpTextWidget)
        self.assertEquals(text.text, 'Here a Heptext')

    def test_file_field(self):
        self.form.fields.create(
            slug='my-file', type_id='file',
            order=self.form.get_next_field_order()
        )
        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('my-file', form.fields)
        field = form.fields['my-file']
        self.assertEqual(type(field), forms.FileField)

    def test_title_field(self):
        self.form.fields.create(
            slug='my-title', type_id='title', label='Hello',
            order=self.form.get_next_field_order()
        )
        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('my-title', form.fields)
        text = form.fields['my-title']
        self.assertEquals(type(text), fields.TitleField)
        self.assertEquals(type(text.widget), widgets.TitleWidget)
        self.assertEquals(text.label, 'Hello')

    def test_separator_field(self):
        self.form.fields.create(
            slug='separator', type_id='separator',
            order=self.form.get_next_field_order()
        )
        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('separator', form.fields)
        field = form.fields['separator']
        self.assertEquals(type(field), fields.SeparatorField)
        self.assertEquals(type(field.widget), widgets.SeparatorWidget)

    def test_paragraph_input(self):
        self.form.fields.create(
            slug='area-input', type_id='paragraph', label='type a msg',
            order=self.form.get_next_field_order()
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
            slug='weapons', type_id='dropdown', label='chose you weapon',
            order=self.form.get_next_field_order()
        )
        for key in ['sword', 'gun']:
            drop.items.create(
                value=key, label=key, order=drop.get_next_order()
            )

        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('weapons', form.fields)
        dropdown = form.fields['weapons']
        self.assertEquals(type(dropdown), forms.ChoiceField)
        self.assertEquals(type(dropdown.widget), forms.Select)
        self.assertTrue(dropdown.choices)
        self.assertEquals(len(dropdown.choices), 2)

    def test_email_input(self):
        self.form.fields.create(
            slug='email', type_id='email', label='my email',
            order=self.form.get_next_field_order()
        )
        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('email', form.fields)
        email = form.fields['email']
        self.assertEqual(type(email), forms.EmailField)

    def test_checkbox(self):
        self.form.fields.create(
            slug='checkbox', type_id='checkbox', label='checkbox',
            order=self.form.get_next_field_order(),
        )

        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('checkbox', form.fields)
        checkbox = form.fields['checkbox']
        self.assertEqual(type(checkbox), forms.BooleanField)

    def test_checkboxes(self):
        self.form.fields.create(
            slug='checkboxes', type_id='checkboxes', label='checkboxes',
            order=self.form.get_next_field_order(),
        )

        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('checkboxes', form.fields)
        checkboxes = form.fields['checkboxes']
        self.assertEqual(type(checkboxes), forms.MultipleChoiceField)

    def test_dropdown_input_multiple(self):
        drop = self.form.fields.create(
            slug='multiple-weapons', type_id='dropdown',
            label='chose you weapon', multiple=True,
            order=self.form.get_next_field_order()
        )
        for key in ['sword', 'gun']:
            drop.items.create(
                value=key, label=key, order=drop.get_next_order()
            )

        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('multiple-weapons', form.fields)
        dropdown = form.fields['multiple-weapons']
        self.assertEquals(type(dropdown), forms.MultipleChoiceField)
        self.assertEquals(type(dropdown.widget), forms.SelectMultiple)
        self.assertTrue(dropdown.choices)
        self.assertEquals(len(dropdown.choices), 2)

    def test_radio_input(self):
        field = self.form.fields.create(
            slug='input-radio', type_id='radios',
            label='chose you weapon',
            order=self.form.get_next_field_order()
        )
        for key in ['sword', 'gun']:
            field.items.create(
                value=key, label=key, order=field.get_next_order()
            )

        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('input-radio', form.fields)
        radio = form.fields['input-radio']
        self.assertEquals(type(radio), forms.ChoiceField)
        self.assertEquals(type(radio.widget), forms.RadioSelect)
        self.assertTrue(radio.choices)
        self.assertEquals(len(radio.choices), 2)

    def test_radio_buttons(self):
        field = self.form.fields.create(
            slug='input-radio-buttons', type_id='radios_buttons',
            label='chose you weapon',
            order=self.form.get_next_field_order()
        )
        for key in ['sword', 'gun']:
            field.items.create(
                value=key, label=key, order=field.get_next_order()
            )

        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('input-radio-buttons', form.fields)
        radio = form.fields['input-radio-buttons']
        self.assertEquals(type(radio), forms.ChoiceField)
        self.assertEquals(type(radio.widget), forms.RadioSelect)
        self.assertTrue(radio.choices)
        self.assertEquals(len(radio.choices), 2)

    def test_date_field(self):
        self.form.fields.create(
            slug='input-date', type_id='date', label='your date',
            order=self.form.get_next_field_order()
        )
        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('input-date', form.fields)
        date = form.fields['input-date']
        self.assertEquals(type(date), forms.DateField)

    def test_number_field(self):
        self.form.fields.create(
            slug='input-number', type_id='number', label='your number',
            order=self.form.get_next_field_order()
        )
        form_class = self.form.get_django_form_class()
        form = form_class()
        self.assertIn('input-number', form.fields)
        number = form.fields['input-number']
        self.assertEquals(type(number), forms.DecimalField, type(number))

    def test_required_field(self):
        self.text_field.accesses.create(access_id='human', level=REQUIRED)
        form_class = self.form.get_django_form_class(role='human')
        form = form_class()
        self.assertIn('text-input', form.fields)
        self.assertEquals(form.fields['text-input'].required, True)

    def test_editable_field(self):
        self.text_field.accesses.create(access_id='human', level=EDITABLE)
        form_class = self.form.get_django_form_class(role='human')
        form = form_class()
        self.assertIn('text-input', form.fields)
        self.assertEquals(form.fields['text-input'].required, False)

    def test_readonly_field(self):
        self.text_field.accesses.create(access_id='human', level=READONLY)
        form_class = self.form.get_django_form_class(role='human')
        form = form_class()
        self.assertIn('text-input', form.fields)
        field = form.fields['text-input']
        self.assertEquals(field.required, False)
        self.assertEquals(field.widget.attrs['disabled'], True)

    def test_no_disabled_attr(self):
        self.text_field.accesses.create(access_id='human', level=EDITABLE)
        form_class = self.form.get_django_form_class(role='human')
        form = form_class()
        self.assertIn('text-input', form.fields)
        field = form.fields['text-input']
        self.assertEquals(field.required, False)
        self.assertNotIn('disabled', field.widget.attrs)

    def test_hidden_field(self):
        self.text_field.accesses.create(access_id='human', level=HIDDEN)
        form_class = self.form.get_django_form_class(role='human')
        form = form_class()
        self.assertNotIn('text-input', form.fields)

    def test_queryset_with_role(self):
        class MyForm(FormidableForm):
            first_name = fields.CharField(default='foo')
            last_name = fields.CharField(default='bar')
            origin = fields.ChoiceField(
                choices=(('fr', 'France'), ('en', 'England'))
            )
            weapons = fields.ChoiceField(
                choices=(('gun', 'Gun'), ('sword', 'Sword'))
            )

        form = MyForm.to_formidable(label='test')

        with django_perf_rec.record(path='perfs/'):
            form.get_django_form_class(role='jedi')

    def test_queryset_without_role(self):
        class MyForm(FormidableForm):
            first_name = fields.CharField(default='foo')
            last_name = fields.CharField(default='bar')
            origin = fields.ChoiceField(
                choices=(('fr', 'France'), ('en', 'England'))
            )
            weapons = fields.ChoiceField(
                choices=(('gun', 'Gun'), ('sword', 'Sword'))
            )

        form = MyForm.to_formidable(label='test')

        with django_perf_rec.record(path='perfs/'):
            form.get_django_form_class(role='jedi')


class TestFormValidation(TestCase):

    def setUp(self):
        self.form = Formidable.objects.create(label='test',
                                              description='desc')
        self.text_field = self.form.fields.create(
            slug='text-input', type_id='text', label='mytext',
            order=self.form.get_next_field_order()
        )

    def test_min_length_ko(self):
        self.text_field.validations.create(type='MINLENGTH', value='5')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'text-input': '1234'})
        self.assertFalse(form.is_valid())

    def test_min_length_ok(self):
        self.text_field.validations.create(type='MINLENGTH', value='5')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'text-input': '12345'})
        self.assertTrue(form.is_valid())

    def test_max_length_ok(self):
        self.text_field.validations.create(type='MAXLENGTH', value='4')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'text-input': '12345'})
        self.assertFalse(form.is_valid())

    def test_max_length_ko(self):
        self.text_field.validations.create(type='MAXLENGTH', value='4')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'text-input': '123'})
        self.assertTrue(form.is_valid())

    def test_regex_ok(self):
        self.text_field.validations.create(type='REGEXP', value=r'^[0-9]+$')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'text-input': '12345'})
        self.assertTrue(form.is_valid())

    def test_regex_ko(self):
        self.text_field.validations.create(type='REGEXP', value=r'^[0-9]+$')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'text-input': 'abcd1234'})
        self.assertFalse(form.is_valid())

    def test_regexp_max_length(self):
        self.text_field.validations.create(type='REGEXP', value=r'^[0-9]+$')
        self.text_field.validations.create(type='MINLENGTH', value='5')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'text-input': '1234'})
        self.assertFalse(form.is_valid())
        form = form_class(data={'text-input': '1234abcdef'})
        self.assertFalse(form.is_valid())
        form = form_class(data={'text-input': '123456789'})
        self.assertTrue(form.is_valid())

    def test_gt_ok(self):
        number = self.form.fields.create(
            slug='input-number', type_id='number', label='your number',
            order=self.form.get_next_field_order()
        )
        number.validations.create(type='GT', value='21')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-number': '42'})
        self.assertTrue(form.is_valid())

    def test_gt_ko(self):
        number = self.form.fields.create(
            slug='input-number', type_id='number', label='your number',
            order=self.form.get_next_field_order()
        )
        number.validations.create(type='GT', value='21')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-number': '21'})
        self.assertFalse(form.is_valid())
        form = form_class(data={'input-number': '20'})
        self.assertFalse(form.is_valid())

    def test_gte_ok(self):
        number = self.form.fields.create(
            slug='input-number', type_id='number', label='your number',
            order=self.form.get_next_field_order()
        )
        number.validations.create(type='GTE', value='21')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-number': '21'})
        self.assertTrue(form.is_valid())
        form = form_class(data={'input-number': '22'})
        self.assertTrue(form.is_valid())

    def test_gte_ko(self):
        number = self.form.fields.create(
            slug='input-number', type_id='number', label='your number',
            order=self.form.get_next_field_order()
        )
        number.validations.create(type='GTE', value='21')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-number': '20'})
        self.assertFalse(form.is_valid())

    def test_lte_ok(self):
        number = self.form.fields.create(
            slug='input-number', type_id='number', label='your number',
            order=self.form.get_next_field_order()
        )
        number.validations.create(type='LTE', value='21')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-number': '21'})
        self.assertTrue(form.is_valid())
        form = form_class(data={'input-number': '20'})
        self.assertTrue(form.is_valid())

    def test_lte_ko(self):
        number = self.form.fields.create(
            slug='input-number', type_id='number', label='your number',
            order=self.form.get_next_field_order()
        )
        number.validations.create(type='LT', value='21')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-number': '22'})
        self.assertFalse(form.is_valid())

    def test_lt_ok(self):
        number = self.form.fields.create(
            slug='input-number', type_id='number', label='your number',
            order=self.form.get_next_field_order()
        )
        number.validations.create(type='LT', value='42')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-number': '21'})
        self.assertTrue(form.is_valid())

    def test_lt_ko(self):
        number = self.form.fields.create(
            slug='input-number', type_id='number', label='your number',
            order=self.form.get_next_field_order()
        )
        number.validations.create(type='LT', value='21')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-number': '21'})
        self.assertFalse(form.is_valid())
        form = form_class(data={'input-number': '22'})
        self.assertFalse(form.is_valid())

    def test_eq_number_ok(self):
        number = self.form.fields.create(
            slug='input-number', type_id='number', label='your number',
            order=self.form.get_next_field_order()
        )
        number.validations.create(type='EQ', value='21')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-number': '21.0'})
        self.assertTrue(form.is_valid())

    def test_eq_number_ko(self):
        number = self.form.fields.create(
            slug='input-number', type_id='number', label='your number',
            order=self.form.get_next_field_order()
        )
        number.validations.create(type='EQ', value='21')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-number': '22.0'})
        self.assertFalse(form.is_valid())

    def test_neq_number_ok(self):
        number = self.form.fields.create(
            slug='input-number', type_id='number', label='your number',
            order=self.form.get_next_field_order()
        )
        number.validations.create(type='NEQ', value='21')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-number': '22.0'})
        self.assertTrue(form.is_valid())

    def test_neq_number_ko(self):
        number = self.form.fields.create(
            slug='input-number', type_id='number', label='your number',
            order=self.form.get_next_field_order()
        )
        number.validations.create(type='NEQ', value='21')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-number': '21.0'})
        self.assertFalse(form.is_valid())

    def test_eq_str_ok(self):
        field = self.form.fields.create(
            slug='input-text', type_id='text', label='your text',
            order=self.form.get_next_field_order()
        )
        field.validations.create(type='EQ', value='21')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-number': '21'})
        self.assertTrue(form.is_valid())

    def test_eq_str_ko(self):
        text = self.form.fields.create(
            slug='input-text', type_id='text', label='your text',
            order=self.form.get_next_field_order()
        )
        text.validations.create(type='EQ', value='21')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-text': '22'})
        self.assertFalse(form.is_valid())

    def test_neq_str_ok(self):
        text = self.form.fields.create(
            slug='input-text', type_id='text', label='your text',
            order=self.form.get_next_field_order()
        )
        text.validations.create(type='NEQ', value='21')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-text': '22'})
        self.assertTrue(form.is_valid())

    def test_neq_str_ko(self):
        text = self.form.fields.create(
            slug='input-text', type_id='text', label='your text',
            order=self.form.get_next_field_order()
        )
        text.validations.create(type='NEQ', value='21')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-text': '21'})
        self.assertFalse(form.is_valid())

    def test_eq_date_ok(self):
        field = self.form.fields.create(
            slug='input-text', type_id='date', label='your text',
            order=self.form.get_next_field_order()
        )
        field.validations.create(type='EQ', value='12/21/2012')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-number': '12/21/2012'})
        self.assertTrue(form.is_valid())

    def test_eq_date_ko(self):
        text = self.form.fields.create(
            slug='input-text', type_id='date', label='your text',
            order=self.form.get_next_field_order()
        )
        text.validations.create(type='EQ', value='12/21/2012')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-text': '22/12/2012'})
        self.assertFalse(form.is_valid())

    def test_neq_date_ok(self):
        text = self.form.fields.create(
            slug='input-text', type_id='date', label='your text',
            order=self.form.get_next_field_order()
        )
        text.validations.create(type='NEQ', value='12/21/2012')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-text': '12/22/2012'})
        self.assertTrue(form.is_valid())

    def test_neq_date_ko(self):
        text = self.form.fields.create(
            slug='input-text', type_id='date', label='your text',
            order=self.form.get_next_field_order()
        )
        text.validations.create(type='NEQ', value='12/21/2012')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-text': '12/21/2012'})
        self.assertFalse(form.is_valid())

    def test_lt_date_ok(self):
        field = self.form.fields.create(
            slug='input-date', type_id='date', label='your date',
            order=self.form.get_next_field_order()
        )
        field.validations.create(type='LT', value='12/21/2012')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-date': '12/20/2012'})
        self.assertTrue(form.is_valid())

    def test_lt_date_ko(self):
        field = self.form.fields.create(
            slug='input-date', type_id='date', label='your date',
            order=self.form.get_next_field_order()
        )
        field.validations.create(type='LT', value='12/21/2012')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-date': '12/21/2012'})
        self.assertFalse(form.is_valid())
        form = form_class(data={'input-date': '12/22/2012'})
        self.assertFalse(form.is_valid())

    def test_lte_date_ok(self):
        field = self.form.fields.create(
            slug='input-date', type_id='date', label='your date',
            order=self.form.get_next_field_order()
        )
        field.validations.create(type='LTE', value='12/21/2012')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-date': '12/20/2012'})
        self.assertTrue(form.is_valid())
        form = form_class(data={'input-date': '12/21/2012'})
        self.assertTrue(form.is_valid())

    def test_lte_date_ko(self):
        field = self.form.fields.create(
            slug='input-date', type_id='date', label='your date',
            order=self.form.get_next_field_order()
        )
        field.validations.create(type='LT', value='12/21/2012')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-date': '12/22/2012'})
        self.assertFalse(form.is_valid())

    def test_gt_date_ok(self):
        field = self.form.fields.create(
            slug='input-date', type_id='date', label='your date',
            order=self.form.get_next_field_order()
        )
        field.validations.create(type='GT', value='12/21/2012')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-date': '12/22/2012'})
        self.assertTrue(form.is_valid())

    def test_gt_date_ko(self):
        field = self.form.fields.create(
            slug='input-date', type_id='date', label='your date',
            order=self.form.get_next_field_order()
        )
        field.validations.create(type='GT', value='12/21/2012')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-date': '12/21/2012'})
        self.assertFalse(form.is_valid())
        form = form_class(data={'input-date': '12/20/2012'})
        self.assertFalse(form.is_valid())

    def test_gte_date_ok(self):
        field = self.form.fields.create(
            slug='input-date', type_id='date', label='your date',
            order=self.form.get_next_field_order()
        )
        field.validations.create(type='GTE', value='12/21/2012')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-date': '12/21/2012'})
        self.assertTrue(form.is_valid())
        form = form_class(data={'input-date': '12/23/2012'})
        self.assertTrue(form.is_valid())

    def test_gte_date_ko(self):
        field = self.form.fields.create(
            slug='input-date', type_id='date', label='your date',
            order=self.form.get_next_field_order()
        )
        field.validations.create(type='GT', value='12/21/2012')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-date': '12/20/2012'})
        self.assertFalse(form.is_valid())

    @freeze_time('2012-12-21')
    def test_date_is_in_the_future_ok(self):
        field = self.form.fields.create(
            slug='input-date', type_id='date', label='your date',
            order=self.form.get_next_field_order()
        )
        field.validations.create(type='IS_DATE_IN_THE_FUTURE',
                                 value='false')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-date': '12/20/2012'})
        self.assertTrue(form.is_valid())
        form = form_class(data={'input-date': '12/21/2012'})
        self.assertTrue(form.is_valid())
        field.validations.update(value='true')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-date': '12/22/2012'})
        self.assertTrue(form.is_valid())

    @freeze_time('2012-12-21')
    def test_date_is_in_the_future_ko(self):
        field = self.form.fields.create(
            slug='input-date', type_id='date', label='your date',
            order=self.form.get_next_field_order()
        )
        field.validations.create(type='IS_DATE_IN_THE_FUTURE',
                                 value='false')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-date': '12/22/2012'})
        self.assertFalse(form.is_valid())
        field.validations.update(value='true')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-date': '12/20/2012'})
        self.assertFalse(form.is_valid())
        form = form_class(data={'input-date': '12/21/2012'})
        self.assertFalse(form.is_valid())

    @freeze_time('2012-01-01')
    def test_is_age_above_ok(self):
        field = self.form.fields.create(
            slug='input-date', type_id='date', label='your date',
            order=self.form.get_next_field_order()
        )
        field.validations.create(type='IS_AGE_ABOVE',
                                 value='20')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-date': '01/01/1990'})
        self.assertTrue(form.is_valid())
        form = form_class(data={'input-date': '01/01/1992'})
        self.assertTrue(form.is_valid())

    @freeze_time('2012-01-01')
    def test_is_age_above_ko(self):
        field = self.form.fields.create(
            slug='input-date', type_id='date', label='your date',
            order=self.form.get_next_field_order()
        )
        field.validations.create(type='IS_AGE_ABOVE',
                                 value='20')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-date': '01/01/2000'})
        self.assertFalse(form.is_valid())

    @freeze_time('2012-01-01')
    def test_is_age_under_ko(self):
        field = self.form.fields.create(
            slug='input-date', type_id='date', label='your date',
            order=self.form.get_next_field_order()
        )
        field.validations.create(type='IS_AGE_UNDER',
                                 value='20')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-date': '01/01/1990'})
        self.assertFalse(form.is_valid())
        form = form_class(data={'input-date': '01/01/1992'})
        self.assertFalse(form.is_valid())

    @freeze_time('2012-01-01')
    def test_is_age_under_ok(self):
        field = self.form.fields.create(
            slug='input-date', type_id='date', label='your date',
            order=self.form.get_next_field_order()
        )
        field.validations.create(type='IS_AGE_UNDER',
                                 value='20')
        form_class = self.form.get_django_form_class()
        form = form_class(data={'input-date': '01/01/2000'})
        self.assertTrue(form.is_valid())


class FormidableModelTestCase(TestCase):

    def test_from_json(self):
        """
        We try to build a ``Formidable`` object from a valid JSON.
        We should have an instance of ``Formidable``.

        """
        filepath = os.path.join(os.path.dirname(__file__),
                                '../fixtures/augmentation_heures.json')
        with io.open(filepath, 'r', encoding='utf-8') as f:
            schema_definition = json.load(f)

        form = Formidable.from_json(schema_definition)

        self.assertTrue(isinstance(form, Formidable))

    def test_from_json_raised_error(self):
        """
        We try to create a ``Formidable`` object with an invalid JSON.
        This will raise a ``ValidationError``.

        """
        with self.assertRaises(ValidationError) as context:
            Formidable.from_json({'json_invalid': True})

        self.assertEqual(len(context.exception.messages), 3)
        for message in context.exception.messages:
            self.assertEqual(message, 'This field is required.')
