FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copy source code
COPY anonymoustrace/ anonymoustrace/
COPY LICENSE .
COPY README.md .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

# Set entrypoint
ENTRYPOINT ["anonymoustrace"]
