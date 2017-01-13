#!/bin/sh

if [ ! -f "/var/lib/mirbot/config.py" ] ; then
    cp /app/mirbot/mirbot/defaults.py /var/lib/mirbot/config.py
fi

mirbot --config /var/lib/mirbot
