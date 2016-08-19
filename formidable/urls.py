from django.conf.urls import patterns, url

from formidable.views import (
    AccessList, ContextFormDetail, FormidableCreate, FormidableDetail,
    PresetsList, ValidateView
)

urlpatterns = patterns(
    r'',
    url(r'^forms/(?P<pk>\d+)/$', ContextFormDetail.as_view(),
        name='form_context'),
    url(r'^forms/(?P<pk>\d+)/validate/$', ValidateView.as_view(),
        name='form_validation'),
    url(r'^builder/forms/(?P<pk>\d+)/$', FormidableDetail.as_view(),
        name='form_detail'),
    url(r'^builder/forms/$', FormidableCreate.as_view(), name='form_create'),
    url(r'^builder/accesses/$', AccessList.as_view(), name='accesses_list'),
    url(r'^builder/presets', PresetsList.as_view(), name='presets_list'),
)
