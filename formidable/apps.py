from django.apps import AppConfig


class FormidableConfig(AppConfig):

    def ready(self):
        # Load every interpreter type
        from formidable.forms.validations.functions import Function  # noqa
        # Load every interpreter type
        from formidable.forms.validations.interpreter import *  # noqa
