
# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-alpine
LABEL maintainer="project2-20"

COPY ./requirements.txt /requirements.txt
COPY ./project2 /project2
WORKDIR /project2

RUN 'echo "WSGIPassAuthorization On" >> /etc/apache2/apache2.conf'


# RUN python -m pip install google-cloud-storage
# RUN python -m pip install django-storages
# RUN python -m pip install google-auth
# RUN python -m pip install google

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt && \
    adduser --disabled-password --no-create-home django-user

# sets environmnet python variable to venv
ENV PATH="/py/bin:$PATH"

USER django-user
# # Allow statements and log messages to immediately appear in the Knative logs
# ENV PYTHONUNBUFFERED True

# # Copy local code to the container image.
# ENV APP_HOME /app
# WORKDIR $APP_HOME
# COPY . ./

# # Install production dependencies.

# RUN python -m pip install google.auth

# # Run the web service on container startup. Here we use the gunicorn
# # webserver, with one worker process and 8 threads.
# # For environments with multiple CPU cores, increase the number of workers
# # to be equal to the cores available.
# # Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app 