#!/bin/bash

mkdir -p /var/run/dbus || return 1
dbus-daemon --system || return 1
/etc/init.d/nginx start || return 1
cd /opt/ctfserver
gunicorn -u www-data -g www-data ctf_server.wsgi