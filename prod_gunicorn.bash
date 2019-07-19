#!/bin/bash
NAME="SRIP-portal"
DJANGODIR=/root/srip-portal
USER=root
GROUP=sudo
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=portal.settings
DJANGO_WSGI_MODULE=portal.wsgi

cd $DJANGODIR
source /root/srip-portal/prodenv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  -D --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=0.0.0.0:9000 \
  --log-level=debug \
  --log-file=/root/srip-portal/logs/debug.log
