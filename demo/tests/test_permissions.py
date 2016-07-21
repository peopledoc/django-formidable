# -*- coding: utf-8 -*-
from django.conf import settings
from django.test import TestCase, override_settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from formidable.views import FormidableDetail, MetaClassView
from formidable.permissions import NoOne


class TestMetaClassPermissions(TestCase):
    """
    We only test ``MetaClassView`` (which is responsible for permission
    load) because permissions classes are generated while URL
    configuration is loaded)

    """

    @override_settings(
        FORMIDABLE_PERMISSION_BUILDER=[
            'rest_framework.permissions.IsAuthenticated'
        ]
    )
    def test_with_settings_key(self):
        attrs = {'settings_permission_key': 'FORMIDABLE_PERMISSION_BUILDER'}
        MyView = MetaClassView('MyView', (APIView,), attrs)
        permission_classes = MyView.permission_classes
        self.assertEqual(len(permission_classes), 1)
        self.assertEqual(permission_classes[0], IsAuthenticated)

    @override_settings(
        FORMIDABLE_DEFAULT_PERMISSION=[
            'rest_framework.permissions.AllowAny'
        ]
    )
    def test_settings_key_not_define(self):
        del settings.FORMIDABLE_PERMISSION_BUILDER

        attrs = {'settings_permission_key': 'FORMIDABLE_PERMISSION_BUILDER'}
        MyView = MetaClassView('MyView', (APIView,), attrs)
        permission_classes = MyView.permission_classes
        self.assertEqual(len(permission_classes), 1)
        self.assertEqual(permission_classes[0], AllowAny)

    def test_no_settings_key_define(self):
        del settings.FORMIDABLE_DEFAULT_PERMISSION

        attrs = {'settings_permission_key': 'FORMIDABLE_PERMISSION_BUILDER'}
        MyView = MetaClassView('MyView', (APIView,), attrs)
        permission_classes = MyView.permission_classes
        self.assertEqual(len(permission_classes), 1)
        self.assertEqual(permission_classes[0], NoOne)


class TestPermission(TestCase):

    def test_permissions_builder_loading(self):
        self.assertTrue(hasattr(FormidableDetail, 'permission_classes'))
        permission_classes = FormidableDetail.permission_classes
        self.assertEqual(len(permission_classes), 1)
        self.assertEqual(permission_classes[0], AllowAny)
