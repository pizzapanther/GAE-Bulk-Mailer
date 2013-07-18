import datetime

from django import http
from django.conf import settings
from django.core.context_processors import csrf

from ..shortcuts import render_tpl, ok
from ..auth import super_admin_required

from .models import ApiKey, Campaign, generate_key
from .forms import ApiKeyForm
from ..tracking.models import Stats, Track

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
  
def compile_stats (request):
  old = datetime.datetime.now() - datetime.timedelta(days=settings.COMPILE_STATS_PERIOD)
  for cmpgn in Campaign.query(Campaign.sent >= old).fetch():
    stat = Stats.query(Stats.list_id == cmpgn.list_id, Stats.campaign_id == cmpgn.campaign_id).get()
    if not stat:
      stat = Stats(list_id=cmpgn.list_id, campaign_id=cmpgn.campaign_id)
      
    stat.process()
    stat.put()
    
  return ok()
  
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
  