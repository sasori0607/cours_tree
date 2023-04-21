#!/bin/sh
#!/usr/bin/env python3


python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate


exec "$@"