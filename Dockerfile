# Base Image
FROM python:3.11 AS base

ADD src $ROOT/src

# Set working directory
WORKDIR $ROOT/src

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry

RUN poetry self update 1.8.4
RUN poetry config virtualenvs.create false

# Copy dependencies files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the whole app
COPY . .

# Expose API port
EXPOSE 8000
EXPOSE 5432

# Add commands
COPY commands $ROOT/commands
RUN chmod +x $ROOT/commands/*
ENV PATH="$ROOT/commands:$PATH"

ENTRYPOINT [ "entrypoint.sh" ]
CMD [ "start.sh" ]

# Run migrations
RUN alembic upgrade head
