from django.conf.urls import patterns, include, url

urlpatterns = patterns('bulkmail.tracking.views',
  url(r'^open_pixel/(\S+)/(\S+).gif$', 'open_pixel', name='open_pixel'),
  url(r'^url/(\S+)$', 'url_redirect', name='url_redirect'),
)
