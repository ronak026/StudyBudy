release: python manage.py migrate --no-input && python manage.py collectstatic --no-input
web: gunicorn studybud.wsgi --log-file -
