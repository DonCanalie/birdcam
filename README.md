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
