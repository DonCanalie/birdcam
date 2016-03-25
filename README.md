# This is an app to control the birdcam surveillance system using Raspberry Pi

# Install Instructions:

apt-get install python lighttpd libfam0 spawn-fcgi

git clone https://github.com/DonCanalie/birdcam

cd birdcam
pip install -r requirements.txt

sudo lighty-enable-mod fastcgi

# http://www.sunspot.co.uk/Projects/Joggler/lighttpd_as_root.html
cp resources/lighttpd/lighttpd /etc/lighttpd/lighttpd
cp resources/lighttpd/lighttpd/lighttpd.conf /etc/lighttpd/lighttpd/lighttpd.conf
cp resources/lighttpd/conf-enabled/10-fastcgi.conf /etc/lighttpd/conf-enabled/10-fastcgi.conf

# Open /etc/lighttpd/lighttpd.conf and correct the document-root to your project- or www-folder
server.document-root = "<www-folder>"

# Configure cron-jobs for dyndns-update and climate-logging
sudo crontab -e

# Starting dyndns-update daily at 5 am
* 5 * * * <birdcam-path>/scripts/ddns_update.sh
# Write current humidity and temperature to birdcam.db every 15 minutes
*/15 * * * * <birdcam-path>/scripts/dht22ToDB.sh

# If you don't have a ddns_update.sh, create a new file with the following content:

#!/bin/bash
curl "<address-to-your-dyndns-hoster>/<the-hosters-update-script>?key=<your-update-key>&host=<your-hosts-comma-separated>"

# for example try ddnss.de
# curl "https://ddnss.de/upd.php?key=<your-update-key>&host=<your-hosts-comma-separated"

