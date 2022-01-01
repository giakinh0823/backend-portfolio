release: chmod u+x release.sh && ./release.sh
web: daphne backend.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: celery -A backend worker -l info
worker: python manage.py runworker channel_layer -v2
