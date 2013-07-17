from django.conf.urls import patterns, include, url

urlpatterns = patterns('bulkmail.api.views',
  url(r'^apikey/add/$', 'key_add', name='key_add'),
  url(r'^apikey/$', 'key_list', name='key_list'),
  
  url(r'^stats/(\S+)/(\S+)/$', 'campaign_stats', name='campaign_stats'),
)

urlpatterns += patterns('bulkmail.api.campaign.views',
  url(r'^campaign/create/$', 'campaign_create', name='campaign_create'),
  url(r'^campaign/add_recipients/$', 'campaign_add_recipients', name='campaign_add_recipients'),
  url(r'^campaign/send/test/$', 'campaign_send_test', name='campaign_send_test'),
  url(r'^campaign/send/$', 'campaign_send', name='campaign_send'),
)
