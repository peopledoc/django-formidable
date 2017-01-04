import logging


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
    logger.info('Sucessfully recorded form :)')
    return True


def callback_fail_message(request):
    """
    This function will be called a form post-save/create.

    It adds a logging message (error)
    """
    logger.error('Form storing has failed :(')
    return True
