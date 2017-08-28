import warnings


default_app_config = 'formidable.app.FormidableConfig'
version = '1.0.0.dev0'

# TO BE REMOVED ON 1.0.0
with warnings.catch_warnings():
    warnings.simplefilter('always', DeprecationWarning)
    page = 'https://django-formidable.readthedocs.io/en/latest/deprecations.html'  # noqa
    warnings.warn(
        'Form Presets are about to be deprecated. '
        'Please refer to the Deprecation Timeline document for more details '
        '{}.'.format(page),
        DeprecationWarning)
    warnings.warn(
        'Support for Django Rest Framework v3.3 is about to be deprecated. '
        'Please refer to the Deprecation Timeline document for more details '
        '{}.'.format(page),
        DeprecationWarning
    )
