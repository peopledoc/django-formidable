# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from copy import deepcopy
from django.core.urlresolvers import reverse
from django.test import override_settings

from rest_framework.test import APITestCase

from formidable.models import Formidable

from . import form_data, form_data_items

import six
if six.PY3:
    from unittest.mock import patch
else:
    from mock import patch

CALLBACK = 'demo.callback_save'
CALLBACK_EXCEPTION = 'demo.callback_exception'


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

    @override_settings(
        FORMIDABLE_POST_CREATE_CALLBACK_SUCCESS=CALLBACK_EXCEPTION
    )
    def test_create_exception(self):
        # The called function raises an error, but the treatment proceeds
        # as if nothing has happened
        res = self.client.post(
            reverse('formidable:form_create'), form_data, format='json'
        )
        self.assertEqual(res.status_code, 201)

    @override_settings(
        FORMIDABLE_POST_CREATE_CALLBACK_SUCCESS=CALLBACK_EXCEPTION
    )
    def test_create_exception_logger(self):
        # The called function raises an error, but the treatment proceeds
        # as if nothing has happened
        with patch('formidable.views.logger.error') as logger_error:
            res = self.client.post(
                reverse('formidable:form_create'), form_data, format='json'
            )
            self.assertEqual(res.status_code, 201)
            self.assertEqual(logger_error.call_count, 1)

    @override_settings(FORMIDABLE_POST_CREATE_CALLBACK_SUCCESS='non.existent')
    def test_create_callback_is_non_existent(self):
        # A non-existing module is treated separately.
        with patch('formidable.views.logger.error') as logger_error:
            res = self.client.post(
                reverse('formidable:form_create'), form_data, format='json'
            )
            self.assertEqual(res.status_code, 201)
            self.assertEqual(logger_error.call_count, 1)


class UpdateFormTestCase(APITestCase):

    def setUp(self):
        super(UpdateFormTestCase, self).setUp()
        self.form = Formidable.objects.create(
            label='test', description='test'
        )

    @override_settings(
        FORMIDABLE_POST_UPDATE_CALLBACK_SUCCESS=CALLBACK,
        FORMIDABLE_POST_UPDATE_CALLBACK_FAIL=CALLBACK
    )
    def test_do_no_call_on_get(self):
        with patch(CALLBACK) as patched_callback:
            res = self.client.get(
                reverse('formidable:form_detail', args=[self.form.id])
            )
            self.assertEqual(res.status_code, 200)
            # No call on GET
            self.assertEqual(patched_callback.call_count, 0)

    @override_settings(FORMIDABLE_POST_UPDATE_CALLBACK_SUCCESS=CALLBACK)
    def test_update_no_error_post(self):
        with patch(CALLBACK) as patched_callback:
            res = self.client.put(
                reverse('formidable:form_detail', args=[self.form.id]),
                form_data, format='json'
            )
            self.assertEqual(res.status_code, 200)
            self.assertEqual(patched_callback.call_count, 1)

    @override_settings(FORMIDABLE_POST_UPDATE_CALLBACK_FAIL=CALLBACK)
    def test_update_error_post(self):
        with patch(CALLBACK) as patched_callback:
            form_data_without_items = deepcopy(form_data_items)
            form_data_without_items['fields'][0].pop('items')

            res = self.client.put(
                reverse('formidable:form_detail', args=[self.form.id]),
                form_data_without_items, format='json'
            )
            self.assertEquals(res.status_code, 400)
            self.assertEqual(patched_callback.call_count, 1)

    @override_settings(
        FORMIDABLE_POST_UPDATE_CALLBACK_SUCCESS=CALLBACK_EXCEPTION
    )
    def test_update_exception(self):
        # The called function raises an error, but the treatment proceeds
        # as if nothing has happened
        res = self.client.put(
            reverse('formidable:form_detail', args=[self.form.id]),
            form_data, format='json'
        )
        self.assertEqual(res.status_code, 200)

    @override_settings(
        FORMIDABLE_POST_UPDATE_CALLBACK_SUCCESS=CALLBACK_EXCEPTION
    )
    def test_update_exception_logger(self):
        # The called function raises an error, but the treatment proceeds
        # as if nothing has happened
        with patch('formidable.views.logger.error') as logger_error:
            res = self.client.put(
                reverse('formidable:form_detail', args=[self.form.id]),
                form_data, format='json'
            )
            self.assertEqual(res.status_code, 200)
            self.assertEqual(logger_error.call_count, 1)

    @override_settings(FORMIDABLE_POST_UPDATE_CALLBACK_SUCCESS='non.existent')
    def test_update_callback_is_non_existent(self):
        # A non-existing module is treated separately.
        with patch('formidable.views.logger.error') as logger_error:
            res = self.client.put(
                reverse('formidable:form_detail', args=[self.form.id]),
                form_data, format='json'
            )
            self.assertEqual(res.status_code, 200)
            self.assertEqual(logger_error.call_count, 1)
