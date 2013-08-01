# Tracking
GAE Bulk Mailer includes several tracking features.

To view tracking done by the Bulk Mailer system go to: _/api/stats/{{ list_id }}/{{ campaign_id }}/_

This URL is secured for Staff users only which is defined in
your settings.  This URL can be opened for viewing domain wide or for individual users.  Statistics are compiled
by the schedule in your cron.yaml or when some clicks "Compile Stats Now".

## Web Anayltics
The first and easiest way to track is to use existing tracking solutions integrated into your site.
You can add a tracking code to all your URLs by using the 'analytics' parameter when creating a campaign. This will 
allow you to track clicks in services like Google Analytics.

## Open Tracking
Open tracking is done by inserting a small 1 pixel tracking image at the end of your body tag. This type of 
tracking has some inherit limitations but is the best way to track e-mail opens currently.
Some of the limitations are:
1. The e-mail client must show images.  By default some clients like GMail do not.
2. You must send an HTML version of your message to track.  Text e-mails can not be tracked.

## Click Tracking
Links are tracked by replacing all your URLs with ones that go through the Bulk Mailer system.  When a link is 
clicked it is first sent to the Bulk Mailer which records the click and then redirects the user to the original
URL.

### Link Tags
You can add further tracking to your URLs by tagging them. This allows you to track what parts of your campaign
are more effective.

To tag a URL simply add something like the following to a URL: **#bmtags:tag1,tag2**

You can further group tags like: **#bmtags:group1:tag1,group1:tag2**

The bmtag string will be removed from your URL during template processing and will be recorded for tracking.

## Image Tracking
Images are currently not tracked but they are giving a URL redirect because spam filters may flag your message
if you do not have images that contain HTTPS URLs.
