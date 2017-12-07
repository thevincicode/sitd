FROM python:3.6.3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code
RUN pip install -r requirements.txt --no-cache-dir
