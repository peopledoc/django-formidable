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
            "default": None
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
        self.assertEqual(res.status_code, 400)


class TestAccess(APITestCase):

    def test_get(self):
        response = self.client.get(reverse('formidable:accesses_list'))
        self.assertEquals(response.status_code, 200)
        for access in response.data:
            self.assertIn('id', access)
            self.assertIn(access['id'], settings.FORMIDABLE_ACCESSES)
