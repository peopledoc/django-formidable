"""
Django-formidable app definition.

The :class:`FormidableConfig` checks various configuration settings:

* post-update and post-create callbacks
"""
import warnings
from distutils.version import StrictVersion as version

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
        # Incompatibility between some version of jsonfield + Django.
        if version(django.get_version()) < version("2.0"):
            warnings.warn(
                "If you're using Django<2.0, you must pin jsonfield version in"
                " your requirements to ``jsonfield<3``. See deprecation"
                " documentation for more details",
                ImportWarning
            )
