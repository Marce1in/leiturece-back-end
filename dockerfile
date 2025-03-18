FROM python:3.13-alpine

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    build-base \
    curl \
    python3-dev \
    musl-dev \
    libffi-dev \
    openssl-dev \
    gcc

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Configure poetry to not use virtualenvs inside Docker
RUN poetry config virtualenvs.create false

# Copy poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry install --no-interaction --no-ansi

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
