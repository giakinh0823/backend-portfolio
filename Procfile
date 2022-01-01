release: python manage.py migrate
release: python -m spacy validate
release: python -m spacy download en_core_web_sm
release: python -m spacy link en_core_web_sm en
web: daphne backend.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: celery -A backend worker -l info
worker: python manage.py runworker channel_layer -v2
