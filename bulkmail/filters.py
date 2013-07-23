def shorten_url (url):
  url = url.replace('http://', '')
  url = url.replace('https://', '')
  
  return url
  