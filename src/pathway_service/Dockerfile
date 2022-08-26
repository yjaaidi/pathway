FROM python:3.10.6-bullseye

WORKDIR /usr/src/app

COPY tools/download-models.sh tools/
RUN tools/download-models.sh

RUN pip install poetry==1.1.15

COPY pyproject.toml poetry.lock ./
COPY src ./src

RUN poetry install --extras service

CMD ["poetry", "run", "start-service"]
