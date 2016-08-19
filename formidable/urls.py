from django.conf.urls import patterns, url
from django.conf import settings

from rest_framework.settings import perform_import

from formidable.views import (
    AccessList, ContextFormDetail, FormidableCreate, FormidableDetail,
    PresetsList, ValidateView
)


def get_view_from_settings(settings, name, default):
    """
    Dynamically import the settings name if its define. Else return the default
    class base view
    """
    if hasattr(settings, name):
        class_view = perform_import(getattr(settings, name), name)
    else:
        class_view = default
    return class_view.as_view()


formidable_detail = get_view_from_settings(
    settings, 'FORMIDABLE_DETAIL_VIEW', FormidableDetail
)
formidable_create = get_view_from_settings(
    settings, 'FORMIDABLE_CREATE_VIEW', FormidableCreate
)
formidable_context = get_view_from_settings(
    settings, 'FORMIDABLE_CONTEXT_VIEW', ContextFormDetail
)
formidable_validate = get_view_from_settings(
    settings, 'FORMIDABLE_VALIDATE_VIEW', ValidateView
)

urlpatterns = patterns(
    r'',
    url(r'^forms/(?P<pk>\d+)/$', formidable_context,
        name='form_detail'),
    url(r'^forms/(?P<pk>\d+)/validate/$', formidable_validate,
        name='form_validation'),
    url(r'^builder/forms/(?P<pk>\d+)/$', formidable_detail,
        name='form_detail'),
    url(r'^builder/forms/$', formidable_create, name='form_create'),
    url(r'^builder/accesses/$', AccessList.as_view(), name='accesses_list'),
    url(r'^builder/presets', PresetsList.as_view(), name='presets_list'),
)
