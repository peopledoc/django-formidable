from django.urls import re_path
from demo.builder import views

urlpatterns = [
    re_path(r'^$',
            views.FormidableListView.as_view(),
            name='formidable-list'),
    re_path(r'^(?P<pk>\d+)/(?P<role>[-_\w]+)/$',
            views.FormidableDetailView.as_view(),
            name='formidable-detail'),
    re_path(r'^edit/(?P<pk>\d+)$',
            views.FormidableUpdateView.as_view(),
            name='formidable-edit'),
    re_path(r'^builder/(?P<pk>\d+)$',
            views.FormidableBuilderView.as_view(),
            name='formidable-builder'),
]
