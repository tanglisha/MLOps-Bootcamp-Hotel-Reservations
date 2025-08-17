# Requires secrets from compose file to work
# Building this image takes a long time because it's creating the model

FROM python:slim as build_model

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

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

# Copy over the project files needed in the image
COPY ./src /app/src
COPY ./config /app/config
COPY ./pipeline /app/pipeline
COPY pyproject.toml /app/pyproject.toml
COPY ./config /app/config
COPY ./static /app/static
COPY ./templates /app/templates
COPY ./application.py /app/application.py

RUN poetry install

RUN --mount=type=secret,id=GOOGLE_APPLICATION_CREDENTIALS,target=/app/gcp_key.json \
    GOOGLE_APPLICATION_CREDENTIALS=/app/gcp_key.json poetry run python pipeline/training_pipeline.py

FROM python:slim
COPY --from=build_model /app/artifacts/models:/app/artifacts/models
COPY --from=build_model /app/config:/app/config
COPY --from=build_model /app/application.py:/app/application.py

RUN pip update --upgrade pip joblib flask

EXPOSE 5000

RUN chown -R app:app /app
USER app

CMD ["poetry", "run", "python", "application.py" ]