#!/bin/sh -e
 
cd /var/www/easeyourshop/
 
#projectname=$(basename $(pwd))
#. ~/virtualenv/$projectname/bin/activate
 
unset GIT_DIR
git pull
 
#./manage.py collectstatic --noinput
 
#touch ../tmp/restart.txt
