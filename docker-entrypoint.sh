#!/bin/sh

if [ ! -f "/var/lib/mirbot/config.py" ] ; then
    cp /app/mirbot/mirbot/defaults.py /var/lib/mirbot/config.py
fi

if [ ! -f "/var/lib/mirbot/.module_lock" ] ; then
    if [ ! -d "/var/lib/mirbot/modules" ] ; then
        mkdir /var/lib/mirbot/modules
    fi

    for module in /app/mirbot/mirbot/modules/* ; do
        if [ -f ${module} ] ; then
            cp ${module} /var/lib/mirbot/modules/
        fi
    done

    touch /var/lib/mirbot/.module_lock
fi

mirbot --config /var/lib/mirbot
