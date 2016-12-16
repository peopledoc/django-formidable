# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from copy import deepcopy
from mock import patch

from django.core.urlresolvers import reverse
from django.test import override_settings

from rest_framework.test import APITestCase
from . import form_data, form_data_items

CALLBACK = 'demo.callback_save'


class CreateFormTestCase(APITestCase):

    @override_settings(
        FORMIDABLE_POST_CREATE_CALLBACK_SUCCESS=CALLBACK,
        FORMIDABLE_POST_CREATE_CALLBACK_FAIL=CALLBACK
    )
    def test_do_no_call_on_get(self):
        with patch(CALLBACK) as patched_callback:
            res = self.client.get(
                reverse('formidable:form_create')
            )
            self.assertEqual(res.status_code, 405)
            # No call on GET
            self.assertEqual(patched_callback.call_count, 0)

    @override_settings(FORMIDABLE_POST_CREATE_CALLBACK_SUCCESS=CALLBACK)
    def test_create_no_error_post(self):
        with patch(CALLBACK) as patched_callback:
            res = self.client.post(
                reverse('formidable:form_create'), form_data, format='json'
            )
            self.assertEqual(res.status_code, 201)
            self.assertEqual(patched_callback.call_count, 1)

    @override_settings(FORMIDABLE_POST_CREATE_CALLBACK_FAIL=CALLBACK)
    def test_create_error_post(self):
        with patch(CALLBACK) as patched_callback:
            form_data_without_items = deepcopy(form_data_items)
            form_data_without_items['fields'][0].pop('items')

            res = self.client.post(
                reverse('formidable:form_create'), form_data_without_items,
                format='json'
            )
            self.assertEquals(res.status_code, 400)
            self.assertEqual(patched_callback.call_count, 1)
