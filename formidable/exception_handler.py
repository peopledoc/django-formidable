# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django import forms
from django.core.exceptions import NON_FIELD_ERRORS, PermissionDenied
from django.forms.utils import ErrorDict, ErrorList
from django.http import Http404

import six
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.settings import api_settings

logger = logging.getLogger(__name__)


def _reformat_drf_errors(errors, detail, path=None):
    if path is None:
        path = []
    if isinstance(detail, dict):
        for k, v in detail.items():
            if k == api_settings.NON_FIELD_ERRORS_KEY:
                new_path = path
            else:
                new_path = path + [k]
            _reformat_drf_errors(errors, v, new_path)
    elif isinstance(detail, list):
        for idx, v in enumerate(detail):
            if v:
                _reformat_drf_errors(errors, v, path + ['{}'.format(idx)])
    else:
        # errors are always coerced to a list so we
        # can skip the last level in our path
        path.pop()
        message = six.text_type(detail)
        error = {
            'message': message,
            'code': getattr(detail, 'code', 'invalid') or 'invalid',
        }
        # do not put a field attribute on global validaiton errors
        if path:
            error['field'] = '.'.join(path)
        errors.append(error)


def format_validation_error(detail):
    errors = []
    _reformat_drf_errors(errors, detail)
    return {
        'code': 'validation_error',
        'message': 'Validation failed',
        'errors': errors,
    }


def _reformat_forms_errors(errors, error, path=None):
    if path is None:
        path = []
    if isinstance(error, ErrorDict):
        for k, v in error.items():
            if k == NON_FIELD_ERRORS:
                new_path = path
            else:
                new_path = path + [k]
            _reformat_forms_errors(errors, v, new_path)
    elif isinstance(error, ErrorList):
        for item in error.as_data():
            _reformat_forms_errors(errors, item, path)
    elif isinstance(error, list):
        for item in error:
            _reformat_forms_errors(errors, item, path)
    else:
        # django.core.exceptions.Exception
        item = {
            'message': six.text_type(error.message),
            'code': error.code or 'invalid',
        }
        if path:
            item['field'] = '.'.join(path)
        errors.append(item)


def format_forms_error(error):
    errors = []
    _reformat_forms_errors(errors, error)
    return {
        'code': 'validation_error',
        'message': 'Validation failed',
        'errors': errors,
    }


def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    headers = None
    if isinstance(exc, exceptions.ValidationError):
        data = format_validation_error(exc.detail)
        # change default 400 status code from DRF to Unprocessable Entity
        status_code = 422
        # status_code = exc.status_code
    elif isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        data = {
            'code': getattr(exc.detail, 'code', 'error'),
            'message': six.text_type(exc.detail),
        }
        status_code = exc.status_code
    elif isinstance(exc, Http404):
        data = {
            'code': 'not_found',
            'message': six.text_type(exceptions.NotFound.default_detail),
        }
        status_code = 404
    elif isinstance(exc, PermissionDenied):
        data = {
            'code': 'permission_denied',
            'message': six.text_type(
                exceptions.PermissionDenied.default_detail),
        }
        status_code = 403
    elif isinstance(exc, forms.ValidationError):
        data = format_forms_error(exc.error_list)
        status_code = 422
    else:
        # unhandled exception, return generic error
        error_message = six.text_type(exceptions.APIException.default_detail)
        data = {
            'code': 'error',
            'message': error_message,
        }
        logger.error("Unexpected Formidable Error: %s", error_message)
        status_code = 500

    return Response(data, status=status_code, headers=headers)


class ExceptionHandlerMixin(object):
    """
    this mixin replaces the exception handler from the APIView

    Warning: must be set *after* `CallbackMixin`.
    """

    def handle_exception(self, exc):
        """
        Handle any exception that occurs, by returning an appropriate response,
        or re-raising the error.
        """
        if isinstance(exc, (exceptions.NotAuthenticated,
                            exceptions.AuthenticationFailed)):
            # WWW-Authenticate header for 401 responses, else coerce to 403
            auth_header = self.get_authenticate_header(self.request)

            if auth_header:
                exc.auth_header = auth_header
            else:
                exc.status_code = 403

        context = self.get_exception_handler_context()
        response = exception_handler(exc, context)

        if response is None:
            raise

        response.exception = True
        return response
