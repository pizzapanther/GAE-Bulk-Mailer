from django import http
from django.conf import settings

from google.appengine.api import users

from .exceptions import ParameterRequired, ApiException

class User (object):
  def __init__ (self):
    self._email = None
    self._is_super = None
    self._is_auth = None
    self._userid = None
    
    self.user = None
    
  def is_authorized (self):
    if self._is_auth is None:
      user = users.get_current_user()
      if user:
        self.user = user
        self._email = self.user.email()
        self._userid = self.user.user_id()
        self._is_super = False
        self._is_auth = True
        self._is_staff = False
        
        if self._email.lower() in settings.SUPER_ADMINS:
          self._is_super = True
          self._is_staff = True
          
        elif self._email.lower() in settings.STAFF_USERS:
          self._is_staff = True
          
        else:
          for d in settings.STAFF_DOMAINS:
            if self._email.lower().endswith(d):
              self._is_staff = True
              break
              
      else:
        self._is_auth = False
        
    return self._is_auth
    
  @property
  def email (self):
    if self._is_auth is None:
      self.is_authorized()
      
    return self._email
    
  @property
  def is_super (self):
    if self._is_auth is None:
      self.is_authorized()
      
    return self._is_super
    
  @property
  def is_staff (self):
    if self._is_auth is None:
      self.is_authorized()
      
    return self._is_staff
    
  @property
  def userid (self):
    if self._is_auth is None:
      self.is_authorized()
      
    return self._userid
    
class Session (object):
  def process_request (self, request):
    request.user = User()
    
    return None
    
class ApiExceptions (object):
  def process_exception (self, request, exception):
    if isinstance(exception, ParameterRequired) or isinstance(exception, ApiException):
      return http.HttpResponseServerError(exception.message, mimetype="text/plain")
      
    return None
    