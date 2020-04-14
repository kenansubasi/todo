FROM python:3.6
RUN apt-get update
RUN apt-get install -y gettext
ENV PYTHONUNBUFFERED 1

## Source code
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /code/
