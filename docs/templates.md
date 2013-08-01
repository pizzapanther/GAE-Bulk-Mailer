# Templating
Each campaign sent is processed through the template system so you can adjust your e-mails to cater for each
individual user.  The template system uses [Jinja2 Templates](http://jinja.pocoo.org/). When processing each e-mail
template context is created from the add recipients data and some default context.  Both the text and html versions of
an email are processed as Jinja2 Templates.

## Default Context
Each e-mail template processed will have the following context in addition to the context you provided when
adding recipients.

* **email:** E-Mail address of recipient
* **key:** Key used for tracking purposes
* **unsubscribe:** Unsubscribe URL

## Additional Processing
* To track e-mail opens, a tracking pixel is added to your body tag.
* All URLs for Links and Images are replaced with tracking URLs that will redirect to the original URL.
* If using 'analytics' with a campaign then the analytics string is added to all links.
* Links that have Bulkmailer tracking tags will be recorded and the Bulkmailer tracking tags will be removed off the URL.

## Best Practices
* Almost always use the unsubscribe url context to provide a link for unsubscribes.  About the only scenario where
you might not use it is for one off e-mails, such as, an invitation to join your list.
