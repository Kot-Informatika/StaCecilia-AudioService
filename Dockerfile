FROM python:3.9.12-bullseye

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

WORKDIR /app

COPY index.py . 
COPY Pipfile .
COPY pretrained_models/ .

RUN pip install pipenv

RUN apt-get update && apt-get install -y --no-install-recommends gcc
RUN apt-get update && apt-get install -y --no-install-recommends libsndfile1-dev
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --skip-lock

EXPOSE 5000

CMD pipenv run python index.py