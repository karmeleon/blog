#!/bin/bash

NAME="blog"                                       # Name of the application
DJANGODIR=/django/blog                            # Django project directory
SOCKFILE=/django/run/gunicorn.sock                # we will communicte using this unix socket
USER=django                                       # the user to run as
GROUP=django                                      # the group to run as
NUM_WORKERS=9                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=blog.prod_settings         # which settings file should Django use
DJANGO_WSGI_MODULE=blog.wsgi                      # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source ../blog-env/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Update venv as necessary
pip install -r requirements.txt
# Rebuild the database
python manage.py buildsite
# Recompile SCSS
python manage.py compilescss
# Populate static files directory
python manage.py collectstatic --noinput

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-
