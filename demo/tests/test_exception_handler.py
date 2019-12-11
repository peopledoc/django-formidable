from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django import forms
from django.http import Http404

from rest_framework.test import APITestCase
from rest_framework import exceptions

from formidable.models import Formidable

from unittest.mock import patch


INIT_TO_MOCK = 'formidable.serializers.forms.FormidableSerializer.__init__'


class ExceptionHandlingTest(APITestCase):
    def setUp(self):
        super().setUp()
        self.form = Formidable.objects.create(
            label='test', description='test'
        )

    @property
    def url(self):
        # We've chosen this view, but it could've been any other.
        return reverse(
            'formidable:form_detail', args=[self.form.id]
        )

    @patch('formidable.exception_handler.logger')
    def test_unknown_exception(self, mock_logger):
        exception = Exception("Unknown exception here!")

        def error_raiser(*args, **kwargs):
            raise exception

        with patch(INIT_TO_MOCK, error_raiser):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 500)
        mock_logger.exception.assert_called_with(
            "Unexpected Formidable Error: %s", 'A server error occurred.',
            exc_info=exception)

    def test_exceptions_validation_error(self):
        def error_raiser(*args, **kwargs):
            raise exceptions.ValidationError("exceptions.ValidationError")
        with patch(INIT_TO_MOCK, error_raiser):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 422)

    def test_exceptions_api_exception(self):
        class CustomException(exceptions.APIException):
            status_code = 418

        def error_raiser(*args, **kwargs):
            raise CustomException("exceptions.APIException")

        with patch(INIT_TO_MOCK, error_raiser):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 418)

    def test_http404(self):
        def error_raiser(*args, **kwargs):
            raise Http404("404")

        with patch(INIT_TO_MOCK, error_raiser):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_permissiondenied(self):
        def error_raiser(*args, **kwargs):
            raise PermissionDenied("PermissionDenied")

        with patch(INIT_TO_MOCK, error_raiser):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_forms_validationerror(self):
        def error_raiser(*args, **kwargs):
            raise forms.ValidationError("forms.ValidationError")

        with patch(INIT_TO_MOCK, error_raiser):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 422)
