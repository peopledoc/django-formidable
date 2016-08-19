# -*- coding: utf-8 -*-
import sys
from imp import reload
from importlib import import_module

from django.conf import settings
from django.core.urlresolvers import (
    get_resolver, get_urlconf, reverse, set_urlconf
)

from django.test import TestCase, override_settings

from formidable.views import (
    FormidableCreate, FormidableDetail, ValidateView
)


def reload_urlconf(urlconf=None, urls_attr='urlpatterns'):
    if urlconf is None:
        urlconf = settings.ROOT_URLCONF
        if urlconf in sys.modules:
            reload(sys.modules[urlconf])
    reloaded = import_module(urlconf)
    reloaded_urls = getattr(reloaded, urls_attr)
    set_urlconf(tuple(reloaded_urls))


class MyDetailView(FormidableDetail):

    permissions_classes = ('rest_framework.permissions.AllowAny',)


class MyCreateView(FormidableCreate):
    pass


class MyValidateView(ValidateView):
    pass


class CustomViewTestCase(TestCase):

    @override_settings(FORMIDABLE_DETAIL_VIEW=MyDetailView)
    def test_custom_detail_view(self):
        resolver = get_resolver(get_urlconf())
        match = resolver.resolve(reverse('formidable:form_detail', args=[1]))
        self.assertEqual(MyDetailView.as_view().__name__, match.func.__name__)

    @override_settings(FORMIDABLE_CREATE_VIEW=MyCreateView)
    def test_custom_create_view(self):
        resolver = get_resolver(get_urlconf())
        match = resolver.resolve(reverse('formidable:form_create'))
        self.assertEqual(MyCreateView.as_view().__name__, match.func.__name__)

    @override_settings(FORMIDABLE_VALIDATE_VIEW=MyValidateView)
    def test_custom_validate_view(self):
        resolver = get_resolver(get_urlconf())
        match = resolver.resolve(reverse('formidable:form_validation',
                                         args=[1]))
        self.assertEqual(MyValidateView.as_view().__name__, match.func.__name__)
