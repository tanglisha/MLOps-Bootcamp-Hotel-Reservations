FROM python:slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_OPTIONS_SYSTEM_SITE_PACKAGES=1

WORKDIR /app

# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#     && \
#     libgomp1 \
#     && \
#     apt get clean \
#     && \
#     rm -rf /var/lib/apt/lists

RUN pip install poetry && touch README.md

# COPY ./*.py /app/
COPY ./src /app/src
COPY ./config /app/config
COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock

RUN pip install --upgrade

RUN poetry install

RUN poetry run python pipeline/training_pipeline.py && poetry env activate

EXPOSE 8080
EXPOSE 8000

ENTRYPOINT [ "poetry run" ]

CMD [ "python", "application.py" ]