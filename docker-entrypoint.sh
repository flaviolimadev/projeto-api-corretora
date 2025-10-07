#!/bin/bash
set -e

echo "🚀 Starting TradingView API..."

# Função para cleanup
cleanup() {
    echo "🛑 Stopping services..."
    kill -TERM "$GUNICORN_PID" "$WORKER_PID" 2>/dev/null || true
    wait "$GUNICORN_PID" "$WORKER_PID" 2>/dev/null || true
    exit 0
}

# Registrar handler de sinal
trap cleanup SIGTERM SIGINT

# Verificar se o worker está habilitado
WORKER_ENABLED=${WORKER_ENABLED:-True}

# Iniciar Gunicorn em background
echo "📡 Starting Gunicorn server..."
gunicorn --bind 0.0.0.0:5000 \
    --workers 4 \
    --worker-class eventlet \
    --worker-connections 1000 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    app:app &
GUNICORN_PID=$!

echo "✅ Gunicorn started (PID: $GUNICORN_PID)"

# Iniciar worker se habilitado
if [ "$WORKER_ENABLED" = "True" ] || [ "$WORKER_ENABLED" = "true" ]; then
    echo "🔄 Starting background worker..."
    sleep 5  # Aguardar Gunicorn iniciar
    cd webapp && python -m workers.main_worker_production &
    WORKER_PID=$!
    echo "✅ Worker started (PID: $WORKER_PID)"
else
    echo "⏸️  Worker disabled (WORKER_ENABLED=$WORKER_ENABLED)"
    WORKER_PID=""
fi

echo "🎉 All services started successfully!"
echo "📊 Gunicorn PID: $GUNICORN_PID"
[ -n "$WORKER_PID" ] && echo "🔄 Worker PID: $WORKER_PID"

# Aguardar processos
wait $GUNICORN_PID $WORKER_PID
