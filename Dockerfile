# Requires secrets from compose file to work

FROM python:slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ARG SECRETS_DIR=/app

WORKDIR /app
RUN useradd -b /app -s /bin/bash app

RUN apt update && \
    apt install -y --no-install-recommends \ 
    libgomp1 \
    direnv \
    git \
    && \
    apt clean \
    && \
    rm -rf /var/lib/apt/lists \
    && \
    chown app:app /app

RUN pip install --upgrade pip poetry && touch README.md

COPY ./src /app/src
COPY ./config /app/config
COPY ./pipeline /app/pipeline
COPY pyproject.toml /app/pyproject.toml
COPY ./config /app/config
COPY ./creds* /creds

RUN poetry install

RUN --mount=type=secret,id=GOOGLE_APPLICATION_CREDENTIALS,target=/app/gcp_key.json \
    GOOGLE_APPLICATION_CREDENTIALS=/app/gcp_key.json poetry run python pipeline/training_pipeline.py

EXPOSE 8080
EXPOSE 8000

RUN chown -R app:app /app
USER app

CMD ["poetry", "run", "python", "application.py" ]