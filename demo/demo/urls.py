from django.conf.urls import include, url
from django.contrib import admin

from demo.views import FormPreview, DemoValidateViewFromSchema

urlpatterns = [
    url(r'^api/', include('formidable.urls', namespace='formidable')),
    url(r'^api/forms/(?P<pk>\d+)/validate_schema/?$',
        DemoValidateViewFromSchema.as_view(),
        name='form_validation_schema'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^preview/(?P<pk>\d+)/', FormPreview.as_view()),
    url(r'^forms/', include('demo.builder.urls', namespace='builder')),
]
