import re
import urllib
import hashlib
import logging

from django.conf import settings
from django.core.urlresolvers import reverse

from jinja2 import Template
from bs4 import BeautifulSoup

from ..tracking.models import Url
from ..api.models import SendLog

def emailer_key (*args):
  text = ':'.join(args)
  return hashlib.sha224(text).hexdigest()
  
class BaseEmailer (object):
  def __init__ (self, subject, reply_to, text_tpl, html_tpl, list_id, campaign_id, from_name, salt):
    self.subject = subject
    self.reply_to = reply_to
    self.text_tpl = text_tpl
    self.html_tpl = html_tpl
    self.list_id = list_id
    self.campaign_id = campaign_id
    self.salt = salt
    
    self.urls = {}
    
    self.frm = settings.DEFAULT_FROM_EMAIL
    if from_name:
      self.frm = '%s <%s>' % (from_name, settings.DEFAULT_FROM_EMAIL)
      
    self.url_regex = re.compile(r"""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>\[\]]+|\(([^\s()<>\[\]]+|(\([^\s()<>\[\]]+\)))*\))+(?:\(([^\s()<>\[\]]+|(\([^\s()<>\[\]]+\)))*\)|[^\s`!(){};:'".,<>?\[\]]))""")
    
  def render (self, tpl, context, html=False):
    template = Template(tpl)
    text = template.render(**context)
    if html:
      soup = BeautifulSoup(text)
      soupers = {
        'a': 'href',
        'img': 'src',
      }
      
      for tag, attr in soupers.items():
        for link in soup.find_all(tag):
          href = link.get(attr)
          if href and href.startswith(('http://', 'https://')):
            if not href.startswith(settings.BASE_URL):
              if href in self.urls:
                link[attr] = self.urls[href]
                
              else:
                url = Url(url=href, list_id=self.list_id, campaign_id=self.campaign_id)
                url.put()
                new_url = '%s%s' % (settings.BASE_URL, reverse('url_redirect', args=(url.key.urlsafe(),)))
                self.urls[href] = new_url
                link[attr] = new_url
                
      text = unicode(soup)
      
    else:
      text = self.url_regex.sub(self.process_match, text)
      
    return text
    
  def process_match(self,  m):
    href = m.group(0)
    if href and href.startswith(('http://', 'https://')):
      if not href.startswith(settings.BASE_URL):
        if href in self.urls:
          return self.urls[href]
          
        else:
          url = Url(url=href, list_id=self.list_id, campaign_id=self.campaign_id)
          url.put()
          new_url = '%s%s' % (settings.BASE_URL, reverse('url_redirect', args=(url.key.urlsafe(),)))
          self.urls[href] = new_url
          
          return new_url
          
    return href
    
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
    
  def send (self, email, context, log=True):
    raise NotImplementedError
    
  def skip (self, email):
    if SendLog.query(
        SendLog.email == email,
        SendLog.campaign_id == self.campaign_id,
        SendLog.list_id == self.list_id
      ).count() > 0:
      logging.info('Skipping already sent: %s, Campaign: %s, List: %s' % (email, self.campaign_id, self.list_id))
      return True
      
    return False
    
  def log_send (self, email):
    sl = SendLog(email=email, campaign_id=self.campaign_id, list_id=self.list_id)
    sl.put()
    
  def close (self):
    pass
  