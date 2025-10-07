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

# Create entrypoint script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "🚀 Starting TradingView API..."\n\
cleanup() {\n\
    echo "🛑 Stopping services..."\n\
    kill -TERM "$GUNICORN_PID" "$WORKER_PID" 2>/dev/null || true\n\
    wait "$GUNICORN_PID" "$WORKER_PID" 2>/dev/null || true\n\
    exit 0\n\
}\n\
trap cleanup SIGTERM SIGINT\n\
WORKER_ENABLED=${WORKER_ENABLED:-True}\n\
echo "📡 Starting Gunicorn server..."\n\
gunicorn --bind 0.0.0.0:5000 --workers 4 --worker-class eventlet --worker-connections 1000 --timeout 120 --access-logfile - --error-logfile - app:app &\n\
GUNICORN_PID=$!\n\
echo "✅ Gunicorn started (PID: $GUNICORN_PID)"\n\
if [ "$WORKER_ENABLED" = "True" ] || [ "$WORKER_ENABLED" = "true" ]; then\n\
    echo "🔄 Starting background worker..."\n\
    sleep 5\n\
    cd webapp && python -m workers.main_worker_production &\n\
    WORKER_PID=$!\n\
    echo "✅ Worker started (PID: $WORKER_PID)"\n\
else\n\
    echo "⏸️  Worker disabled"\n\
    WORKER_PID=""\n\
fi\n\
echo "🎉 All services started!"\n\
wait $GUNICORN_PID $WORKER_PID' > /entrypoint.sh && chmod +x /entrypoint.sh

# Run the application
ENTRYPOINT ["/entrypoint.sh"]