from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
  url(r'^api/', include('bulkmail.api.urls')),
  
  url(r'^$', 'bulkmail.views.home', name='home'),
)
