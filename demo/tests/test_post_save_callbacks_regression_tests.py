# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from copy import deepcopy

from django.core.urlresolvers import reverse
from django.test import override_settings
from django.conf import settings

from rest_framework.test import APITestCase

from formidable.models import Formidable

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
        self.assertEquals(res.status_code, 422)

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
        self.assertEquals(res.status_code, 422)


class UpdateFormTestCase(APITestCase):

    def setUp(self):
        super(UpdateFormTestCase, self).setUp()
        self.form = Formidable.objects.create(
            label='test', description='test'
        )

    @override_settings(FORMIDABLE_POST_UPDATE_CALLBACK_SUCCESS=None)
    def test_update_no_error(self):
        res = self.client.put(
            reverse('formidable:form_detail', args=[self.form.id]),
            form_data, format='json'
        )
        self.assertEquals(res.status_code, 200)

    @override_settings(FORMIDABLE_POST_UPDATE_CALLBACK_FAIL=None)
    def test_update_error(self):
        form_data_without_items = deepcopy(form_data_items)
        form_data_without_items['fields'][0].pop('items')

        res = self.client.put(
            reverse('formidable:form_detail', args=[self.form.id]),
            form_data_without_items, format='json'
        )
        self.assertEquals(res.status_code, 422)

    @override_settings()
    def test_update_no_settings_no_error(self):
        del settings.FORMIDABLE_POST_UPDATE_CALLBACK_SUCCESS
        res = self.client.put(
            reverse('formidable:form_detail', args=[self.form.id]),
            form_data, format='json'
        )
        self.assertEquals(res.status_code, 200)

    @override_settings()
    def test_update_no_settings_error(self):
        del settings.FORMIDABLE_POST_UPDATE_CALLBACK_FAIL
        form_data_without_items = deepcopy(form_data_items)
        form_data_without_items['fields'][0].pop('items')

        res = self.client.put(
            reverse('formidable:form_detail', args=[self.form.id]),
            form_data_without_items, format='json'
        )
        self.assertEquals(res.status_code, 422)


class UpdateFormWithTheSameFieldSlug(APITestCase):
    @override_settings(FORMIDABLE_POST_CREATE_CALLBACK_SUCCESS=None)
    def test_update_no_error(self):
        res_create = self.client.post(
            reverse('formidable:form_create'), form_data, format='json'
        )
        data = res_create.json()
        form_id = data.get('id')
        data_to_update = deepcopy(form_data_items)
        data_to_update['fields'][0]['slug'] = form_data['fields'][0]['slug']
        res_update = self.client.put(
            reverse('formidable:form_detail', args=[form_id]),
            data_to_update, format='json'
        )
        self.assertEquals(res_update.status_code, 200)
