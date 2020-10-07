import os
import json
import datetime
from decimal import Decimal

from copy import deepcopy

from django.conf import settings
from django.db import DatabaseError
from django.urls import reverse
import django_perf_rec

from freezegun import freeze_time
from rest_framework.test import APITestCase

from formidable.models import Formidable
from formidable.accesses import get_accesses
from formidable.forms import FormidableForm, fields, get_dynamic_form_class
from formidable import validators, constants

from . import form_data, form_data_items, form_data_readonly

from unittest.mock import patch


TESTS_DIR = os.path.dirname(os.path.abspath(__file__))


class FormidableAPITestCase(APITestCase):

    def check_errors_format(self, data):
        # keys must be in {'code', 'message', 'errors'}
        # 'errors' is optional
        self.assertFalse(set(data.keys()) - {'code', 'message', 'errors'})
        self.assertIn('code', data)
        self.assertIn('message', data)
        for error in data.get('errors', []):
            self.assertFalse(set(error.keys()) - {'code', 'message', 'field'})
            # 'field' is optional
            self.assertIn('code', error)
            self.assertIn('message', error)


class MyTestForm(FormidableForm):
    name = fields.CharField(label='Name', accesses={'jedi': 'REQUIRED'})
    birth_date = fields.DateField(
        label='Your Birth Date',
        validators=[
            validators.AgeAboveValidator(
                21, message='You cannot be a jedi until your 21'
            ),
            validators.DateIsInFuture(False)
        ],
        accesses={'jedi': 'REQUIRED'},
    )
    out_date = fields.DateField(
        validators=[validators.DateIsInFuture(True)]
    )
    weapons = fields.ChoiceField(choices=[
        ('gun', 'blaster'), ('sword', 'light saber')
    ])
    salary = fields.NumberField(
        validators=[
            validators.GTValidator(0), validators.LTEValidator(25)
        ],
        accesses={'jedi': 'HIDDEN', 'jedi-master': 'REQUIRED'}
    )


class CreateFormTestCase(FormidableAPITestCase):

    def test_simple(self):
        initial_count = Formidable.objects.count()
        res = self.client.post(
            reverse('formidable:form_create'), form_data, format='json'
        )
        self.assertEquals(res.status_code, 201)
        self.assertEquals(initial_count + 1, Formidable.objects.count())
        formidable = Formidable.objects.order_by('pk').last()
        self.assertEquals(formidable.fields.count(), 1)
        field = formidable.fields.first()
        self.assertEquals(field.accesses.count(), 5)
        accesses = [
            ('padawan', 'REQUIRED'), ('jedi', 'EDITABLE'),
            ('jedi-master', 'READONLY'), ('human', 'HIDDEN'),
        ]
        for access, level in accesses:
            self.assertTrue(
                field.accesses.filter(access_id=access, level=level).exists()
            )

    def test_trailing_slash(self):
        url = reverse('formidable:form_create')
        self.assertFalse(url.endswith('/'))
        res = self.client.post(
            url, form_data, format='json'
        )
        self.assertEquals(res.status_code, 201)
        res = self.client.post(
            url + '/', form_data, format='json'
        )
        self.assertEquals(res.status_code, 201)

    def test_fields_slug(self):
        data = deepcopy(form_data)
        # duplicate field
        data['fields'] *= 2
        res = self.client.post(
            reverse('formidable:form_create'), data, format='json'
        )
        self.assertEquals(res.status_code, 422)
        self.check_errors_format(res.data)

    def test_with_items_in_fields(self):
        initial_count = Formidable.objects.count()
        res = self.client.post(
            reverse('formidable:form_create'), form_data_items, format='json'
        )
        self.assertEquals(res.status_code, 201)
        self.assertEquals(initial_count + 1, Formidable.objects.count())
        formidable = Formidable.objects.order_by('pk').last()
        self.assertEquals(formidable.fields.count(), 1)
        field = formidable.fields.first()
        self.assertEquals(field.items.count(), 2)

    def test_forgotten_items_fields(self):
        form_data_without_items = deepcopy(form_data_items)
        form_data_without_items['fields'][0].pop('items')
        res = self.client.post(
            reverse('formidable:form_create'), form_data_without_items,
            format='json'
        )
        self.assertEquals(res.status_code, 422)
        self.check_errors_format(res.data)

    def test_with_unknown_accesses(self):
        form_data_copy = deepcopy(form_data)
        field = form_data_copy['fields'][0]
        field['accesses'][0]['access_id'] = 'NOT_A_LEVEL'
        res = self.client.post(
            reverse('formidable:form_create'), form_data_copy,
            format='json'
        )
        self.assertEquals(res.status_code, 422)
        self.check_errors_format(res.data)


class UpdateFormTestCase(FormidableAPITestCase):

    def setUp(self):
        super().setUp()
        self.form = Formidable.objects.create(
            label='test', description='test'
        )

    @property
    def edit_url(self):
        return reverse(
            'formidable:form_detail', args=[self.form.id]
        )

    def test_simple(self):
        initial_count = Formidable.objects.count()
        data = {
            'label': 'edited label',
            'description': 'edited description',
            'fields': []
        }
        res = self.client.put(self.edit_url, data, format="json")
        self.assertEquals(res.status_code, 200)
        formidable = Formidable.objects.order_by('pk').last()
        self.assertEquals(formidable.pk, self.form.pk)
        self.assertEquals(formidable.label, 'edited label')
        self.assertEquals(formidable.description, 'edited description')
        self.assertEquals(Formidable.objects.count(), initial_count)

    def test_trailing_slash_on_put(self):
        data = {
            'label': 'edited label',
            'description': 'edited description',
            'fields': []
        }
        url = self.edit_url
        self.assertFalse(url.endswith('/'))
        res = self.client.put(
            url, data, format="json"
        )
        self.assertEquals(res.status_code, 200)
        res = self.client.put(
            url + '/', form_data, format='json'
        )
        self.assertEquals(res.status_code, 200)

    def test_trailing_slash_on_get(self):
        data = {
            'label': 'edited label',
            'description': 'edited description',
            'fields': []
        }
        url = self.edit_url
        self.assertFalse(url.endswith('/'))
        res = self.client.get(
            url, data
        )
        self.assertEquals(res.status_code, 200)
        res = self.client.get(
            url + '/', form_data
        )
        self.assertEquals(res.status_code, 200)

    def test_update_simple_fields(self):
        field = self.form.fields.create(
            type_id='text', slug='textslug', label='mytext',
            order=self.form.get_next_field_order()
        )
        for access in get_accesses():
            field.accesses.create(access_id=access.id, level='EDITABLE')
        res = self.client.put(self.edit_url, form_data, format='json')
        self.assertEquals(res.status_code, 200)
        form = Formidable.objects.order_by('pk').last()
        self.assertEquals(form.pk, self.form.pk)
        self.assertEquals(form.fields.count(), 1)
        field = form.fields.first()
        self.assertEquals(field.label, 'hello')
        self.assertEquals(field.accesses.count(), 5)

    def test_create_field_on_update(self):
        field = self.form.fields.create(
            type_id='text', slug='textslug', label='mytext',
            order=self.form.get_next_field_order()
        )
        for access in get_accesses():
            field.accesses.create(access_id=access.id, level='EDITABLE')

        data = deepcopy(form_data)
        data['fields'].extend(form_data_items['fields'])
        res = self.client.put(self.edit_url, data, format='json')
        self.assertEquals(res.status_code, 200)
        form = Formidable.objects.order_by('pk').last()
        self.assertEquals(form.pk, self.form.pk)
        self.assertEquals(form.fields.count(), 2)

    def test_duplicate_items_update(self):
        # create a form with items
        data = deepcopy(form_data_items)
        res = self.client.put(self.edit_url, data, format='json')
        self.assertEquals(res.status_code, 200)
        # update items with duplicate entries
        data['fields'] *= 2
        res = self.client.put(self.edit_url, data, format='json')
        # expect validation error
        self.assertEquals(res.status_code, 422)
        self.check_errors_format(res.data)

    def test_delete_field_on_update(self):
        self.form.fields.create(
            type_id='text', slug='textslug', label='mytext',
            order=self.form.get_next_field_order()
        )
        self.form.fields.create(
            order=self.form.get_next_field_order(),
            type_id='text', slug='delete-slug', label='text'
        )

        for access in get_accesses():
            for field in self.form.fields.all():
                field.accesses.create(access_id=access.id, level='EDITABLE')

        res = self.client.put(self.edit_url, form_data, format='json')
        self.assertEquals(res.status_code, 200)
        form = Formidable.objects.order_by('pk').last()
        self.assertEquals(form.pk, self.form.pk)
        self.assertEquals(form.fields.count(), 1)
        field = form.fields.first()
        self.assertEquals(field.label, 'hello')
        self.assertEquals(field.accesses.count(), 5)
        self.assertTrue(field.accesses.filter(
            access_id='padawan', level='REQUIRED'
        ).exists())
        self.assertTrue(field.accesses.filter(
            access_id='human', level='HIDDEN'
        ).exists())
        self.assertTrue(field.accesses.filter(
            access_id="jedi-master", level="READONLY"
        ).exists())

    def test_queryset_on_get(self):
        record_name = 'UpdateFormTestCase.test_queryset_on_get'
        if 'postgresql' in settings.DATABASES['default']['ENGINE']:
            record_name = '{}-pg'.format(record_name)

        with django_perf_rec.record(record_name=record_name, path='perfs/'):
            self.client.get(reverse(
                'formidable:form_detail', args=[self.form.pk])
            )

    def test_queryset_on_context_form_detail(self):
        record_name = 'UpdateFormTestCase.test_queryset_on_context_form_detail'
        if 'postgresql' in settings.DATABASES['default']['ENGINE']:
            record_name = '{}-pg'.format(record_name)

        session = self.client.session
        session['role'] = 'padawan'
        session.save()

        with django_perf_rec.record(record_name=record_name, path='perfs/'):
            self.client.get(reverse(
                'formidable:context_form_detail', args=[self.form.pk])
            )

    def test_non_regression_database_ordering(self):
        """
        Form update relies on database ordering (#215)
        """
        data = deepcopy(form_data)
        data['fields'][0]['slug'] = 'aaa'
        data['fields'].append(deepcopy(data['fields'][0]))
        data['fields'][1]['slug'] = 'BBB'
        data['fields'].append(deepcopy(data['fields'][0]))
        data['fields'][2]['slug'] = 'bbb'
        from django.db.models import QuerySet
        original_order_by = QuerySet.order_by

        def order_by(self, *fields):
            if fields == ('slug',):
                fields = ('-slug',)
            return original_order_by(self, *fields)

        # create/update the form
        res = self.client.put(self.edit_url, data, format='json')
        self.assertEquals(res.status_code, 200, res)
        # update the same form
        with patch.object(QuerySet, 'order_by', order_by):
            res = self.client.put(self.edit_url, data, format='json')
        self.assertEquals(res.status_code, 200, res)

    def test_simple_database_error_update(self):
        data = {
            'label': 'edited label',
            'description': 'edited description',
            'fields': []
        }
        with patch('formidable.views.FormidableDetail.get_queryset') as patched:  # noqa
            patched.side_effect = DatabaseError(
                'could not obtain lock on row...')
            res = self.client.put(self.edit_url, data, format="json")
        # 409 means "CONFLICT"
        self.assertEquals(res.status_code, 409)
        self.assertEquals(
            res.json(),
            {
                "code": "permission_denied",
                "message": "Database error, operation failed"
            }
        )


class TestAccess(FormidableAPITestCase):

    def test_get(self):
        response = self.client.get(reverse('formidable:accesses_list'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 5)
        for access in response.data:
            self.assertIn('id', access)
            self.assertIn('label', access)
            self.assertIn(
                access['id'], [obj.id for obj in get_accesses()]
            )
            self.assertIn(
                access['label'], [obj.label for obj in get_accesses()]
            )
            self.assertIn('preview_as', access)
            if access['id'] == 'robot':
                self.assertEqual(access['preview_as'], 'TABLE')
            else:
                self.assertEqual(access['preview_as'], 'FORM')


class TestReadonlyDefault(FormidableAPITestCase):
    def test_form_readonly_empty_submit(self):
        res = self.client.post(
            reverse('formidable:form_create'),
            form_data_readonly, format='json')
        self.assertEquals(res.status_code, 201)
        formidable = Formidable.objects.order_by('pk').last()
        form_class = get_dynamic_form_class(formidable, 'padawan')
        form = form_class({})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, {
            'readonly_text': 'Hello World!',
            'readonly_paragraph': 'Hello World!',
            'readonly_date': datetime.date(2020, 9, 29),
            'readonly_number': Decimal('10'),
            'readonly_email': 'jon.europe@example.com',
            'readonly_dropdown': 'val1',
            'readonly_multiple_dropdown': ['val2', 'val3'],
            'readonly_checkbox': True,
            'readonly_checkboxes': ['val2', 'val3'],
            'readonly_radios': 'val1',
            'readonly_radios_buttons': 'val1'
        })

    def test_form_readonly_empty_defaults(self):

        form_data = deepcopy(form_data_readonly)
        # Preparing a "bad" defaults
        for field in form_data['fields']:
            field['defaults'].append("")  # empty value

        res = self.client.post(
            reverse('formidable:form_create'),
            form_data, format='json')
        self.assertEquals(res.status_code, 201)
        formidable = Formidable.objects.order_by('pk').last()
        form_class = get_dynamic_form_class(formidable, 'padawan')
        form = form_class({})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, {
            'readonly_text': 'Hello World!',
            'readonly_paragraph': 'Hello World!',
            'readonly_date': datetime.date(2020, 9, 29),
            'readonly_number': Decimal('10'),
            'readonly_email': 'jon.europe@example.com',
            'readonly_dropdown': 'val1',
            'readonly_multiple_dropdown': ['val2', 'val3'],
            'readonly_checkbox': True,
            'readonly_checkboxes': ['val2', 'val3'],
            'readonly_radios': 'val1',
            'readonly_radios_buttons': 'val1'
        })

    def test_validate_form_readonly_empty_defaults(self):

        session = self.client.session
        session['role'] = 'padawan'
        session.save()

        form_data = deepcopy(form_data_readonly)
        # Preparing a "bad" defaults
        for field in form_data['fields']:
            field['defaults'].append("")  # empty value

        res = self.client.post(
            reverse('formidable:form_create'),
            form_data, format='json')
        self.assertEquals(res.status_code, 201)
        formidable = Formidable.objects.order_by('pk').last()

        # Validation from schema
        res = self.client.post(
            reverse('form_validation_schema', args=[formidable.pk]),
            {}, format='json'
        )
        self.assertEqual(res.status_code, 204)
        self.assertIn(res.content, ("", b""))  # Should be empty
        # As a consequence, if there's no body content, there shouldn't be any
        # content-type sent back to the client.


class TestChain(FormidableAPITestCase):

    def setUp(self):
        super().setUp()
        self.form = MyTestForm.to_formidable(label='Jedi Form')
        self.assertTrue(self.form.pk)

    @freeze_time('2021-01-01')
    def test_jedi_form_valid(self):
        form_class = self.form.get_django_form_class(role='jedi')
        form = form_class(data={
            'name': 'Gerard', 'birth_date': '1998-01-01', 'weapons': 'gun',
            'out_date': '2042-01-01'
        })
        self.assertTrue(form.is_valid())

    @freeze_time('2021-01-01')
    def test_jedi_form_form_invalid(self):
        form_class = self.form.get_django_form_class(role='jedi')
        form = form_class(data={
            'name': 'Gerard', 'birth_date': '2010-01-01', 'weapons': 'gun',
            'out_date': '2042-01-01'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('birth_date', form.errors)
        self.assertEquals(
            form.errors['birth_date'][0],
            'You cannot be a jedi until your 21'
        )


class MyForm(FormidableForm):
    first_name = fields.CharField(
        accesses={'padawan': constants.REQUIRED},
    )
    last_name = fields.CharField(
        accesses={'padawan': constants.REQUIRED},
        validators=[validators.MinLengthValidator(5)]
    )


class TestValidationEndPoint(FormidableAPITestCase):
    url = 'formidable:form_validation'

    def setUp(self):
        super().setUp()
        self.formidable = MyForm.to_formidable(label='title')

    def test_validate_data_ok(self):
        parameters = {
            'first_name': 'Guillaume',
            'last_name': 'Gérard',
        }
        session = self.client.session
        session['role'] = 'padawan'
        session.save()
        res = self.client.post(
            reverse(self.url, args=[self.formidable.pk]),
            parameters, format='json'
        )
        self.assertEqual(res.status_code, 204)
        self.assertIn(res.content, ("", b""))  # Should be empty
        # As a consequence, if there's no body content, there shouldn't be any
        # content-type sent back to the client.

    def test_formidable_does_not_exist(self):
        parameters = {
            'first_name': 'Guillaume',
            'last_name': 'Gérard',
        }
        session = self.client.session
        session['role'] = 'padawan'
        session.save()
        res = self.client.post(
            reverse(self.url, args=[9999]),
            parameters, format='json'
        )
        self.assertEqual(res.status_code, 404)

    def test_validate_data_ko(self):
        parameters = {
            'last_name': 'Gérard',
        }
        session = self.client.session
        session['role'] = 'padawan'
        session.save()
        res = self.client.post(
            reverse(self.url, args=[self.formidable.pk]),
            parameters, format='json'
        )
        self.assertEqual(res.status_code, 400)
        errors = res.data
        self.assertIn('first_name', errors)
        self.assertIn('application/json', str(res.serialize_headers()))

    def test_validate_with_mandatory_file(self):
        class WithFile(FormidableForm):
            mandatory = fields.FileField(
                accesses={'padawan': constants.REQUIRED}
            )

        formidable = WithFile.to_formidable(label='test with file')
        parameters = {}
        session = self.client.session
        session['role'] = 'padawan'
        session.save()
        res = self.client.post(
            reverse(self.url, args=[formidable.pk]),
            parameters, format='json'
        )
        self.assertEqual(res.status_code, 204)

    def test_validate_with_mandatory_file_and_conditions(self):
        class WithFile(FormidableForm):
            checkbox = fields.BooleanField(
                label='My checkbox',
                accesses={'padawan': constants.EDITABLE}
            )
            mandatory = fields.FileField(
                accesses={'padawan': constants.REQUIRED}
            )

        formidable = WithFile.to_formidable(label='test with file')
        # mandatory to be checked only if the checkbox is on.
        formidable.conditions = [
            {
                'name': 'My Name',
                'action': 'display_iff',
                'fields_ids': ['mandatory'],
                'tests': [
                    {
                        'field_id': 'checkbox',
                        'operator': 'eq',
                        'values': [True],
                    }
                ]
            }
        ]
        formidable.save()

        # Set role for the session
        session = self.client.session
        session['role'] = 'padawan'
        session.save()

        # The checkbox is checked.
        parameters = {'checkbox': True}
        res = self.client.post(
            reverse(self.url, args=[formidable.pk]),
            parameters, format='json'
        )
        # We don't validate file fields, even if they're mandatory, because
        # they belong to the multi-part side of HTTP
        self.assertEqual(res.status_code, 204)

        # The checkbox is NOT checked.
        parameters = {'checkbox': False}
        res = self.client.post(
            reverse(self.url, args=[formidable.pk]),
            parameters, format='json'
        )
        # We still don't validate file fields.
        self.assertEqual(res.status_code, 204)

    def test_unallowed_method(self):
        parameters = {
            'first_name': 'Guillaume',
            'last_name': 'Gérard',
        }
        session = self.client.session
        session['role'] = 'padawan'
        session.save()
        # As of 1.4.0, GET is disallowed.
        res = self.client.get(
            reverse(self.url, args=[self.formidable.pk]),
            parameters, format='json'
        )
        self.assertEqual(res.status_code, 405)


class TestValidationFromSchemaEndPoint(TestValidationEndPoint):
    url = 'form_validation_schema'


class TestConditionalRulesWithDropDowns(FormidableAPITestCase):
    def test_can_validate_form_with_dropdown_conditional_fields(self):
        url = 'formidable:form_validation'

        class DropDownForm(FormidableForm):
            main_dropdown = fields.ChoiceField(
                choices=(
                    ('first', 'First'),
                    ('second', 'Second'),
                    ('third', 'Third'),
                ),
                accesses={'padawan': constants.EDITABLE}
            )
            first_field = fields.CharField(
                accesses={'padawan': constants.EDITABLE})
            second_field = fields.CharField(
                accesses={'padawan': constants.EDITABLE})
            third_field = fields.CharField(
                accesses={'padawan': constants.EDITABLE})
            another_field = fields.CharField(
                accesses={'padawan': constants.EDITABLE})

        form = DropDownForm.to_formidable(label='Drop Down Test Form')
        form.conditions = [
            {
                'name': 'Show first and second if value "first" selected',
                'action': 'display_iff',
                'fields_ids': ['first_field', 'second_field', ],
                'tests': [
                    {
                        'field_id': 'main_dropdown',
                        'operator': 'eq',
                        'values': ['first'],
                    }
                ]
            },
            {
                'name': 'Show third if value "second" selected',
                'action': 'display_iff',
                'fields_ids': ['third_field'],
                'tests': [
                    {
                        'field_id': 'main_dropdown',
                        'operator': 'eq',
                        'values': ['second'],
                    }
                ]
            }
        ]
        form.save()
        session = self.client.session
        session['role'] = 'padawan'
        session.save()
        res = self.client.post(
            reverse(url, args=[form.pk]),
            {"main_dropdown": "first", "third_field": "test"},
            format='json'
        )
        self.assertEqual(res.status_code, 204)

    def test_can_create_form_with_dropdown_conditional_fields_via_api(self):
        conditions_schema = json.load(open(
            os.path.join(
                TESTS_DIR, 'fixtures', 'drop-down-conditions.json'
            )
        ))
        session = self.client.session
        session['role'] = 'padawan'
        session.save()
        res = self.client.post(
            reverse('formidable:form_create'),
            conditions_schema,
            format='json'
        )
        self.assertEqual(res.status_code, 201)


class TestConditionalRulesWithMultiChoice(FormidableAPITestCase):

    def test_can_validate_form_with_multiple_choice_fields(self):
        url = 'formidable:form_validation'

        class MultipleChoiceForm(FormidableForm):
            main_choices = fields.MultipleChoiceField(
                choices=(
                    ('first', 'First'),
                    ('second', 'Second'),
                    ('third', 'Third'),
                ),
                accesses={'padawan': constants.EDITABLE}
            )
            first_field = fields.CharField(
                accesses={'padawan': constants.EDITABLE})
            second_field = fields.CharField(
                accesses={'padawan': constants.EDITABLE})
            third_field = fields.CharField(
                accesses={'padawan': constants.EDITABLE})
            another_field = fields.CharField(
                accesses={'padawan': constants.EDITABLE})

        form = MultipleChoiceForm.to_formidable(label='Drop Down Test Form')
        form.conditions = [
            {
                'name': 'Show first and second if value "first" selected',
                'action': 'display_iff',
                'fields_ids': ['first_field', 'second_field', ],
                'tests': [
                    {
                        'field_id': 'main_choices',
                        'operator': 'eq',
                        'values': ['first'],
                    }
                ]
            },
            {
                'name': 'Show third if value "second" selected',
                'action': 'display_iff',
                'fields_ids': ['third_field'],
                'tests': [
                    {
                        'field_id': 'main_choices',
                        'operator': 'eq',
                        'values': ['second'],
                    }
                ]
            }
        ]
        form.save()
        session = self.client.session
        session['role'] = 'padawan'
        session.save()
        res = self.client.post(
            reverse(url, args=[form.pk]),
            {"main_dropdown": "first", "third_field": "test"},
            format='json'
        )
        self.assertEqual(res.status_code, 204)

    def test_can_create_form_with_multiple_choices_via_api(self):
        conditions_schema = json.load(open(
            os.path.join(
                TESTS_DIR, 'fixtures', 'multiple-choices-conditions.json'
            )
        ))
        session = self.client.session
        session['role'] = 'padawan'
        session.save()
        res = self.client.post(
            reverse('formidable:form_create'),
            conditions_schema,
            format='json'
        )
        self.assertEqual(res.status_code, 201)
