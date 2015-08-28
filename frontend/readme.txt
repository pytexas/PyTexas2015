Roost Chrome Installation Files - May 05, 2015

------
Chrome & SSL

Chrome notifications require that your site is on SSL/HTTPS. This security feature is required by the underlying ServiceWorker technology (that makes all this possible) for security reasons.

This means that you must have an SSL certificate configured with your host. SSL certificates can normally be obtained from your web host, or can be purchased from third party certificate providers. Setting up SSL is different for each web host (where your site is served from). Contact your web host for details, the process is not usually very difficult.

Cloudflare

Cloudflare can provide SSL for many types of sites. Sign up a free Cloudflare account here:  https://cloudflare.com

Once your Cloudflare account is set up and configured for your site, then you can enable SSL. Click on the 'Cloudflare Settings' next to your domain on the Cloudflare dashboard. Enable SSL using one of the options shown.

------

Chrome Install Files

3 files need to be installed at the root level of your site's server.  These files work together with the Roost system to enable the opt-in and sending process for Chrome notifications.

These files are generated based on your site's settings, and should not be modified. The purpose and content of each file is described below. 

roost.html:  This drives the whole process, installs the service worker and handles notification clicks.

roost_manifest.json:  This identifies your site to Google and drives some of the backend push components.

roost_worker.js:  This file receives the pushes, communicates with Roost, and shows the actual notifications.

------

Troubleshooting:

- Check out the JavaScript console for any errors.  In Chrome navigate to View -> Developer -> JavaScript Console.

- Make sure you are using the latest Chrome Browser (M42).

- Refresh your page a couple more times (the Internet is like that).

- Are you using multiple domains or odd subdomain configurations? Contact support and we’ll take a look.

- Did you install the files somewhere other than root (“/”)?  Contact support and we’ll help you with that. 

- 301 Redirect: If you are just making the switch to SSL, make sure you use a 301 Redirect to push your HTTP traffic to HTTPS. Check with us if you don't know how to do this.

- Permission Error (403): Does the directory where the Chrome files are stored have the correct permissions?

------

If you have any issues, contact support@goroost.com.
