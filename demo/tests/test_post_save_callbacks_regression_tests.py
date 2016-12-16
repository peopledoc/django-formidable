# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from copy import deepcopy

from django.core.urlresolvers import reverse
from django.test import override_settings
from django.conf import settings

from rest_framework.test import APITestCase
from . import form_data, form_data_items


class CreateFormTestCase(APITestCase):

    @override_settings(FORMIDABLE_POST_CREATE_CALLBACK_SUCCESS=None)
    def test_create_no_error(self):
        res = self.client.post(
            reverse('formidable:form_create'), form_data, format='json'
        )
        self.assertEquals(res.status_code, 201)

    @override_settings(FORMIDABLE_POST_CREATE_CALLBACK_FAIL=None)
    def test_create_error(self):
        form_data_without_items = deepcopy(form_data_items)
        form_data_without_items['fields'][0].pop('items')

        res = self.client.post(
            reverse('formidable:form_create'), form_data_without_items,
            format='json'
        )
        self.assertEquals(res.status_code, 400)

    @override_settings()
    def test_create_no_settings_no_error(self):
        del settings.FORMIDABLE_POST_CREATE_CALLBACK_SUCCESS
        res = self.client.post(
            reverse('formidable:form_create'), form_data, format='json'
        )
        self.assertEquals(res.status_code, 201)

    @override_settings()
    def test_create_no_settings_error(self):
        del settings.FORMIDABLE_POST_CREATE_CALLBACK_FAIL
        form_data_without_items = deepcopy(form_data_items)
        form_data_without_items['fields'][0].pop('items')

        res = self.client.post(
            reverse('formidable:form_create'), form_data_without_items,
            format='json'
        )
        self.assertEquals(res.status_code, 400)
