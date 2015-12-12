#!/bin/bash
# This script requires mjpg-streamer-experimental to be installted.
# The difference to the non-experimental version is the raspicam support.
# In production, this will not be needed, because it will be used a normal 
# USB-Webcam.

PORT=8080
FPS=10
WIDTH=640
HEIGHT=400
WWW=/usr/local/www

export LD_LIBRARY_PATH=/usr/local/lib

mjpg_streamer -i "input_raspicam.so -fps $FPS -x $WIDTH -y $HEIGHT" -o "output_http.so -w $WWW -p $PORT"
