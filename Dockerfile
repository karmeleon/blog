FROM python:3.7-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN apk add --no-cache alpine-sdk zlib-dev py3-lxml jpeg-dev libxml2-dev libxslt-dev

RUN pip install -r requirements.txt
RUN python manage.py buildsite
RUN python manage.py compilescss
RUN python manage.py collectstatic --output

CMD python manage.py runserver 0.0.0.0:8000
