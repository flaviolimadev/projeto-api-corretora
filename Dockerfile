FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Generate Prisma Client
RUN cd webapp && prisma generate --schema=./prisma/schema.prisma

# Create necessary directories
RUN mkdir -p logs export

# Set environment variables
ENV PYTHONPATH=/app/webapp:/app
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Copy entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Run the application with Gunicorn (production) and worker
ENTRYPOINT ["/docker-entrypoint.sh"]