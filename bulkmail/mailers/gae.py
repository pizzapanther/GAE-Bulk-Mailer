from django.conf import settings

from google.appengine.api import mail

from .base import BaseEmailer

class EMailer (BaseEmailer):
  def send (self, email, context, log=True):
    if self.skip(email):
      return None
      
    key = self.generate_key(email)
    context['key'] = key
    context['unsubscribe'] = self.unsubscribe_url(email, key)
    
    message = mail.EmailMessage(
      sender=self.frm,
      subject=self.subject,
      to=email,
      reply_to=self.reply_to,
      body=self.render(self.text_tpl, context),
      headers=self.headers(context['unsubscribe']),
    )
    
    if self.html_tpl:
      message.html = self.render(self.html_tpl, context, True)
      
    message.send()
    
    if log:
      self.log_send(email)
      