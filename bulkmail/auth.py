import logging

from django import http

from google.appengine.api import users

from .shortcuts import PermissionDenied
from .api.models import ApiKey

def super_admin_required (target):
  def wrapper (*args, **kwargs):
    request = args[0]
    if request.user.is_authorized():
      if request.user.is_super:
        response = target(*args, **kwargs)
        return response
        
      return PermissionDenied()
      
    return http.HttpResponseRedirect(users.create_login_url(request.build_absolute_uri()))
    
  return wrapper
  
def key_required (target):
  def wrapper (*args, **kwargs):
    request = args[0]
    akey = request.REQUEST.get('key', '')
    if akey:
      akey = ApiKey.query(ApiKey.akey == akey).get()
      if akey:
        logging.info('Using ApiKey: %s' % akey.name)
        response = target(*args, **kwargs)
        return response
        
    return PermissionDenied()
    
  return wrapper
  