import datetime
import calendar
import logging
import operator

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
  tags = ndb.JsonProperty(compressed=True, required=False)
  
  opens = ndb.JsonProperty(compressed=True)
  clients = ndb.JsonProperty(compressed=True, required=False)
  urls = ndb.JsonProperty(compressed=True, required=False)
  
  created = ndb.DateTimeProperty(auto_now_add=True)
  last_compiled = ndb.DateTimeProperty(auto_now=True)
  
  def clients_sorted (self):
    return reversed(sorted(self.clients.iteritems(), key=operator.itemgetter(1)))
    
  def tags_sorted (self):
    return reversed(sorted(self.tags.iteritems(), key=operator.itemgetter(1)))
    
  def urls_sorted (self):
    return reversed(sorted(self.urls.iteritems(), key=operator.itemgetter(1)))
    
  def opens_pc (self, count):
    pc = (float(count) / self.total_opens) * 100
    return int(round(pc))
    
  def clicks_pc (self, count):
    pc = (float(count) / self.total_clicks) * 100
    return int(round(pc))
    
  def process_track (self, t, ptype):
    if t.created.minute % 10 >= 5:
      m = t.created.minute + (10 - (t.created.minute % 10))
      
    else:
      m = t.created.minute - (t.created.minute % 10)
      
    if m == 60:
      time = t.created.replace(minute=0, second=0, microsecond=0)
      time = time + datetime.timedelta(hours=1)
      
    else:
      time = t.created.replace(minute=m, second=0, microsecond=0)
      
    key = calendar.timegm(time.timetuple())
    
    if self.temp.has_key(key):
      self.temp[key] += 1
      
    else:
      self.temp[key] = 1
      
    if ptype == 'clicks':
      if t.tags:
        for tag in t.tags:
          if tag in self.tags:
            self.tags[tag] += 1
            
          else:
            self.tags[tag] = 1
            
      url = t.url.get().url
      if url in self.urls:
        self.urls[url] += 1
        
      else:
        self.urls[url] = 1
        
    elif ptype == 'opens':
      key = 'Other'
      if t.email_client:
        key = t.email_client
        
      elif t.browser_os:
        key = t.browser_os
        
      if key in self.clients:
        self.clients[key] += 1
        
      else:
        self.clients[key] = 1
        
  def sort_data (self, ptype):
    keys = self.temp.keys()
    keys.sort()
    perm = []
    
    for k in keys:
      perm.append((k, self.temp[k]))
      
    setattr(self, ptype, perm)
    
  def process (self, ptype):
    ttype = ptype[:-1]
    
    cursor = None
    total = 0
    
    self.temp = {}
    if ptype == 'clicks':
      self.tags = {}
      self.urls = {}
      
    if ptype == 'opens':
      self.clients = {}
      
    while 1:
      tracks, cursor, more = Track.query(
        Track.list_id == self.list_id,
        Track.campaign_id == self.campaign_id,
        Track.ttype == ttype,
      ).fetch_page(100, start_cursor=cursor)
      
      for t in tracks:
        self.process_track(t, ptype)
        total += 1
        
      if more and cursor:
        continue
        
      else:
        break
        
    setattr(self, 'total_' + ptype, total)
    self.sort_data(ptype)
    
WEB_CLIENTS = (
  ('google.com', 'GMail'),
  ('yahoo.com', 'Yahoo'),
  ('live.com', 'Outlook.com'),
)

EMAIL_CLIENTS = (
  ('Outlook', 'Outlook'),
)

class Track (ndb.Model):
  ttype = ndb.StringProperty() #open, click, image
  
  list_id = ndb.StringProperty()
  campaign_id = ndb.StringProperty()
  
  user_agent = ndb.StringProperty(required=False)
  referer = ndb.StringProperty(required=False)
  
  browser_os = ndb.StringProperty(required=False)
  browser_name = ndb.StringProperty(required=False)
  browser_version = ndb.IntegerProperty(required=False)
  email_client = ndb.StringProperty(required=False)
  
  email = ndb.StringProperty(required=False)
  url = ndb.KeyProperty(kind=Url, required=False)
  
  tags = ndb.StringProperty(repeated=True, required=False)
  
  created = ndb.DateTimeProperty(auto_now_add=True)
  
  def detect_browser (self):
    if self.user_agent:
      for client in EMAIL_CLIENTS:
        if client[0] in self.user_agent:
          self.email_client = client[1]
          break
          
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
            
    if self.referer:
      for client in WEB_CLIENTS:
        if client[0] in self.referer:
          self.email_client = client[1]
          break
          