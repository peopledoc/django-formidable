from django.conf.urls import patterns, url

from formidable.views import FormidableDetail, FormidableCreate

urlpatterns = patterns(
    r'',
    url(r'(?P<pk>\d+)/$', FormidableDetail.as_view(), name='form_detail'),
    url(r'create/$', FormidableCreate.as_view(), name='form_create'),
)
