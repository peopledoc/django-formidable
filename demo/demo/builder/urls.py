# -*- coding: utf-8 -*-
from django.conf.urls import url
from demo.builder import views

urlpatterns = [
    r'',
    url(r'^$',
        views.FormidableListView.as_view(),
        name='formidable-list'),
    url(r'^(?P<pk>\d+)/(?P<role>[-_\w]+)/$',
        views.FormidableDetailView.as_view(),
        name='formidable-detail'),
    url(r'^edit/(?P<pk>\d+)$',
        views.FormidableUpdateView.as_view(),
        name='formidable-edit'),
    url(r'^builder/(?P<pk>\d+)$',
        views.FormidableBuilderView.as_view(),
        name='formidable-builder'),
]
