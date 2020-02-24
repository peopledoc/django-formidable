import warnings

from distutils.version import StrictVersion as version

import django
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
            # Verify some things
            if version(django.get_version()) < version("2.0"):
                # Django 1.11 mainly
                assert len(w) == 1, w
                test_warning = w[0]
                assert issubclass(test_warning.category, ImportWarning)
                assert "jsonfield" in str(test_warning.message)
            else:
                # No warning beyond Django 2.
                assert len(w) == 0, w
