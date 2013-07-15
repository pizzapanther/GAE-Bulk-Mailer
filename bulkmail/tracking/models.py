
from google.appengine.ext import ndb

class Url (ndb.Model):
  url = ndb.StringProperty()
  list_id = ndb.StringProperty()
  campaign_id = ndb.StringProperty()
  
  tags = ndb.StringProperty(repeated=True)
  
  created = ndb.DateTimeProperty(auto_now_add=True)
  
class Track (ndb.Model):
  ttype = ndb.StringProperty() #open, click
  list_id = ndb.StringProperty()
  campaign_id = ndb.StringProperty()
  email = ndb.StringProperty()
  
  tags = ndb.StringProperty(repeated=True)
  
  created = ndb.DateTimeProperty(auto_now_add=True)
  