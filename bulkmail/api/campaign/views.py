import json
import types
import datetime
import logging
import importlib

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from google.appengine.api import taskqueue

from ...shortcuts import get_required, get_optional, ok
from ...auth import key_required
from ...exceptions import ApiException

from ..models import Campaign, SendData, generate_salt

imp = importlib.import_module(settings.EMAILER)
EMailer = imp.EMailer

@csrf_exempt
@key_required
def campaign_create (request):
  required = ('subject', 'reply_to', 'list_id', 'campaign_id', 'text')
  optional = ('html', 'from_name', 'analytics')
  
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
      
    sd = SendData(data=json_data)
    sd.put()
    
    cmpgn.send_data.append(sd.key)
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
      
    cmpgn.sent = datetime.datetime.utcnow()
    cmpgn.put()
    for i in range(0, len(cmpgn.send_data)):
      taskqueue.add(url='/mailer', params={'ckey': cmpgn.key.urlsafe(), 'i': i}, queue_name='mail')
      
    return ok()
    
  raise ApiException('Unknown Campaign with list_id and campaign_id')
  
@csrf_exempt
@key_required
def campaign_send_test (request):
  required = ('subject', 'reply_to', 'list_id', 'campaign_id', 'text', 'test_emails')
  optional = ('html', 'from_name', 'analytics')
  
  kwargs = get_required(request, required)
  kwargs.update(get_optional(request, optional))
  kwargs['salt'] = generate_salt(datetime.datetime.utcnow())
  
  emails = json.loads(kwargs['test_emails'])
  del kwargs['test_emails']
  kwargs['campaign_id'] = kwargs['campaign_id'] + '-test'
  kwargs['list_id'] = kwargs['list_id'] + '-test'
  
  cmpgn = Campaign.query(Campaign.campaign_id == kwargs['campaign_id'], Campaign.list_id == kwargs['list_id']).get()
  if cmpgn:
    for r in required:
      if kwargs.has_key(r):
        setattr(cmpgn, r, kwargs[r])
        
    for r in optional:
      if kwargs.has_key(r):
        setattr(cmpgn, r, kwargs[r])
        
    cmpgn.put()
    
  else:
    cmpgn = Campaign(**kwargs)
    cmpgn.put()
    
  emailer = EMailer(
    cmpgn.subject,
    cmpgn.reply_to,
    cmpgn.text,
    cmpgn.html,
    cmpgn.list_id,
    cmpgn.campaign_id,
    cmpgn.from_name,
    cmpgn.salt,
    None
  )
  
  for edata in emails:
    if type(edata) == types.UnicodeType or type(edata) == types.StringType:
      email = edata
      context = {'request': request, 'email': edata}
      
    else:
      email = edata[0]
      context = {'request': request, 'email': edata[0]}
      context.update(edata[1])
      
    try:
      emailer.send(email, context, log=False)
      
    except:
      logging.error('Send Error: ' + email)
      logging.error(traceback.format_exc())
      
  return ok()
  