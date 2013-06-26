import base64
import random
import hashlib

from google.appengine.ext import ndb

class ApiKey (ndb.Model):
  name = ndb.StringProperty(required=True)
  akey = ndb.StringProperty(required=True)
  created = ndb.DateTimeProperty(auto_now_add=True)
  created_by = ndb.UserProperty(required=True)
  
def generate_key ():
  while 1:
    akey = base64.b64encode(hashlib.sha512( str(random.getrandbits(256)) ).digest(), random.choice(['rA','aZ','gQ','hH','hG','aR','DD'])).rstrip('==')
    if ApiKey.query(ApiKey.akey == akey).count() == 0:
      break
    
  return akey
  
class Campaign (ndb.Model):
  subject = ndb.StringProperty(required=True)
  reply_to = ndb.StringProperty(required=True)
  
  html = ndb.TextProperty(required=False)
  text = ndb.TextProperty(required=True)
  
  list_id = ndb.StringProperty(required=True)
  campaign_id = ndb.StringProperty(required=True)
  
  created = ndb.DateTimeProperty(auto_now_add=True)
  
  sent = ndb.DateTimeProperty(required=False)
  send = ndb.DateTimeProperty(required=False)
  
  send_data = ndb.JsonProperty(repeated=True, compressed=True)
  