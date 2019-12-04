import copy

from django.test import TestCase, override_settings
from django.urls import reverse
from django.conf import settings

from rest_framework.test import APITestCase

from formidable.models import Formidable
from formidable.serializers import FormidableSerializer
from formidable.security import get_clean_function

from . import form_data


XSS = """<IMG SRC=/ onerror="alert(String.fromCharCode(88,83,83))"></img>"""
XSS_RESULT = '<img src="/">'


class XSSLoaderTestCase(TestCase):

    @override_settings()
    def test_no_settings(self):
        # Deleting the settings
        del settings.DJANGO_FORMIDABLE_SANITIZE_FUNCTION

        clean_func = get_clean_function()
        assert clean_func(XSS) == XSS

    @override_settings(DJANGO_FORMIDABLE_SANITIZE_FUNCTION=None)
    def test_none_settings(self):
        clean_func = get_clean_function()
        assert clean_func(XSS) == XSS

    @override_settings(DJANGO_FORMIDABLE_SANITIZE_FUNCTION="foo.bar")
    def test_unimportable_settings(self):
        clean_func = get_clean_function()
        assert clean_func(XSS) == XSS

    @override_settings(
        DJANGO_FORMIDABLE_SANITIZE_FUNCTION="demo.security.clean_alert")
    def test_fake_cleaner_settings(self):
        clean_func = get_clean_function()
        assert clean_func(XSS) != XSS, clean_func(XSS)


class XSSViewsTestCase(APITestCase):

    def test_create_label_via_view(self):
        _form_data = copy.deepcopy(form_data)
        _form_data['label'] = XSS
        res = self.client.post(
            reverse('formidable:form_create'), _form_data, format='json'
        )
        self.assertEquals(res.status_code, 201)
        formidable = Formidable.objects.order_by('pk').last()
        assert formidable.label == XSS_RESULT

    def test_create_description_via_view(self):
        _form_data = copy.deepcopy(form_data)
        _form_data['description'] = XSS
        res = self.client.post(
            reverse('formidable:form_create'), _form_data, format='json'
        )
        self.assertEquals(res.status_code, 201)
        formidable = Formidable.objects.order_by('pk').last()
        assert formidable.description == XSS_RESULT

    def test_create_field_label_via_view(self):
        _form_data = copy.deepcopy(form_data)
        _form_data['fields'][0]['label'] = XSS
        res = self.client.post(
            reverse('formidable:form_create'), _form_data, format='json'
        )
        self.assertEquals(res.status_code, 201)
        formidable = Formidable.objects.order_by('pk').last()
        field = formidable.fields.first()
        assert field.label == XSS_RESULT

    def test_create_field_description_via_view(self):
        _form_data = copy.deepcopy(form_data)
        _form_data['fields'][0]['description'] = XSS
        res = self.client.post(
            reverse('formidable:form_create'), _form_data, format='json'
        )
        self.assertEquals(res.status_code, 201)
        formidable = Formidable.objects.order_by('pk').last()
        field = formidable.fields.first()
        # For historical reasons, help_text is mapped to description
        assert field.help_text == XSS_RESULT

    def test_create_field_defaults_via_view(self):
        _form_data = copy.deepcopy(form_data)
        _form_data['fields'][0]['defaults'] = [XSS]
        res = self.client.post(
            reverse('formidable:form_create'), _form_data, format='json'
        )
        self.assertEquals(res.status_code, 201)
        formidable = Formidable.objects.order_by('pk').last()
        field = formidable.fields.first()
        default = field.defaults.first()
        assert default.value == XSS_RESULT

    def test_create_field_placeholder_via_view(self):
        _form_data = copy.deepcopy(form_data)
        _form_data['fields'][0]['placeholder'] = XSS
        res = self.client.post(
            reverse('formidable:form_create'), _form_data, format='json'
        )
        self.assertEquals(res.status_code, 201)
        formidable = Formidable.objects.order_by('pk').last()
        field = formidable.fields.first()
        assert field.placeholder == XSS_RESULT


class XSSSerializerTestCase(TestCase):
    def test_create_label_via_serializer(self):
        _form_data = copy.deepcopy(form_data)
        _form_data['label'] = XSS

        serializer = FormidableSerializer(data=_form_data)
        serializer.is_valid()
        serializer.save()
        formidable = serializer.instance
        assert formidable.label == XSS_RESULT

    def test_create_description_via_serializer(self):
        _form_data = copy.deepcopy(form_data)
        _form_data['description'] = XSS

        serializer = FormidableSerializer(data=_form_data)
        serializer.is_valid()
        serializer.save()
        formidable = serializer.instance
        assert formidable.description == XSS_RESULT

    def test_create_field_label_via_serializer(self):
        _form_data = copy.deepcopy(form_data)
        _form_data['fields'][0]['label'] = XSS

        serializer = FormidableSerializer(data=_form_data)
        serializer.is_valid()
        serializer.save()
        formidable = serializer.instance
        field = formidable.fields.first()
        assert field.label == XSS_RESULT

    def test_create_field_description_via_serializer(self):
        _form_data = copy.deepcopy(form_data)
        _form_data['fields'][0]['description'] = XSS

        serializer = FormidableSerializer(data=_form_data)
        serializer.is_valid()
        serializer.save()
        formidable = serializer.instance
        field = formidable.fields.first()
        # For historical reasons, help_text is mapped to description
        assert field.help_text == XSS_RESULT

    def test_create_field_defaults_via_serializer(self):
        _form_data = copy.deepcopy(form_data)
        _form_data['fields'][0]['defaults'] = [XSS]

        serializer = FormidableSerializer(data=_form_data)
        serializer.is_valid()
        serializer.save()
        formidable = serializer.instance
        field = formidable.fields.first()
        default = field.defaults.first()
        assert default.value == XSS_RESULT

    def test_create_field_placeholder_via_serializer(self):
        _form_data = copy.deepcopy(form_data)
        _form_data['fields'][0]['placeholder'] = XSS

        serializer = FormidableSerializer(data=_form_data)
        serializer.is_valid()
        serializer.save()
        formidable = serializer.instance
        field = formidable.fields.first()
        assert field.placeholder == XSS_RESULT


class XSSInstructionFieldTestCase(APITestCase):
    """
    Tests for XSS on Instruction fields.

    The Instruction fields are an important attack vector, because they often
    carry HTML that has to be interpreted in the integration application.
    """
    def test_create_field_via_serializer(self):
        _form_data = copy.deepcopy(form_data)
        BASE_INSTRUCTIONS = "<p>Instructions to fill the form</p>\n"
        _form_data['fields'][0] = {
            "validations": [],
            "slug": "instructions",
            "description": BASE_INSTRUCTIONS + XSS,
            "placeholder": None,
            "type_id": "help_text",
            "defaults": [],
            "accesses": []
        }

        serializer = FormidableSerializer(data=_form_data)
        serializer.is_valid()
        serializer.save()
        formidable = serializer.instance
        field = formidable.fields.first()
        assert field.help_text == BASE_INSTRUCTIONS + XSS_RESULT

    def test_create_field_via_view(self):
        _form_data = copy.deepcopy(form_data)
        BASE_INSTRUCTIONS = "<p>Instructions to fill the form</p>\n"
        _form_data['fields'] = [{
            "validations": [],
            "slug": "instructions",
            "description": BASE_INSTRUCTIONS + XSS,
            "placeholder": None,
            "type_id": "help_text",
            "defaults": [],
            "accesses": []
        }]
        res = self.client.post(
            reverse('formidable:form_create'), _form_data, format='json'
        )
        self.assertEquals(res.status_code, 201)
        formidable = Formidable.objects.order_by('pk').last()
        field = formidable.fields.first()
        assert field.help_text == BASE_INSTRUCTIONS + XSS_RESULT
