# Mailers
GAE Bulk Mailer was created to accomodate different e-mail backends which actually send your mail. Currently 
a Google and Amazon backend are included by default. For each mailer you will need to make sure you set your
send rate settings according to your quota limitations.

## Google Mailer (bulkmail.mailers.gae)
The Google Mailer uses the send mail system built into Google App Engine.  This is system is the easiest to use
but has [limitations](https://developers.google.com/appengine/docs/quotas#Mail). The biggest limit to note is that
even if you get billed you still can not go past 20,000 emails per day. I've tried to talk to Google representives
to see what the limit would be for premier accounts as their docs state it should be flexible if you go premier.
However, they stated you could not go above that limit.

## Amazon Mailer
The Amazon Mailer uses [Amazon SES](http://aws.amazon.com/ses/) to send mail and 
[Amazon SNS](http://aws.amazon.com/sns/) to recieve bounce and complaint notifications.  This requires more 
setup but Amazon will raise your send rate and send limit automatically as you use the service more.

### Amazon Setup Steps (assumes you have an Amazon AWS account)
1. Update your local_settings.py for the Amazon Mailer send rate limitations.
2. Create an Amazon Key and Secret and store in local_settings.py.
3. Upload your app to App Engine.
4. SNS: Create a Topic to the end point: https://your-app-id.appspot.com/amazon-bounce (once Amazon verifies the endpoint it will become selectable for the feedback settings)
5. SES: Verify your sender address.
6. SES: Setup your DKIM and DNS records for your domain and sender address.
7. SES: Setup your feedback for bounces and complaints to the topic created in step 3 for your domain and sender address.
8. SES: Make sure you Amazon SES account is out of sandbox mode.
