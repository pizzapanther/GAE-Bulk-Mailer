from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
  url(r'^api/', include('bulkmail.api.urls')),
  
  url(r'^analytics/', include('bulkmail.tracking.urls')),
  
  url(r'^unsubscribe/(\S+)/(\S+)/$', 'bulkmail.views.unsubscribe', name='unsubscribe'),
  url(r'^mailer$', 'bulkmail.views.mailer', name='mailer'),
  
  url(r'^_ah/bounce$', 'bulkmail.views.bouncer', name='bouncer'),
  url(r'^amazon-bounce.*$', 'bulkmail.views.amazon_bouncer', name='amazon_bouncer'),
  
  url(r'^$', 'bulkmail.views.home', name='home'),
)
