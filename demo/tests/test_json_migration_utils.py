import os
import json
from django.test import TestCase

from formidable.json_migrations.utils import merge_context_forms

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))


class JSONMigrationUtilsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.expected_form = json.load(open(
            os.path.join(
                TESTS_DIR, 'fixtures', 'migration-form-data-expected.json'
            )
        ))
        cls.base_form = json.load(open(
            os.path.join(
                TESTS_DIR,
                'fixtures',
                'migration-form-data-input.json'
            )
        ))

    def get_base_form(self, version=None):
        form = self.base_form.copy()
        if version is not None:
            form['version'] = version
        return form

    def get_expected_form(self, version=None):
        form = self.expected_form.copy()
        if version is not None:
            form['version'] = version
        return form

    def test_merge_context_forms_without_version(self):
        base_form = self.get_base_form()
        expected_form = self.get_expected_form()
        expected_form['fields'][0]['accesses'].sort(key=self.dict_sort_key)

        result = merge_context_forms(base_form)
        result['fields'][0]['accesses'].sort(key=self.dict_sort_key)

        self.assertDictEqual(expected_form, result)

    def test_merge_context_forms_with_version(self):
        version = 2
        base_form = self.get_base_form(version=version)
        expected_form = self.get_expected_form(version=version)
        expected_form['fields'][0]['accesses'].sort(key=self.dict_sort_key)

        result = merge_context_forms(base_form)
        result['fields'][0]['accesses'].sort(key=self.dict_sort_key)

        self.assertDictEqual(expected_form, result)

    def dict_sort_key(self, obj):
        return obj['access_id']
