from .shortcuts import render_tpl

def home (request):
  return render_tpl(request, 'home.html', {})
  