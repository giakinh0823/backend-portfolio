release: chmod u+x release.sh && ./release.sh
web: python -m spacy validate && python -m spacy download en_core_web_sm && python -m spacy link en_core_web_sm en &&  daphne backend.asgi:application --port $PORT --bind 0.0.0.0 -v2 
celery: python -m spacy validate && python -m spacy download en_core_web_sm && python -m spacy link en_core_web_sm en && celery -A backend worker -l info && celery -A backend beat --pool=solo -l info && wait -n 
worker1: python manage.py runworker channel_layer -v2
worker2: python -m spacy validate && python -m spacy download en_core_web_sm && python -m spacy link en_core_web_sm en  && celery -A backend worker -l info --concurrency=4 && celery -A backend beat --pool=solo -l info && python manage.py runworker channel_layer -v2 && wait -n

