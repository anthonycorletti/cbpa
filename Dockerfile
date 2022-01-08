FROM python:3.9.6-slim

ENV PYTHONUNBUFFERED True

WORKDIR /cbpa
COPY . /cbpa

RUN apt-get update -y \
    && apt-get install build-essential -y \
    && rm -rf /var/lib/apt/lists/* \
    && pip install flit \
    && FLIT_ROOT_INSTALL=1 flit install --deps production \
    && rm -rf $(pip cache dir)

CMD gunicorn cbpa.main:api -c cbpa/gunicorn_config.py
