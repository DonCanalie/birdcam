#!/bin/bash
DIR=$(dirname $0)
sqlite3 $DIR/../birdcam.db "insert into climate values(`python $DIR/../readDHT22.py`);"
