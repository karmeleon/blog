FROM python:3.7-alpine

RUN apk add --no-cache alpine-sdk zlib-dev py3-lxml jpeg-dev libxml2-dev libxslt-dev
EXPOSE 8000

COPY requirements.txt /
RUN pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN python manage.py migrate --noinput
RUN python manage.py buildsite
RUN python manage.py compilescss
RUN python manage.py collectstatic --noinput

CMD python manage.py runserver 0.0.0.0:8000
