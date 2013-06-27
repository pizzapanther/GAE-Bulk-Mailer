from django import http

from google.appengine.ext import ndb

from .models import Url

def url_redirect (request, key):
  url = ndb.Key(urlsafe=key).get()
  
  if url:
    return http.HttpResponseRedirect(url.url)
    
  raise http.Http404
  