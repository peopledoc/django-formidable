import logging

from django.contrib import messages

logger = logging.getLogger(__name__)


class DemoCallbackException(Exception):
    "A dummy callback exception"


def callback_save(*args, **kwargs):
    """
    This function will be called as a dummy callback on form post-save/create.

    It doesn't do much, and that's fine.
    """
    return True


def callback_exception(*args, **kwargs):
    """
    This function will be called-back on form post-save/create

    It'll raise an exception
    """
    raise DemoCallbackException()


def callback_success_message(request):
    """
    This function will be called a form post-save/create.

    It adds a logging message

    """
    msg = 'Sucessfully recorded form :)'
    logger.info(msg)
    messages.info(request._request, msg)


def callback_fail_message(request):
    """
    This function will be called a form post-save/create.

    It adds a logging message (error)
    """
    msg = 'Form storing has failed :('
    logger.error(msg)
    messages.error(request._request, msg)
