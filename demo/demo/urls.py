from distutils.version import StrictVersion as version
import django
from django.conf.urls import include, url
from django.contrib import admin

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
]

if version(django.get_version()) < version("2.0"):
    urlpatterns += [
        url(r'^admin/', include(admin.site.urls)),
    ]
else:
    from django.urls import path  # noqa
    urlpatterns += [
        path(r'admin/', admin.site.urls, 'admin'),
    ]
