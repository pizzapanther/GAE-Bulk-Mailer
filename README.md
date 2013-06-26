GAE-Bulk-Mailer
===============

Bulk e-mail service for Google App Engine

Current bulk e-mail services like MailChimp, Campaign Monitor, etc in general 
provide the following services: List Management, Sending E-Mail, Analytics, etc.
Then there are lower level services like Mandrill or Amazon SES which provide
just the sending e-mail service and bounce back notifications.  While the higher
level services are great, they often catered for smaller businesses.  Thus, if 
out you grow them you are stuck with you using lower level services that do not 
provide the reporting and tracking you might need.

GAE Bulk Mailer was written so you can integrate lower level transactional 
services, but still have a mechanism to track your e-mails.  This gives you more
control while also giving you some tools to help build your e-mail service.  
GAE Bulk Mailer provides the following:

  1. Sending API so you can switch e-mail sending providers.
  2. Template API when sending.
  3. Tracking and reporting: tracks opens, links, unsubscribes, mail client, etc.

## Why App Engine?

Tracking can be a very write heavy operation so having a service that can scale
automatically as you grow and can scale back down when your traffic dies down is
desired. App Engine provides this without having to worry about server 
maintenance and deployment.

### GAE Bulk Mailer is brought to you by:

Lead Developer: Paul Bailey: [Twitter](https://twitter.com/pizzapanther) - [GitHub](https://github.com/pizzapanther) - [G+](https://plus.google.com/111994399408696258069)

Initial development funded by: [CultureMap.com](http://houston.culturemap.com/)
