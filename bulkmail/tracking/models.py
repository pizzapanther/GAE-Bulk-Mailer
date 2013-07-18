import calendar
import logging

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
  
  total_clicks = ndb.IntegerProperty(default=0)
  total_opens = ndb.IntegerProperty(default=0)
  
  clicks = ndb.JsonProperty(compressed=True)
  opens = ndb.JsonProperty(compressed=True)
  
  created = ndb.DateTimeProperty(auto_now_add=True)
  
  def process_track (self, t):
    if t.created.minute % 10 >= 5:
      m = t.created.minute + (10 - (t.created.minute % 10))
      
    else:
      m = t.created.minute - (t.created.minute % 10)
      
    time = t.created.replace(minute=m, second=0, microsecond=0)
    key = calendar.timegm(time.timetuple()) * 1000
    data_dict = getattr(self, t.ttype + 's_temp')
    
    if data_dict.has_key(key):
      data_dict[key] += 1
      
    else:
      data_dict[key] = 1
      
  def sort_data (self, temp, perm):
    keys = temp.keys()
    keys.sort()
    for k in keys:
      perm.append((k, temp[k]))
      
  def process (self):
    cursor = None
    self.total_clicks = 0
    self.total_opens = 0
    self.clicks = []
    self.opens = []
    
    self.clicks_temp = {}
    self.opens_temp = {}
    
    while 1:
      tracks, cursor, more = Track.query(Track.list_id==self.list_id, Track.campaign_id==self.campaign_id).fetch_page(500, start_cursor=cursor)
      
      for t in tracks:
        if t.ttype in ('open', 'click'):
          self.process_track(t)
          
          if t.ttype == 'open':
            self.total_opens += 1
            
          if t.ttype == 'click':
            self.total_clicks += 1
            
      if more and cursor:
        continue
        
      else:
        break
        
    self.sort_data(self.clicks_temp, self.clicks)
    self.sort_data(self.opens_temp, self.opens)
    logging.info(self.opens)
    
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
            
            