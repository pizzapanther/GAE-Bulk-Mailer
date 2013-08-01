# Directions for install GAE Bulk Mailer
Assumes you have the [Google App Engine Python SDK](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python) installed.

1. Create an app on Google App Engine (https://appengine.google.com/start/createapp?)
2. Clone GAE Bulk Mailer ``git@github.com:pizzapanther/GAE-Bulk-Mailer.git your-app-id``
3. Create your configuration files<br>
``cd your-app-id``<br>
``cp app.yaml.example app.yaml``<br>
``cp queue.yaml.example queue.yaml``<br>
``cp cron.yaml.example cron.yaml``<br>
``touch local_settings.py``
4. Insert your app ID into app.yaml.
5. Tweak queue.yaml depending on your send rate limits.
6. Tweak your local_settings.py.  Some settings you may wish to add:<br>
``SUPER_ADMINS = ('your_address@gmail.com',)``<br>
``STAFF_USERS = ('staff_user@gmail.com',)``<br>
``STAFF_DOMAINS = ('gmail-app-domain.com',)``<br>
``ALLOWED_HOSTS = ('your-app-id.appspot.com', '1.your-app-id.appspot.com')``<br>
``DEFAULT_FROM_EMAIL = 'from_address@example.com'``<br>
``BASE_URL = 'https://your-app-id.appspot.com'``<br>
``REPORT_BOUNCE_URL = 'https://example.com/bounce_reporting_url'``<br>
``REPORT_UNSUBSCRIBE_URL = 'https://example.com/unsubscribe_reporting_url'``<br>
``REPORT_PAYLOAD = {'key': 'abcdefgh123456'}``<br>
``EMAILER = 'bulkmail.mailers.amazon' #Or 'bulkmail.mailers.gae'``<br>
``MAIL_SEND_RATE = 85``<br>
``MAIL_SEND_INTERVAL = 'seconds'``<br>
``AWS_KEY_ID = 'abcdefgh123456' #Needed for AWS Mailer only``<br>
``AWS_SECRET_KEY = 'abcdefgh123456'``
7. Upload your app: ``cd ..; appcfg.py update your-app-id``
8. Go to https://your-app-id.appspot.com/api/apikey/ to create an API Key.
9. Implement the bounce and unsubscribe hooks you provided.  See the 
[Web Hooks Documentation](docs/hooks.md) for more info.

### More Info
* [API Details](docs/api.md)
* [Bulkmailer.py](docs/bulkmailer.md) (API implemented in Python)
* [Web Hooks](docs/hooks.md)
* [Templating](docs/templates.md)
* [Tracking](docs/tracking.md)
* [Mailer Backends](docs/mailers.md)
