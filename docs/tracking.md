# Tracking
GAE Bulk Mailer includes several tracking features.  To view tracking done by the Bulk Mailer system go to
'/api/stats/{{ list_id }}/{{ campaign_id }}/'.  This URL is secured for Staff users only which is defined in
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


## Image Tracking
Images are currently not tracked but they are giving a URL redirect because spam filters may flag your message
if you do not have images that contain HTTPS urls.
