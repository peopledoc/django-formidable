from django.test import TestCase

from rest_framework.permissions import BasePermission, AllowAny

from formidable.views import FormidableDetail


class MyBasePermission(BasePermission):
    pass


class MyFormidableView(FormidableDetail):

    permission_classes = (MyBasePermission,)


class YaFormidableView(FormidableDetail):
    pass


class TestCustomView(TestCase):

    def test_custom_permission(self):
        self.assertIn(MyBasePermission, MyFormidableView.permission_classes)

    def test_default_permission(self):
        self.assertIn(AllowAny, YaFormidableView.permission_classes)
