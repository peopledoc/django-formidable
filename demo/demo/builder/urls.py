# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from demo.builder.views import (
    FormidableListView, FormidableDetailView, FormidableBuilderView
)

urlpatterns = patterns(
    r'',
    url(r'^$', FormidableListView.as_view(), name='formidable-list'),
    url(r'^(?P<pk>\d+)/(?P<role>[-_\w]+)/$', FormidableDetailView.as_view(),
        name='formidable-detail'),
    url(r'^builder/(?P<pk>\d+)$', FormidableBuilderView.as_view(),
        name='formidable-builder'),
)
