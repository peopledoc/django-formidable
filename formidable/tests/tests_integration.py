# -*- coding: utf-8 -*-
from copy import deepcopy

from django.core.urlresolvers import reverse
from django.conf import settings

from rest_framework.test import APITestCase

from formidable.models import Formidable

form_data = {
    "label": "test create",
    "description": "my first formidable by api",
    "fields": [
        {
            "label": "hello",
            "slug": "textslug",
            "type_id": "text",
            "placeholder": None,
            "helptext": None,
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
        "helptext": "Lesfrites c'est bon",
        "default": None,
        "accesses": [
            {"access_id": "padawan", "level": "REQUIRED"},
            {"access_id": "jedi", "level": "EDITABLE"},
            {"access_id": "jedi-master", "level": "READONLY"},
            {"access_id": "human", "level": "HIDDEN"},
        ],
        "items": {
            "plop": "coin",
            "tuto": "toto"
        },
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
            label=u'test', description='test'
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
        self.assertEquals(formidable.label, u'edited label')
        self.assertEquals(formidable.description, u'edited description')
        self.assertEquals(Formidable.objects.count(), initial_count)

    def test_update_simple_fields(self):
        field = self.form.fields.create(
            type_id='text', slug='textslug', label=u'mytext',
        )
        for access in settings.FORMIDABLE_ACCESSES:
            field.accesses.create(access_id=access, level=u'EDITABLE')
        res = self.client.put(self.edit_url, form_data,  format='json')
        self.assertEquals(res.status_code, 200)
        form = Formidable.objects.order_by('pk').last()
        self.assertEquals(form.pk, self.form.pk)
        self.assertEquals(form.fields.count(), 1)
        field = form.fields.first()
        self.assertEquals(field.label, u'hello')
        self.assertEquals(field.accesses.count(), 4)

    def test_create_field_on_update(self):
        field = self.form.fields.create(
            type_id='text', slug='textslug', label=u'mytext',
        )
        for access in settings.FORMIDABLE_ACCESSES:
            field.accesses.create(access_id=access, level=u'EDITABLE')

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
        )
        self.form.fields.create(
            type_id='text', slug='delete-slug', label='text'
        )

        for access in settings.FORMIDABLE_ACCESSES:
            for field in self.form.fields.all():
                field.accesses.create(access_id=access, level=u'EDITABLE')

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
            self.assertIn(access['id'], settings.FORMIDABLE_ACCESSES)
