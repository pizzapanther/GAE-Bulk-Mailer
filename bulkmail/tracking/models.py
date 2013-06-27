
from google.appengine.ext import ndb

class Url (ndb.Model):
  url = ndb.StringProperty()
  list_id = ndb.StringProperty()
  campaign_id = ndb.StringProperty()
  created = ndb.DateTimeProperty(auto_now_add=True)
  