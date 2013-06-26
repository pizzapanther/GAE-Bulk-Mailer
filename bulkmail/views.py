import re
import email
import logging
import datetime
import types
import importlib
import urllib
import json

from django import http
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from google.appengine.ext import ndb
from google.appengine.api import urlfetch

from .shortcuts import render_tpl, ok
from .api.models import Bounce, Campaign, Unsubscribe
from .mailers.base import emailer_key

imp = importlib.import_module(settings.EMAILER)
EMailer = imp.EMailer

def home (request):
  return render_tpl(request, 'home.html', {})
  
def unsubscribe (request, list_id, campaign_id):
  email = request.GET.get('email', '')
  key = request.GET.get('key', '')
  
  if email and key:
    cmpgn = Campaign.query(Campaign.list_id == list_id, Campaign.campaign_id == campaign_id).get()
    if cmpgn:
      if key == emailer_key(email, list_id, campaign_id, cmpgn.salt):
        if Unsubscribe.query(Unsubscribe.email == email.lower(), Unsubscribe.list_id == list_id, Unsubscribe.campaign_id == campaign_id).count() == 0:
          unsub = Unsubscribe(email=email.lower(), list_id=list_id, campaign_id=campaign_id)
          unsub.put()
          
        form_data = {'email': email, 'list_id': list_id, 'campaign_id': campaign_id}
        form_data.update(settings.REPORT_PAYLOAD)
        form_data = urllib.urlencode(form_data)
        result = urlfetch.fetch(url=settings.REPORT_UNSUBSCRIBE_URL, payload=form_data, method=urlfetch.POST, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        rdata = json.loads(result.content)
        return http.HttpResponseRedirect(rdata['url'])
        
  raise http.Http404
  
@csrf_exempt
def mailer (request):
  ckey = request.POST.get('ckey')
  cmpgn = ndb.Key(urlsafe=ckey).get()
  if cmpgn:
    cmpgn.sent = datetime.datetime.utcnow()
    cmpgn.put()
    emailer = EMailer(
      cmpgn.subject,
      cmpgn.reply_to,
      cmpgn.text,
      cmpgn.html,
      cmpgn.list_id,
      cmpgn.campaign_id,
      cmpgn.salt,
    )
    
    for elist in cmpgn.send_data:
      for edata in elist:
        if type(edata) == types.UnicodeType or type(edata) == types.StringType:
          email = edata
          context = {'request': request, 'email': edata}
          
        else:
          email = edata[0]
          context = {'request': request, 'email': edata[0]}
          context.update(edata[1])
          
        logging.info(email)
        
        emailer.send(email, context)
        
    cmpgn.finished = datetime.datetime.utcnow()
    cmpgn.put()
    
    return ok()
    
  raise Exception('Unknown Campaign')
  
@csrf_exempt
def bouncer (request):
  params = (
    'original-from',
    'original-to',
    'original-subject',
    'original-text',
    'notification-from',
    'notification-to',
    'notification-subject',
    'notification-text',
    'raw-message',
  )
  
  kwargs = {}
  for p in params:
    kwargs[p.replace('-', '_')] = request.POST.get(p, '')
    
  b = Bounce(**kwargs)
  b.put()
  
  msg = email.message_from_string(kwargs['raw_message'])
  
  found = re.search('<http\S+/unsubscribe/(\S+)/(\S+)/\?(\S+)>', msg['List-Unsubscribe'])
  if found:
    b.list_id = found.group(1)
    b.campaign_id = found.group(2)
    b.put()
    
    form_data = {'email': kwargs['original_to'], 'list_id': b.list_id, 'campaign_id': b.campaign_id}
    form_data.update(settings.REPORT_PAYLOAD)
    form_data = urllib.urlencode(form_data)
    result = urlfetch.fetch(url=settings.REPORT_BOUNCE_URL, payload=form_data, method=urlfetch.POST, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    logging.info('Bounce Report Status: ' + str(result.status_code))
    
  return ok()
  