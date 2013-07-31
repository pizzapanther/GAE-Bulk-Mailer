# API Documentation

## General Requirements
Every request requires an API key and a set of required parameters encoded via a standard HTTP POST request.
You can create an API Key by visiting /api/apikey/ on your GAE Bulk Mail instance (admin privileges required).
The API key should be sent as a parameter named "key" with every request.

<hr>
### /api/campaign/create/
Creates a campaign to send.

**Required Parameters:**
* **subject:** subject of e-mail
* **reply_to:** reply to e-mail address
* **list_id:** List ID, unique url safe string to identify list
* **campaign_id:** Campaign ID, unique url safe string to identify campaign
* **text:** text template for body of e-mail

**Optional Parameters:**
* **html:** html template for body of e-mail
* **from_name:** Display name for from address
* **analytics:** Anayltics string added to each URL for services such as Google Anayltics.  Example: ``utm_source=monthlyMailt&utm_medium=email&utm_campaign=campaign1``

**Response:**
HTTP Response 200
<hr>
### /api/campaign/add_recipients/
Add recipients to your campaign.

**Required Parameters:**
* **recipients:** JSON encoded list of e-mails to add to the campaign.  A limit of 100 recpicients per request is enforced.  The list can be a simple lists of e-mails or a list of lists.  The inner list should contain an e-mail and a map of the template context for the second item in the list.
* **list_id:** List ID
* **campaign_id:** Campaign ID

**Response:**
HTTP Response 200
<hr>
### /api/campaign/send/test/
Send a test campaign e-mail

**Required Parameters:**
* **subject:** subject of e-mail
* **reply_to:** reply to e-mail address
* **list_id:** List ID, unique url safe string to identify list
* **campaign_id:** Campaign ID, unique url safe string to identify campaign
* **text:** text template for body of e-mail
* **test_emails:** JSON encoded list of e-mails to add to the campaign.  A limit of 100 recpicients per request is enforced.  The list can be a simple lists of e-mails or a list of lists.  The inner list should contain an e-mail and a map of the template context for the second item in the list.

**Optional Parameters:**
* **html:** html template for body of e-mail
* **from_name:** Display name for from address
* **analytics:** Anayltics string added to each URL for services such as Google Anayltics.  Example: ``utm_source=monthlyMailt&utm_medium=email&utm_campaign=campaign1``

**Response:**
HTTP Response 200
<hr>
### /api/campaign/send/
Send a campaign

**Required Parameters:**
* **list_id:** List ID
* **campaign_id:** Campaign ID

**Response:**
HTTP Response 200
