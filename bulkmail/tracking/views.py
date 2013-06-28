from django import http

from google.appengine.ext import ndb

from .models import Url

def url_redirect (request, key):
  try:
    url = ndb.Key(urlsafe=key).get()
    
  except:
    raise http.Http404
    
  if url:
    return http.HttpResponseRedirect(url.url)
    
  raise http.Http404
  