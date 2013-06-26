from django.conf import settings

from google.appengine.api import mail

from .base import BaseEmailer

class EMailer (BaseEmailer):
  def send (self, email, context):
    key = self.generate_key(email)
    context['key'] = key
    context['unsubscribe'] = self.unsubscribe_url(email, key)
    
    message = mail.EmailMessage(
      sender=settings.DEFAULT_FROM_EMAIL,
      subject=self.subject,
      to=email,
      reply_to=self.reply_to,
      body=self.render(self.text_tpl, context),
      headers=self.headers(context['unsubscribe']),
    )
    
    if self.html_tpl:
      message.html = self.render(self.html_tpl, context)
      
    message.send()
    