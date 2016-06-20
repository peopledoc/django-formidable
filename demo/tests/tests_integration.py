# -*- coding: utf-8 -*-
from copy import deepcopy

from django.core.urlresolvers import reverse

from freezegun import freeze_time
from rest_framework.test import APITestCase

from formidable.models import Formidable
from formidable.accesses import get_accesses
from formidable.forms import FormidableForm, fields
from formidable import validators

form_data = {
    "label": "test create",
    "description": "my first formidable by api",
    "fields": [
        {
            "label": "hello",
            "slug": "textslug",
            "type_id": "text",
            "placeholder": None,
            "help_text": None,
            "default": None,
            "accesses": [
                {"access_id": "padawan", "level": "REQUIRED"},
                {"access_id": "jedi", "level": "EDITABLE"},
                {"access_id": "jedi-master", "level": "READONLY"},
                {"access_id": "human", "level": "HIDDEN"},
            ]
        },
    ]
}

form_data_items = {
    "label": "test create",
    "description": "my first formidable by api",
    "fields": [{
        "label": "my_dropdwon",
        "slug": "dropdown_slug",
        "type_id": "dropdown",
        "placeholder": None,
        "help_text": "Lesfrites c'est bon",
        "default": None,
        "accesses": [
            {"access_id": "padawan", "level": "REQUIRED"},
            {"access_id": "jedi", "level": "EDITABLE"},
            {"access_id": "jedi-master", "level": "READONLY"},
            {"access_id": "human", "level": "HIDDEN"},
        ],
        "items": [
            {'value': 'tuto', 'label': 'toto'},
            {'value': 'plop', 'label': 'coin'},
        ],
        "multiple": False
    }]
}


class CreateFormTestCase(APITestCase):

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
        self.assertEquals(field.accesses.count(), 4)
        accesses = [
            ('padawan', 'REQUIRED'), ('jedi', 'EDITABLE'),
            ('jedi-master', 'READONLY'), ('human', 'HIDDEN'),
        ]
        for access, level in accesses:
            self.assertTrue(
                field.accesses.filter(access_id=access, level=level).exists()
            )

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
        self.assertEquals(res.status_code, 400)

    def test_with_unknown_accesses(self):
        form_data_copy = deepcopy(form_data)
        field = form_data_copy['fields'][0]
        field['accesses'][0]['access_id'] = 'NOT_A_LEVEL'
        res = self.client.post(
            reverse('formidable:form_create'), form_data_copy,
            format='json'
        )
        self.assertEquals(res.status_code, 400)


class UpdateFormTestCase(APITestCase):

    def setUp(self):
        super(UpdateFormTestCase, self).setUp()
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
        res = self.client.put(self.edit_url, data)
        self.assertEquals(res.status_code, 200)
        formidable = Formidable.objects.order_by('pk').last()
        self.assertEquals(formidable.pk, self.form.pk)
        self.assertEquals(formidable.label, 'edited label')
        self.assertEquals(formidable.description, 'edited description')
        self.assertEquals(Formidable.objects.count(), initial_count)

    def test_update_simple_fields(self):
        field = self.form.fields.create(
            type_id='text', slug='textslug', label=u'mytext',
            order=self.form.get_next_field_order()
        )
        for access in get_accesses():
            field.accesses.create(access_id=access.id, level='EDITABLE')
        res = self.client.put(self.edit_url, form_data,  format='json')
        self.assertEquals(res.status_code, 200)
        form = Formidable.objects.order_by('pk').last()
        self.assertEquals(form.pk, self.form.pk)
        self.assertEquals(form.fields.count(), 1)
        field = form.fields.first()
        self.assertEquals(field.label, 'hello')
        self.assertEquals(field.accesses.count(), 4)

    def test_create_field_on_update(self):
        field = self.form.fields.create(
            type_id='text', slug='textslug', label='mytext',
            order=self.form.get_next_field_order()
        )
        for access in get_accesses():
            field.accesses.create(access_id=access.id, level='EDITABLE')

        data = deepcopy(form_data)
        data['fields'].extend(form_data_items['fields'])
        res = self.client.put(self.edit_url, data,  format='json')
        self.assertEquals(res.status_code, 200)
        form = Formidable.objects.order_by('pk').last()
        self.assertEquals(form.pk, self.form.pk)
        self.assertEquals(form.fields.count(), 2)

    def test_delete_field_on_update(self):
        self.form.fields.create(
            type_id='text', slug='textslug', label=u'mytext',
            order=self.form.get_next_field_order()
        )
        self.form.fields.create(
            order=self.form.get_next_field_order(),
            type_id='text', slug='delete-slug', label='text'
        )

        for access in get_accesses():
            for field in self.form.fields.all():
                field.accesses.create(access_id=access.id, level=u'EDITABLE')

        res = self.client.put(self.edit_url, form_data,  format='json')
        self.assertEquals(res.status_code, 200)
        form = Formidable.objects.order_by('pk').last()
        self.assertEquals(form.pk, self.form.pk)
        self.assertEquals(form.fields.count(), 1)
        field = form.fields.first()
        self.assertEquals(field.label, u'hello')
        self.assertEquals(field.accesses.count(), 4)
        self.assertTrue(field.accesses.filter(
            access_id=u'padawan', level='REQUIRED'
        ).exists())
        self.assertTrue(field.accesses.filter(
            access_id=u'human', level='HIDDEN'
        ).exists())
        self.assertTrue(field.accesses.filter(
            access_id="jedi-master", level="READONLY"
        ).exists())


class TestAccess(APITestCase):

    def test_get(self):
        response = self.client.get(reverse('formidable:accesses_list'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 4)
        for access in response.data:
            self.assertIn('id', access)
            self.assertIn('label', access)
            self.assertIn(
                access['id'], [obj.id for obj in get_accesses()]
            )
            self.assertIn(
                access['label'], [obj.label for obj in get_accesses()]
            )


class TestChain(APITestCase):

    class MyTestForm(FormidableForm):

        name = fields.CharField(label='Name', accesses={'jedi': 'REQUIRED'})
        birth_date = fields.DateField(
            label='Your Birth Date', validators=[
                validators.AgeAboveValidator(
                    21, message='You cannot be a jedi until your 21'
                ),
                validators.DateIsInFuture(False)
            ],
            accesses={'jedi': 'REQUIRED'},
        )
        out_date = fields.DateField(validators=[
            validators.DateIsInFuture(True)
            ]
        )
        weapons = fields.ChoiceField(choices=[
            ('gun', 'blaster'), ('sword', 'light saber')
        ])
        salary = fields.IntegerField(validators=[
            validators.GTValidator(0), validators.LTEValidator(25)
            ], accesses={'jedi': 'HIDDEN', 'jedi-master': 'REQUIRED'}
        )

    def setUp(self):
        super(APITestCase, self).setUp()
        self.form = self.MyTestForm.to_formidable(label='Jedi Form')
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
