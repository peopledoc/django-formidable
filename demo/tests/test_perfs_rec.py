# -*- coding: utf-8 -*-
import os
import json

from django.test import TestCase as OrigTestCase

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from django_perf_rec import TestCaseMixin


class TestCase(TestCaseMixin, OrigTestCase):
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

    def record_performance(self, record_name=None, path=None):
        if path is None:
            path = self.get_yml_dir_path()

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
        with self.record_performance(record_name='accesses-list'):
            url = reverse('formidable:accesses_list')
            self.client.get(url)

    def test_context_form_details_perf_rec(self):
        form_id = self._create_form()

        with self.record_performance(record_name='get-context-form'):
            url = reverse('formidable:context_form_detail', args=(form_id,))
            self.client.get(url)

    def test_form_create_perf_rec(self):
        with self.record_performance(record_name='create-form'):
            self._create_form()

    def test_form_update_form_without_changes(self):
        form_id = self._create_form()

        with self.record_performance(
                record_name='update-form-without-changes'
        ):
            url = reverse('formidable:form_detail', args=(form_id, ))
            self.client.put(
                url, data=json.dumps(self.form_data),
                content_type='application/json'
            )

    def test_form_update_with_changes(self):
        form_id = self._create_form()

        with self.record_performance(
                record_name='update-form-with-changes'
        ):
            url = reverse('formidable:form_detail', args=(form_id,))
            self.client.put(
                url, data=json.dumps(self.form_data_changed),
                content_type='application/json'
            )

    def test_retrieve_form_perf_rec(self):
        form_id = self._create_form()

        with self.record_performance(record_name='retrieve-form'):
            url = reverse('formidable:form_detail', args=(form_id,))
            self.client.get(url)

    def test_form_validate_perf_rec(self):
        form_id = self._create_form()

        with self.record_performance(record_name='validate-form'):
            url = reverse('formidable:form_validation', args=(form_id,))
            self.client.get(url)

    def _create_form(self):
        session = self.client.session
        session['role'] = 'padawan'
        session.save()

        url = reverse('formidable:form_create')
        result = self.client.post(
            url, data=self.form_data
        )

        return result.data.get('id')
