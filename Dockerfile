# 1. Base image
FROM python:3.12-slim as base

# 2. Set working directory
WORKDIR /app

# 3. Install Poetry and dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# 4. Copy application code
COPY app ./app

# 5. Expose port
EXPOSE 8000

# 6. Runtime command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]