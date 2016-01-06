from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    # Examples:
    # url(r'^$', 'demo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/', include('formidable.urls', namespace='formidable')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('demo.builder.urls', namespace='builder')),
]
