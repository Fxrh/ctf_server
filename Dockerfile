FROM ubuntu:latest
MAINTAINER fxrh

RUN apt-get update
RUN mkdir /var/run/dbus
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y nginx python3-pip python3-dbus dbus
RUN pip3 install django
RUN pip3 install gunicorn
RUN pip3 install django-debug-toolbar

ADD docker/nginxconf /etc/nginx/sites-enabled/default

ADD web/ /opt/ctfserver/
RUN chown -R www-data:www-data /opt/ctfserver
RUN mkdir /var/www/
RUN cd /opt/ctfserver && python3 manage.py collectstatic --noinput
ADD daemon/ctfdaemon /usr/local/bin/
ADD daemon/de.fxrh.ctfserver.conf /etc/dbus-1/system.d/
ADD daemon/de.fxrh.ctfserver.service /usr/share/dbus-1/system-services/

ADD docker/run_ctfserver.sh /usr/local/bin/

EXPOSE 80
CMD /usr/local/bin/run_ctfserver.sh
