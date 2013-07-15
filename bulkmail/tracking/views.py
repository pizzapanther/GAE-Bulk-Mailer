from django import http

from google.appengine.ext import ndb

from .models import Url, Track
from ..mailers.base import emailer_key
from ..api.models import Campaign

TRANSPARENT_1_PIXEL_GIF = "\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"

def verify_email (target):
  def wrapper (*args, **kwargs):
    request = args[0]
    if len(args) == 3:
      list_id = args[1]
      campaign_id = args[2]
      
    else:
      try:
        obj = ndb.Key(urlsafe=args[1]).get()
      except:
        raise http.Http404
        
      if obj:
        list_id = obj.list_id
        campaign_id = obj.campaign_id
        
      else:
        raise http.Http404
        
    email = request.GET.get('email', '')
    key = request.GET.get('key', '')
    
    if email and key:
      cmpgn = Campaign.query(Campaign.list_id==list_id, Campaign.campaign_id==campaign_id).get()
      if cmpgn:
        if key == emailer_key(email, cmpgn.list_id, cmpgn.campaign_id, cmpgn.salt):
          if len(args) == 3:
            kwargs['email'] = email
            return target(*args, **kwargs)
            
          else:
            return target(request, obj, email, **kwargs)
            
    raise http.Http404
    
  return wrapper
  
@verify_email
def open_pixel (request, list_id, campaign_id, email=None):
  t = Track(ttype='open', list_id=list_id, campaign_id=campaign_id, email=email.lower())
  t.put()
  
  return http.HttpResponse(TRANSPARENT_1_PIXEL_GIF, content_type='image/gif')
  
@verify_email
def url_redirect (request, url, email):
  t = Track(ttype='click', list_id=url.list_id, campaign_id=url.campaign_id, email=email.lower())
  t.put()
  
  return http.HttpResponseRedirect(url.url)
  