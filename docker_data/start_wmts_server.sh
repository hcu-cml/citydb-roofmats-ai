#!/bin/bash

# Start your Python server in the background
python3 /opt/wmts.py &

# Start Apache in the foreground
apachectl -D FOREGROUND