python -m spacy validate
python -m spacy download en_core_web_sm
python -m spacy link en_core_web_sm en
python manage.py makemigrations
python manage.py migrate
