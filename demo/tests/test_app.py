import warnings

from django.apps import apps
from django.test import TestCase


class FormidableConfigTest(TestCase):
    def test_apps(self):
        config = apps.get_app_config('formidable')
        self.assertEqual(config.name, 'formidable')
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # Trigger a warning.
            config.ready()
            # Verify there's no warning.
            assert len(w) == 0, w
