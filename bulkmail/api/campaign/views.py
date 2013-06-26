import json
import datetime

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from google.appengine.api import taskqueue

from ...shortcuts import get_required, get_optional, ok
from ...auth import key_required
from ...exceptions import ApiException

from ..models import Campaign, generate_salt

@csrf_exempt
@key_required
def campaign_create (request):
  required = ('subject', 'reply_to', 'list_id', 'campaign_id', 'text')
  optional = ('html',)
  
  kwargs = get_required(request, required)
  kwargs.update(get_optional(request, optional))
  kwargs['salt'] = generate_salt(datetime.datetime.utcnow())
  
  if Campaign.query(Campaign.campaign_id == kwargs['campaign_id'], Campaign.list_id == kwargs['list_id']).count() > 0:
    raise ApiException('Campaign with list_id and campaign_id already created')
    
  cmpgn = Campaign(**kwargs)
  cmpgn.put()
  
  return ok()
  
@csrf_exempt
@key_required
def campaign_add_recipients (request):
  required = ('recipients', 'list_id', 'campaign_id')
  data = get_required(request, required)
  
  cmpgn = Campaign.query(Campaign.campaign_id == data['campaign_id'], Campaign.list_id == data['list_id']).get()
  if cmpgn:
    if cmpgn.sent:
      raise ApiException('Campaign sent already')
      
    json_data = json.loads(data['recipients'])
    if len(json_data) > settings.LIST_LIMIT:
      raise ApiException('Recipient list too large, limit is %d' % settings.LIST_LIMIT)
      
    cmpgn.send_data.append(json_data)
    cmpgn.put()
    
    return ok()
    
  raise ApiException('Unknown Campaign with list_id and campaign_id')
  
@csrf_exempt
@key_required
def campaign_send (request):
  required = ('list_id', 'campaign_id')
  data = get_required(request, required)
  cmpgn = Campaign.query(Campaign.campaign_id == data['campaign_id'], Campaign.list_id == data['list_id']).get()
  if cmpgn:
    if cmpgn.sent:
      raise ApiException('Campaign sent already')
      
    taskqueue.add(url='/mailer', params={'ckey': cmpgn.key.urlsafe()}, queue_name='mail')
    return ok()
    
  raise ApiException('Unknown Campaign with list_id and campaign_id')
  