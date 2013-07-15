# bulkmailer.py Documentation

### Installation:
``pip install bulkmailer``

### Usage:
```python
import bulkmailer

...
BMAIL_HOST = 'your-app-id.appspot.com'
BMAIL_KEY = '...'
USE_SSL = True
bm = bulkmailer.Api(BMAIL_HOST, BMAIL_KEY, USE_SSL)
payload = {
  'subject': "E-Mail Subject",
  'from_name': "Mailer Dude",
  'reply_to': "no_reply@example.com",
  'list_id': "unique_list_id",
  'campaign_id': "unique_campaign_id",
  'html': html_template,
  'text': text_template,
}

# emails is a list of e-mails or a list of lists containing e-mails with context.
emails = ['narf@example.com', 'troz@example.com', 'frell@example.com']

# OR
emails = [
  ('narf@example.com', {'title': 'Mr', 'last_name': 'Narf'}),
  ('troz@example.com', {'title': 'Mrs', 'last_name': 'Troz'}),
  ('frell@example.com', {'title': 'Frell', 'last_name': 'Me'})
]
# Jinja2 is used to fill in your templates.  Context provided will be used with 
# your template.  See the API documentation for default context added to each template.

# Send a test
bm.campaign_send_test("unique_list_id", cmpgn_id, emails, payload)

#Normal Campaign
bm.campaign_create(payload)
bm.campaign_add_recipients("unique_list_id", "unique_campaign_id", emails)
bm.campaign_send("unique_list_id", "unique_campaign_id")
```
