import mock
import os
from copy import deepcopy

from django.test import TestCase

from formidable.json_migrations import migrate


@mock.patch('formidable.json_migrations.HERE',
            os.path.join(os.path.dirname(__file__), 'json_migrations'))
@mock.patch('formidable.json_migrations.package',
            'tests.json_migrations')
class JSONMigrationTestCase(TestCase):
    def setUp(self):
        super(JSONMigrationTestCase, self).setUp()

        self.data = deepcopy({
            'fields': [
                {'foo': 'bar', 'help_text': 'SOS'},
                {'foo': 'baz', 'help_text': 'SAS'},
            ]
        })

    def test_migration_from_scratch(self):
        updated_data, version = migrate(self.data)

        self.assertEqual(updated_data, {
            'version': 2,
            'fields': [
                {'foo': 'bar', 'description': 'SOS'},
                {'foo': 'baz', 'description': 'SAS'},
            ]
        })
        self.assertEqual(version, 2)

    def test_migration_from_version_1(self):
        updated_data, version = migrate(self.data, 1)

        self.assertEqual(updated_data, {
            'version': 2,
            'fields': [
                {'foo': 'bar', 'help_text': 'SOS'},
                {'foo': 'baz', 'help_text': 'SAS'},
            ],
        })
        self.assertEqual(version, 2)

    def test_migration_from_version_2(self):
        updated_data, version = migrate(self.data, 2)
        self.assertEqual(updated_data, self.data)
        self.assertEqual(version, 2)

    @mock.patch('tests.json_migrations.0002_add_version.migrate')
    @mock.patch('tests.json_migrations.0001_rename_helptext.migrate')
    def test_migration_from_scratch_call_count(self, migrate_1, migrate_2):
        migrate(self.data)
        self.assertEqual(migrate_1.call_count, 1)
        self.assertEqual(migrate_2.call_count, 1)

    @mock.patch('tests.json_migrations.0002_add_version.migrate')
    @mock.patch('tests.json_migrations.0001_rename_helptext.migrate')
    def test_migration_from_version_1_call_count(self, migrate_1, migrate_2):
        migrate(self.data, 1)
        self.assertEqual(migrate_1.call_count, 0)
        self.assertEqual(migrate_2.call_count, 1)

    @mock.patch('tests.json_migrations.0002_add_version.migrate')
    @mock.patch('tests.json_migrations.0001_rename_helptext.migrate')
    def test_migration_from_version_2_call_count(self, migrate_1, migrate_2):
        migrate(self.data, 2)
        self.assertEqual(migrate_1.call_count, 0)
        self.assertEqual(migrate_2.call_count, 0)
