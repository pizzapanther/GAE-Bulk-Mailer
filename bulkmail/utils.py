import time
import datetime
import logging

def cached_method (target):
  def wrapper(*args, **kwargs):
    obj = args[0]
    name = '_' + target.__name__
    
    if not hasattr(obj, name):
      value = target(*args, **kwargs)
      setattr(obj, name, value)
      
    return getattr(obj, name)
    
  return wrapper
  
class RateLimit (object):
  def __init__ (self, rate, interval):
    self.interval = {interval: 1}
    self.rate = rate
    self.count = 0
    self.start = datetime.datetime.now()
    
  def limit (self):
    if self.rate == 0:
      return False
      
    ret = False
    self.count += 1
    
    if self.count >= self.rate:
      logging.info('Started Rate Limit: %d' % self.count)
      while 1:
        time.sleep(.1)
        now = datetime.datetime.now()
        if now - self.start >= datetime.timedelta(**self.interval):
          break
          
      ret = True
      
    now = datetime.datetime.now()
    if now - self.start >= datetime.timedelta(**self.interval):
      self.count = 0
      self.start = datetime.datetime.now()
      
    return ret
    