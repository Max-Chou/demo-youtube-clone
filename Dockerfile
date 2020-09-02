FROM python:3.6

ENV FLASK_APP faketube.py
ENV FLASK_CONFIG development

WORKDIR /faketube

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY faketube.py config.py ./
RUN mkdir -p /faketube/uploads/videos \
    && mkdir -p /faketube/uploads/thumbnails \
    && mkdir -p /faketube/uploads/profiles

VOLUME /faketube/uploads

EXPOSE 5000
CMD "gunicorn -b 0.0.0.0:5000 --access-logfile - --error-logfile - faketube:app"