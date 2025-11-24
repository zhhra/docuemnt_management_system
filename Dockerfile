FROM python:3.12-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files first for caching
COPY pyproject.toml poetry.lock* /app/

# Install pip (upgrade) and dependencies
RUN python -m pip install --upgrade pip \
    && pip install --upgrade build setuptools wheel \
    && pip install .

# Copy the rest of the project
COPY . /app/

# Expose port
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
