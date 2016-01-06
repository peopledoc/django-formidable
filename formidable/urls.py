from django.conf.urls import patterns, url

from formidable.views import FormidableDetail, FormidableCreate, AccessList

urlpatterns = patterns(
    r'',
    url(r'^builder/forms/(?P<pk>\d+)/$', FormidableDetail.as_view(), name='form_detail'),
    url(r'^builder/forms/$', FormidableCreate.as_view(), name='form_create'),
    url(r'^builder/accesses/$', AccessList.as_view(), name='accesses_list')
)
