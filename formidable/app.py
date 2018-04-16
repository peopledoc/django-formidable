"""
Django-formidable app definition.

The :class:`FormidableConfig` checks various configuration settings:

* post-update and post-create callbacks
"""

import warnings
from distutils.version import StrictVersion

import django
from django.apps import AppConfig


class FormidableConfig(AppConfig):
    """
    Formidable application configuration class. Runs various checks.
    """
    name = 'formidable'

    def ready(self):
        """
        Run various checks when ready
        """
        from .views import check_callback_configuration
        check_callback_configuration()

        # Deprecation warning for django 1.8 and 1.9
        if StrictVersion(django.get_version()) < StrictVersion("1.10"):
            warnings.warn("Support for Django 1.8 and 1.9 is about to be "
                          "dropped. Please update to a newer version.",
                          DeprecationWarning)
