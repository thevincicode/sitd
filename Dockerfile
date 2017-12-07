FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
#ADD requirements.txt /code/
COPY . /code
RUN pip install -r requirements.txt
#RUN python manage.py syncdb --noinput
#RUN (cd /deploy/myblog && python manage.py migrate --noinput)
#RUN (cd /deploy/myblog && python manage.py collectstatic --noinput)
