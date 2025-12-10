FROM python:3.12-slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app/backend

# Install system dependencies (minimal for production)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry and dependencies
COPY pyproject.toml poetry.lock* /app/backend/
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.in-project true && poetry install --no-root --without dev --no-cache

# Copy backend source code
COPY backend/ /app/backend

# Change ownership to non-root user
RUN chown -R appuser:appuser /app
# Switch to user to run collectstatic (permissions)
USER appuser

# Run collectstatic (using a dummy secret key if needed for build)
ENV SECRET_KEY=build_dummy_key
RUN poetry run python manage.py collectstatic --noinput

# Expose port for Gunicorn (internal to Docker network)
EXPOSE 8080

# Run Gunicorn with dynamic port and migration
CMD ["sh", "-c", "poetry run python manage.py migrate && poetry run gunicorn web.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 3"]
