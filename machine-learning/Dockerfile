FROM python:3.12-bullseye AS builder

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=1 \
  POETRY_VIRTUALENVS_CREATE=1 \
  POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

FROM python:3.12-slim-bullseye AS runtime

ENV VIRTUAL_ENV=/app/.venv \
  PATH="/app/.venv/bin:$PATH" \
  PYTHONPATH=/app

WORKDIR /app

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY machine_learning ./machine_learning

# Point to __init__.py instead of main.py
ENTRYPOINT ["uvicorn", "machine_learning:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]