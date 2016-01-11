# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from demo.builder.views import FormidableListView, FormidableDetailView

urlpatterns = patterns(
    r'',
    url(r'^$', FormidableListView.as_view(), name='formidable-list'),
    url(r'^(?P<pk>\d+)$', FormidableDetailView.as_view(), name='formidable-detail'),
)
