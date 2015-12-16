from django.conf.urls import patterns, url

from formidable.views import FormidableDetail, FormidableUpdate

urlpatterns = patterns(
    r'',
    url(r'(?P<pk>\d+)/$', FormidableDetail.as_view(), name='form_detail'),
    url(r'create/$', FormidableUpdate.as_view(), name='form_create'),
)
