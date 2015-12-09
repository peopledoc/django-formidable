from django.conf.urls import patterns, url

from formidable.views import FormidableDetail

urlpatterns = patterns(
    r'',
    url(r'(?P<pk>\d+)/$', FormidableDetail.as_view()),
)
