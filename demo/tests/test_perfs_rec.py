# -*- coding: utf-8 -*-
import os
import json

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from django.conf import settings
from django_perf_rec import TestCaseMixin
from rest_framework.test import APITestCase


class TestCase(TestCaseMixin, APITestCase):
    """
    Add use perf rec mixin
    """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    yml_dir = 'perfs'

    def get_yml_dir_path(self):
        """
        Generate a path for the file
        """

        return os.path.join(self.dir_path, self.yml_dir, '')

    def record_performance(self, record_name, path=None):
        if path is None:
            path = self.get_yml_dir_path()

        if 'postgresql' in settings.DATABASES['default']['ENGINE']:
            record_name = '{}-pg'.format(record_name)

        return super(TestCase, self).record_performance(
            path=path,
            record_name=record_name
        )


class TestPerfRec(TestCase):
    """
    Log the queries to DB
    """

    fixtures_folder = 'fixtures'

    @classmethod
    def setUpClass(cls):
        super(TestPerfRec, cls).setUpClass()
        fixtures_path = os.path.join(cls.dir_path, cls.fixtures_folder)

        cls.form_data = json.load(
            open(os.path.join(fixtures_path, 'form-data.json'))
        )
        cls.form_data_changed = json.load(
            open(os.path.join(fixtures_path, 'form-data-changed.json'))
        )

    def test_access_list_perf_rec(self):
        with self.record_performance(record_name='TestPerfRec.accesses-list'):
            url = reverse('formidable:accesses_list')
            response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_context_form_details_perf_rec(self):
        form_id = self._create_form()

        url = reverse('formidable:context_form_detail', args=(form_id,))

        with self.record_performance(
                record_name='TestPerfRec.get-context-form'):
            response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_form_create_perf_rec(self):
        with self.record_performance(record_name='TestPerfRec.create-form'):
            self._create_form()
        # Status code is checked in :func:`_create_form()`

    def test_form_update_form_without_changes(self):
        form_id = self._create_form()

        with self.record_performance(
                record_name='TestPerfRec.update-form-without-changes'
        ):
            url = reverse('formidable:form_detail', args=(form_id, ))
            response = self.client.put(
                url, data=self.form_data,
                format='json'
            )
        self.assertEqual(response.status_code, 200)

    def test_form_update_with_changes(self):
        form_id = self._create_form()

        with self.record_performance(
                record_name='TestPerfRec.update-form-with-changes'
        ):
            url = reverse('formidable:form_detail', args=(form_id,))
            response = self.client.put(
                url, data=self.form_data_changed,
                format='json'
            )
        self.assertEqual(response.status_code, 200)

    def test_retrieve_form_perf_rec(self):
        form_id = self._create_form()

        with self.record_performance(record_name='TestPerfRec.retrieve-form'):
            url = reverse('formidable:form_detail', args=(form_id,))
            response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_form_validate_perf_rec(self):
        form_id = self._create_form()

        with self.record_performance(record_name='TestPerfRec.validate-form'):
            url = reverse('formidable:form_validation', args=(form_id,))
            response = self.client.post(url, format="json")
        # Empty response in the case it's valid.
        self.assertEqual(response.status_code, 204)

    def _create_form(self):
        session = self.client.session
        session['role'] = 'padawan'
        session.save()

        url = reverse('formidable:form_create')
        result = self.client.post(
            url, data=self.form_data, format="json"
        )
        self.assertEqual(result.status_code, 201)

        return result.data.get('id')
