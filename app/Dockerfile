FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/bin/bash", "/usr/src/app/entrypoint.sh"]
