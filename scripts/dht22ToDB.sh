#!/bin/bash
sqlite3 ../birdcam.db "insert into climate values(`python ../readDHT22.py`);"
