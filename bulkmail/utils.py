import time
import datetime
import logging

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
          
      logging.info('Stopped Rate Limit')
      ret = True
      
    now = datetime.datetime.now()
    if now - self.start >= datetime.timedelta(**self.interval):
      self.count = 0
      self.start = datetime.datetime.now()
      
    return ret
    