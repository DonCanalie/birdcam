#!/bin/bash
# This script requires mjpg-streamer-experimental to be installted.
# The difference to the non-experimental version is the raspicam support.
# In production, this will not be needed, because it will be used a normal 
# USB-Webcam. The script needs to be run with root access.

PORT=8080
FPS=15

export LD_LIBRARY_PATH=/usr/local/lib

mjpg_streamer -i "input_raspicam.so -fps %FPS% -x 1280 -y 960" -o "output_http.so -w /usr/local/www -p %PORT%"
