web: gunicorn account.wsgi:application

release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input
release: python manage.py collectstatic --no-input
