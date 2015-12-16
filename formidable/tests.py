# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from formidable.models import Formidable

form_data = {
    "label": "test create",
    "description": "my first formidable by api",
    "fields": [
        {
            "label": "hello",
            "type_id": "text",
            "placeholder": None,
            "helptext": None,
            "default": None
        },
    ]
}

"""
        {
            "label": "my_dropdwon",
            "type_id": "dropdown",
            "placeholder": None,
            "helptext": "Lesfrites c'est bon",
            "default": None,
            "items": {
                "plop": "coin",
                "tuto": "toto"
            },
            "multiple": False
        }
"""


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
