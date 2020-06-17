from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from demo.views import FormPreview, DemoValidateViewFromSchema

urlpatterns = [
    url(r'^api/',
        include(('formidable.urls', 'formidable'), namespace='formidable')),
    url(r'^api/forms/(?P<pk>\d+)/validate_schema/?$',
        DemoValidateViewFromSchema.as_view(),
        name='form_validation_schema'),
    url(r'^preview/(?P<pk>\d+)/', FormPreview.as_view()),
    url(r'^forms/',
        include(('demo.builder.urls', 'builder'), namespace='builder')),
    path(r'admin/', admin.site.urls, 'admin'),
]
