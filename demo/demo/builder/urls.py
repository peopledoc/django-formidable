from django.conf.urls import patterns, url
from demo.builder.views import index

urlpatterns = patterns(
    r'',
    url(r'^$', index),
)