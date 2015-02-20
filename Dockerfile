FROM ubuntu:latest
MAINTAINER fxrh

RUN mkdir -p /var/run/dbus && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y nginx python3-pip python3-dbus dbus && \
    pip3 install django gunicorn django-debug-toolbar

COPY docker/nginxconf /etc/nginx/sites-enabled/default
COPY docker/run_ctfserver.sh /usr/local/bin/

COPY daemon/ctfdaemon /usr/local/bin/
COPY daemon/de.fxrh.ctfserver.conf /etc/dbus-1/system.d/
COPY daemon/de.fxrh.ctfserver.service /usr/share/dbus-1/system-services/

COPY web/ /opt/ctfserver/
RUN chown -R www-data:www-data /opt/ctfserver && \
    mkdir /var/www/ && \
    cd /opt/ctfserver && python3 manage.py collectstatic --noinput

VOLUME /opt/ctfserver/db.sqlite3

EXPOSE 80
CMD /usr/local/bin/run_ctfserver.sh
