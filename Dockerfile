FROM python:3.7.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt
RUN python -m spacy validate
RUN python -m spacy download en_core_web_sm
RUN python -m spacy link en_core_web_sm en

COPY . /code/

EXPOSE 8080

CMD ["python", "manage.py", "runserver"]