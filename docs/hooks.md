# Web Hooks
Actions such as an unsubscribe, bounce, or complaint are recieved by the Bulk Mailer and then communicated 
to you so that you can clean up your list.  The following hooks should be implemented before using the Bulk Mailer
service.

All hooks are called with the parameters from settings.REPORT_PAYLOAD.  If you need to implement an API key 
for the callback, this is where you can put it.

## Unsubscribe Hook

**Setting**: REPORT_UNSUBSCRIBE_URL - _URL to report unsubscribes to_

**Parameters Sent in POST Request:**
* email: E-Mail of user who unsubscribed
* list_id: List ID to remove user from
* campaign_id: Campaign ID on which unsubscribed took place

## Bounce/Complaint Hook

**Setting**: REPORT_BOUNCE_URL - _URL to report bounces and complaints to_

**Parameters Sent in Google Mailer POST Request:**
* email: E-Mail of user who unsubscribed
* list_id: List ID to remove user from
* campaign_id: Campaign ID on which unsubscribed took place
* bounce: Bounce type (for Google 'bounce')

**Parameters Sent in Amazon Mailer POST Request:**
* email: E-Mail of user who unsubscribed
* bounce: Bounce type ('bounce' or 'complaint')
