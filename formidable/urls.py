from django.urls import re_path

from formidable import views

urlpatterns = [
    re_path(r'^forms/(?P<pk>\d+)/?$', views.ContextFormDetail.as_view(),
            name='context_form_detail'),
    re_path(r'^forms/(?P<pk>\d+)/validate/?$', views.ValidateView.as_view(),
            name='form_validation'),
    re_path(r'^builder/forms/(?P<pk>\d+)/?$', views.FormidableDetail.as_view(),
            name='form_detail'),
    re_path(r'^builder/forms/?$', views.FormidableCreate.as_view(),
            name='form_create'),
    re_path(r'^builder/accesses/?$', views.AccessList.as_view(),
            name='accesses_list'),
]
