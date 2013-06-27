import hmac
import base64
import hashlib
import datetime
import urllib

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from google.appengine.api import urlfetch

from .base import BaseEmailer

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
    
    result = urlfetch.fetch(
      url='https://email.us-east-1.amazonaws.com/',
      payload=form_data,
      method=urlfetch.POST,
      headers=self.headers
    )
    
class EMailer (BaseEmailer):
  def __init__ (self, *args, **kwargs):
    super(EMailer, self).__init__(*args, **kwargs)
    self.connection = AmazonSES(settings.AWS_KEY_ID, settings.AWS_SECRET_KEY)
    
  def send (self, email, context):
    key = self.generate_key(email)
    context['key'] = key
    context['unsubscribe'] = self.unsubscribe_url(email, key)
    
    headers = self.headers(context['unsubscribe'])
    headers['Reply-To'] = self.reply_to
    
    msg = EmailMultiAlternatives(
      self.subject,
      self.render(self.text_tpl, context),
      settings.DEFAULT_FROM_EMAIL,
      [email]
    )
    
    if self.html_tpl:
      msg.attach_alternative(self.render(self.html_tpl, context, True), "text/html")
      
    self.connection.send(email, msg.message().as_string())
    