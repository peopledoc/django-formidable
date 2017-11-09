import mock
import os

from django.test import TestCase

from formidable.json_migrations import migrate


@mock.patch('formidable.json_migrations.HERE',
            os.path.join(os.path.dirname(__file__), 'json_migrations'))
@mock.patch('formidable.json_migrations.package',
            'tests.json_migrations')
class JSONMigrationTestCase(TestCase):
    def _fixtures(self, version=None):
        data = {
            'fields': [
                {'foo': 'bar', 'help_text': 'SOS'},
                {'foo': 'baz', 'help_text': 'SAS'},
            ]
        }
        if version:
            data['version'] = version

        return data

    def test_migration_from_scratch(self):
        data = self._fixtures()
        updated_data = migrate(data)

        self.assertEqual(updated_data, {
            'version': 2,
            'fields': [
                {'foo': 'bar', 'description': 'SOS'},
                {'foo': 'baz', 'description': 'SAS'},
            ]
        })
        self.assertEqual(updated_data['version'], 2)

    def test_migration_from_version_1(self):
        data = self._fixtures(version=1)
        updated_data = migrate(data, 1)

        self.assertEqual(updated_data, {
            'version': 2,
            'fields': [
                {'foo': 'bar', 'help_text': 'SOS'},
                {'foo': 'baz', 'help_text': 'SAS'},
            ],
        })
        self.assertEqual(updated_data['version'], 2)

    def test_migration_from_version_2(self):
        data = self._fixtures(version=2)
        updated_data = migrate(data, 2)
        self.assertEqual(updated_data, data)

    @mock.patch('tests.json_migrations.0002_add_version.migrate')
    @mock.patch('tests.json_migrations.0001_rename_helptext.migrate')
    def test_migration_from_scratch_call_count(self, migrate_1, migrate_2):
        data = self._fixtures()
        migrate(data)
        self.assertEqual(migrate_1.call_count, 1)
        self.assertEqual(migrate_2.call_count, 1)

    @mock.patch('tests.json_migrations.0002_add_version.migrate')
    @mock.patch('tests.json_migrations.0001_rename_helptext.migrate')
    def test_migration_from_version_1_call_count(self, migrate_1, migrate_2):
        data = self._fixtures(version=1)
        migrate(data, 1)
        self.assertEqual(migrate_1.call_count, 0)
        self.assertEqual(migrate_2.call_count, 1)

    @mock.patch('tests.json_migrations.0002_add_version.migrate')
    @mock.patch('tests.json_migrations.0001_rename_helptext.migrate')
    def test_migration_from_version_2_call_count(self, migrate_1, migrate_2):
        data = self._fixtures(version=2)
        migrate(data, 2)
        self.assertEqual(migrate_1.call_count, 0)
        self.assertEqual(migrate_2.call_count, 0)
