import urllib
import hashlib

from django.conf import settings
from django.core.urlresolvers import reverse

from jinja2 import Template
from bs4 import BeautifulSoup

from ..tracking.models import Url

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
    
    self.urls = {}
    
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
      
    return text
    
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
  