from django import http

from shortcuts import render_tpl

def home (request):
  content = render_tpl('home.html', {})
  return http.HttpResponse(content)
  