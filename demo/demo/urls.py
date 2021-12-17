from django.urls import include, re_path
from django.contrib import admin

from demo.views import FormPreview, DemoValidateViewFromSchema


urlpatterns = [
    re_path(
        r'^api/',
        include(('formidable.urls', 'formidable'), namespace='formidable')),
    re_path(r'^api/forms/(?P<pk>\d+)/validate_schema/?$',
            DemoValidateViewFromSchema.as_view(),
            name='form_validation_schema'),
    re_path(r'^preview/(?P<pk>\d+)/', FormPreview.as_view()),
    re_path(r'^forms/',
            include(('demo.builder.urls', 'builder'), namespace='builder')),
    re_path(r'admin/', admin.site.urls, 'admin'),
]
