from django.conf.urls import patterns, include, url

urlpatterns = patterns('bulkmail.tracking.views',
  url(r'^url/(\S+)$', 'url_redirect', name='url_redirect'),
)
