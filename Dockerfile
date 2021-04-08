FROM python:3.9.1-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM base AS builder
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    curl

ENV POETRY_VERSION=1.1.5
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-dev

FROM base AS production

COPY --from=builder $VENV_PATH $VENV_PATH

RUN . $VENV_PATH/bin/activate

COPY ./.env /.env
COPY ./mass_mentioner/mass_mentioner.py /mass_mentioner/mass_mentioner.py

ENTRYPOINT ["python3", "/mass_mentioner/mass_mentioner.py"]
