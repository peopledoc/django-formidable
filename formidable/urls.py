from django.conf.urls import url

from formidable import views

urlpatterns = [
    url(r'^forms/(?P<pk>\d+)/?$', views.ContextFormDetail.as_view(),
        name='context_form_detail'),
    url(r'^forms/(?P<pk>\d+)/validate/?$', views.ValidateView.as_view(),
        name='form_validation'),
    url(r'^builder/forms/(?P<pk>\d+)/?$', views.FormidableDetail.as_view(),
        name='form_detail'),
    url(r'^builder/forms/?$', views.FormidableCreate.as_view(),
        name='form_create'),
    url(r'^builder/accesses/?$', views.AccessList.as_view(),
        name='accesses_list'),
]
