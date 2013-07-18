import httpagentparser

from google.appengine.ext import ndb

class Url (ndb.Model):
  url = ndb.StringProperty()
  html_tag = ndb.StringProperty(default='a')
  
  list_id = ndb.StringProperty()
  campaign_id = ndb.StringProperty()
  
  tags = ndb.StringProperty(repeated=True, required=False)
  
  created = ndb.DateTimeProperty(auto_now_add=True)
  
class Stats (ndb.Model):
  list_id = ndb.StringProperty()
  campaign_id = ndb.StringProperty()
  
  created = ndb.DateTimeProperty(auto_now_add=True)
  
class Track (ndb.Model):
  ttype = ndb.StringProperty() #open, click, image
  
  list_id = ndb.StringProperty()
  campaign_id = ndb.StringProperty()
  
  user_agent = ndb.StringProperty(required=False)
  browser_os = ndb.StringProperty(required=False)
  browser_name = ndb.StringProperty(required=False)
  browser_version = ndb.IntegerProperty(required=False)
  
  email = ndb.StringProperty(required=False)
  url = ndb.KeyProperty(kind=Url, required=False)
  
  tags = ndb.StringProperty(repeated=True, required=False)
  
  created = ndb.DateTimeProperty(auto_now_add=True)
  
  def detect_browser (self):
    if self.user_agent:
      b = httpagentparser.detect(self.user_agent)
      if 'dist' in b and 'name' in b['dist']:
        self.browser_os = b['dist']['name']
        
      elif 'os' in b and 'name' in b['os']:
        self.browser_os = b['os']['name']
        
      if 'browser' in b:
        if 'name' in b['browser']:
          self.browser_name = b['browser']['name']
          
        if 'version' in b['browser']:
          try:
            self.browser_version = int(b['browser']['version'].split('.')[0])
            
          except:
            pass
            
            