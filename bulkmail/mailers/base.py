import urllib
import hashlib

from django.conf import settings
from django.core.urlresolvers import reverse

from jinja2 import Template

def emailer_key (*args):
  text = ':'.join(args)
  return hashlib.sha224(text).hexdigest()
  
class BaseEmailer (object):
  def __init__ (self, subject, reply_to, text_tpl, html_tpl, list_id, campaign_id, salt):
    self.subject = subject
    self.reply_to = reply_to
    self.text_tpl = text_tpl
    self.html_tpl = html_tpl
    self.list_id = list_id
    self.campaign_id = campaign_id
    self.salt = salt
    
  def render (self, tpl, context):
    template = Template(tpl)
    return template.render(**context)
    
  def generate_key (self, email):
    return emailer_key(email, self.list_id, self.campaign_id, self.salt)
    
  def unsubscribe_url (self, email, key):
    url = settings.BASE_URL + reverse('unsubscribe', args=(self.list_id, self.campaign_id))
    url += '?key=%s&email=%s' % (urllib.quote(key), urllib.quote(email))
    return url
    
  def headers (self, unsubscribe):
    h = {
      'List-Id': self.list_id,
      'List-Unsubscribe': '<%s>' % unsubscribe,
    }
    return h
    
  def send (self, email, context):
    raise NotImplementedError
    
  def close (self):
    pass
  