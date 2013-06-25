from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
  url(r'^$', 'bulkmail.views.home', name='home'),
  # url(r'^bulkmail/', include('bulkmail.foo.urls')),
)
