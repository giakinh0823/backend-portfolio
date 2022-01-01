release: chmod u+x release.sh && ./release.sh
web: python -m spacy validate && python -m spacy download en_core_web_sm && python -m spacy link en_core_web_sm en &&  daphne backend.asgi:application --port $PORT --bind 0.0.0.0 -v2 
celery: python -m spacy validate && python -m spacy download en_core_web_sm && python -m spacy link en_core_web_sm en && celery -A backend worker -l info -c 10
worker: python manage.py runworker channel_layer -v2
