# syntax=docker/dockerfile:1
# check=skip=SecretsUsedInArgOrEnv
FROM python:slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_OPTIONS_SYSTEM_SITE_PACKAGES=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=0

WORKDIR /app

RUN apt update && \
    apt install -y --no-install-recommends \ 
    libgomp1 \
    && \
    apt clean \
    && \
    rm -rf /var/lib/apt/lists

RUN pip install poetry && touch README.md

# COPY ./*.py /app/
COPY ./src /app/src
COPY ./config /app/config
COPY ./pipeline /app/pipeline
COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock
COPY ./config /app/config
COPY ./creds* /creds

RUN pip install --upgrade pip

RUN poetry install

# RUN if [ -z ${GOOGLE_APPLICATION_CREDENTIALS} ] ; then export GOOGLE_APPLICATION_CREDENTIALS="${GOOGLE_APPLICATION_CREDENTIALS}"; fi; poetry run python pipeline/training_pipeline.py
RUN poetry run python pipeline/training_pipeline.py
RUN poetry env activate

EXPOSE 8080
EXPOSE 8000

CMD ["poetry", "run", "python", "application.py" ]

# In GCP, enable Google Cloud Registry API, Google Artifact Registry API, and Cloud Resource Manager API
# Add role "owner" to service account. There's probably a better way to do this.