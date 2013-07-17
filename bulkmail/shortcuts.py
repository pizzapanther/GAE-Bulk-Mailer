import json

from django import http
from django.conf import settings

from .exceptions import ParameterRequired

def static_url (path):
  return settings.BASE_URL + settings.STATIC_URL + path
  
def render_tpl (request, tpl, context):
  template = settings.TPL_ENV.get_template(tpl)
  context['request'] = request
  context['static'] = static_url
  context['DEBUG'] = settings.DEBUG
  
  content = template.render(**context)
  return http.HttpResponse(content)
  
def PermissionDenied (message='Permission Denied: You do not have access to this area.'):
  return http.HttpResponseForbidden(message, mimetype='text/plain')
  
def get_required (request, required):
  kwargs = {}
  for r in required:
    value = request.POST.get(r, '')
    if value:
      kwargs[r] = value
      
    else:
      raise ParameterRequired(r)
      
  return kwargs
  
def get_optional (request, required):
  kwargs = {}
  for r in required:
    value = request.POST.get(r, '')
    if value:
      kwargs[r] = value
      
  return kwargs
  
def json_response (context):
  json_dump = json.dumps(context)
  return http.HttpResponse(json_dump, mimetype='application/json')
  
def ok ():
  return http.HttpResponse('OK', mimetype='text/plain')
  