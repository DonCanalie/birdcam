## This is an app to control the birdcam surveillance system using Raspberry Pi

### Install Instructions:

```
# The following Firmware-Upgrade should defenitely be run to fix problems, 
# that may occur with the cameras and make the Raspberry Pi stop working
rpi-update  

apt-get install python lighttpd libfam0 spawn-fcgi build-essential python-dev

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
```

# Enable IP-forwarding by editing /etc/sysctl.conf and uncomment:
net.ipv4.ip_forward = 1

# Save and enable changes with
sysctl -p /etc/sysctl.conf

# Restart networking with
service networking restart

# Optionally set iptables-rules for accessing the lte-stick's webinterface over lan
sudo iptables -A PREROUTING -t nat -p tcp -m tcp --dport <lan port> -j DNAT --to-destination <ip-address of the lte-stick's webinterface>:80/24
sudo iptables -t nat -A POSTROUTING -p tcp -m tcp -s <ip-address of the lte-stick's webinterface>/24 --sport 80 -j SNAT --to-source <lan ip-address>
sudo iptables -A FORWARD -m state -p tcp -d <ip-address of the lte-stick's webinterface>/24 --dport 80 --state NEW,ESTABLISHED,RELATED -j ACCEPT

# Save iptables-rules
sudo sh -c "iptables-save > /etc/iptables.rules"

# /etc/network/interface-rule for bringing iptables-rules up, when lan-interface ist coming up
# Add this to /etc/network/interface
<your lan-interfaces's config>
  pre-up iptables-restore < /etc/iptables.rules
  
# On your client, your have to add a static rule for accessing the lte-stick's webinterface
route add <lte-sticks netaddress> mask 255.255.255.0 <birdcam's lan-ipaddress>


