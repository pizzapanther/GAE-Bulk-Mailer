import datetime

from django import http
from django.conf import settings
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

from ..shortcuts import render_tpl, ok
from ..auth import super_admin_required, staff_required

from .models import ApiKey, Campaign, generate_key
from .forms import ApiKeyForm
from ..tracking.models import Stats, Track

from google.appengine.api import taskqueue
from google.appengine.ext import ndb

@super_admin_required
def key_list (request):
  c = {
    'keys': ApiKey.query()
  }
  return render_tpl(request, 'api/key_list.html', c)
  
def key_add (request):
  return key_edit_view(request)
  
@super_admin_required
def key_edit_view (request, kid=None):
  instance = None
  verb = 'Add'
  form = ApiKeyForm(request.POST or None)
  
  if request.method == 'POST':
    if form.is_valid():
      akey = ApiKey(
        name=form.cleaned_data['name'],
        akey=generate_key(),
        created_by=request.user.user
      )
      akey.put()
      return http.HttpResponseRedirect('../')
      
  c = {
    'instance': instance,
    'verb': verb,
    'form': form,
  }
  c.update(csrf(request))
  
  return render_tpl(request, 'api/key_edit.html', c)
  
@csrf_exempt
@staff_required
def force_compile_stats (request):
  key = request.POST.get('key', '')
  cmpgn = ndb.Key(urlsafe=key).get()
  taskqueue.add(url='/api/compile-stats', params={'list_id': cmpgn.list_id, 'campaign_id': cmpgn.campaign_id}, queue_name='stats')
  return ok()
  
@csrf_exempt
def compile_stats (request):
  list_id = request.POST.get('list_id', '')
  campaign_id = request.POST.get('campaign_id', '')
  process = request.POST.get('process', '')
  key = request.POST.get('key', '')
  
  if list_id and campaign_id:
    if key:
      stat = ndb.Key(urlsafe=key).get()
      
    else:
      stat = Stats.query(Stats.list_id == list_id, Stats.campaign_id == campaign_id).get()
      if not stat:
        stat = Stats(list_id=list_id, campaign_id=campaign_id)
        
    if not process:
      process = 'opens'
      
    stat.process(process)
    stat.put()
    
    if process == 'opens':
      taskqueue.add(
        url='/api/compile-stats',
        params={
          'list_id': list_id,
          'campaign_id': campaign_id,
          'process': 'clicks',
          'key': stat.key.urlsafe()
        },
        queue_name='stats'
      )
      
  else:
    old = datetime.datetime.now() - datetime.timedelta(days=settings.COMPILE_STATS_PERIOD)
    for cmpgn in Campaign.query(Campaign.sent >= old).fetch():
      taskqueue.add(url='/api/compile-stats', params={'list_id': cmpgn.list_id, 'campaign_id': cmpgn.campaign_id}, queue_name='stats')
      
  return ok()
  
@staff_required
def campaign_stats (request, list_id, campaign_id):
  campaign = Campaign.query(Campaign.list_id == list_id, Campaign.campaign_id == campaign_id).get()
  if campaign:
    c = {
      'list_id': list_id,
      'campaign_id': campaign_id,
      'campaign': campaign,
    }
    return render_tpl(request, 'api/stats/campaign.html', c)
    
  raise http.Http404
  