FROM python:3.9

RUN apt-get update && apt-get install -y postgresql-client redis-tools 

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt

COPY . /app

WORKDIR /app

CMD  ["gunicorn", "task_backend.wsgi:application", "--bind", "0:8000" ] 