FROM python:3.6

ENV FLASK_APP faketube.py
ENV FLASK_CONFIG development

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

EXPOSE 5000
CMD "gunicorn -b 0.0.0.0:5000 -w 3 --access-logfile - --error-logfile - faketube:app"