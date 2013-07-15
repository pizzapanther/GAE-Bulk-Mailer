import hmac
import base64
import hashlib
import datetime
import urllib
import logging
import traceback
import json
import time

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from google.appengine.api import urlfetch
from google.appengine.api import taskqueue

from .base import BaseEmailer

def amazon_send (**kwargs):
  count = 0
  email = kwargs['email']
  del kwargs['email']
  
  while 1:
    count += 1
    
    try:
      result = urlfetch.fetch(**kwargs)
      
    except:
      logging.error('Send Error: ' + email)
      logging.error('Try: %d' % count)
      logging.error(traceback.format_exc())
      
    else:
      if result.status_code == 200:
        break
        
      else:
        logging.error('Send Error: ' + email)
        logging.error('Try: %d' % count)
        logging.error('Status Code: %d' % result.status_code)
        
    if count >= 3:
      logging.error(kwargs)
      raise Exception("Send Failed")
      
    time.sleep(2)
    
class AmazonSES (object):
  def __init__ (self, access_id, access_key):
    self.access_id = access_id
    self.access_key = access_key
    
    self.headers = { 'Content-type': 'application/x-www-form-urlencoded' }
    
    d = datetime.datetime.utcnow()
    dateValue = d.strftime('%a, %d %b %Y %H:%M:%S GMT')
    self.headers['Date'] = dateValue
    signature = self.signature(dateValue)
    
    self.headers['X-Amzn-Authorization'] = 'AWS3-HTTPS AWSAccessKeyId=%s, Algorithm=HMACSHA256, Signature=%s' % (access_id, signature)
    
  def signature (self, dateValue):
    h = hmac.new(key=self.access_key, msg=dateValue, digestmod=hashlib.sha256)
    return base64.b64encode(h.digest()).decode()
    
  def send (self, email, raw_message):
    form_data = {
      'Action': 'SendRawEmail',
      'Destinations.member.1': email,
      'RawMessage.Data': base64.b64encode(raw_message),
    }
    form_data = urllib.urlencode(form_data)
    
    kwargs = {
      'email': email,
      'url': 'https://email.us-east-1.amazonaws.com/',
      'payload': form_data,
      'method': urlfetch.POST,
      'headers': self.headers,
      'deadline': 60,
    }
    
    taskqueue.add(url='/amazon/send', params={'data': json.dumps(kwargs)}, queue_name='amazon')
    
class EMailer (BaseEmailer):
  def __init__ (self, *args, **kwargs):
    super(EMailer, self).__init__(*args, **kwargs)
    self.connection = AmazonSES(settings.AWS_KEY_ID, settings.AWS_SECRET_KEY)
    
  def send (self, email, context, log=True):
    if self.skip(email):
      return None
      
    key = self.generate_key(email)
    context['key'] = key
    context['unsubscribe'] = self.unsubscribe_url(email, key)
    
    headers = self.headers(context['unsubscribe'])
    headers['Reply-To'] = self.reply_to
    
    msg = EmailMultiAlternatives(
      self.subject,
      self.render(self.text_tpl, context),
      self.frm,
      [email],
      headers=headers
    )
    
    if self.html_tpl:
      msg.attach_alternative(self.render(self.html_tpl, context, True), "text/html")
      
    self.connection.send(email, msg.message().as_string())
    
    if log:
      self.log_send(email)
      
  def close (self):
    #self.connection.close()
    pass
  