import logging

from django.conf import settings
from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)


def get_clean_function(*args, **kwargs):

    def _no_clean(s):
        return s

    if not hasattr(settings, 'DJANGO_FORMIDABLE_SANITIZE_FUNCTION'):
        return _no_clean
    if not settings.DJANGO_FORMIDABLE_SANITIZE_FUNCTION:
        return _no_clean

    try:
        clean_function = import_string(
            settings.DJANGO_FORMIDABLE_SANITIZE_FUNCTION
        )
    except ImportError:
        logger.error("This application has no sanitization function. "
                     "There's a risk of XSS attack")
        clean_function = _no_clean

    return clean_function
