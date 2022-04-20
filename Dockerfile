FROM python:3.9.12-bullseye

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

RUN apt-get update && apt-get install -y --no-install-recommends gcc
RUN apt-get update && apt-get install -y --no-install-recommends libsndfile1-dev
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg
RUN apt-get update && apt-get install -y --no-install-recommends wget

WORKDIR /app

RUN wget https://github.com/deezer/spleeter/releases/download/v1.4.0/2stems.tar.gz
RUN mkdir -p ./pretrained_models/2stems && tar -xf 2stems.tar.gz -C ./pretrained_models/2stems

COPY index.py . 
COPY Pipfile .

RUN pip install pipenv

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --skip-lock

EXPOSE 5000

CMD pipenv run python index.py