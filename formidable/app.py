"""
Django-formidable app definition.

The :class:`FormidableConfig` checks various configuration settings:

* post-update and post-create callbacks
"""

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
