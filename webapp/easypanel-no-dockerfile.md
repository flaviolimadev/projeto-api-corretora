# 🚀 Easypanel sem Dockerfile - TradingView API

## 📋 Configuração no Easypanel

### 1. **Tipo de Serviço**
- **Service Type**: `Python`
- **Python Version**: `3.11`

### 2. **Build Settings**
- **Build Command**: 
```bash
pip install -r requirements.production.txt
```

- **Start Command**:
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 --worker-class eventlet --worker-connections 1000 --timeout 120 --keep-alive 2 --max-requests 1000 --max-requests-jitter 100 app:app
```

### 3. **Working Directory**
- **Working Directory**: `/app/webapp`

### 4. **Port Configuration**
- **Port**: `5000`
- **Protocol**: `HTTP`

### 5. **Environment Variables**
```env
# Database Configuration
DATABASE_URL=postgres://postgres:6b7215f9594dea0d0673@easypainel.ctrlser.com:5435/corretora?sslmode=disable

# API Configuration
API_HOST=0.0.0.0
API_PORT=5000
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta-super-segura

# Worker Configuration
WORKER_ENABLED=True
WORKER_THREADS=4
MAX_ASSETS_PER_SYNC=100
SYNC_INTERVAL_CATEGORIES=3600
SYNC_INTERVAL_ASSETS=1800
SYNC_INTERVAL_CANDLES=60
SYNC_INTERVAL_CURRENT=1

# Cache Configuration
CACHE_ENABLED=True
CACHE_TTL=300

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/app.log

# Python Path
PYTHONPATH=/app/webapp:/app
```

## 🐍 Configuração Python

### 1. **requirements.txt** (na raiz do projeto)
```txt
# Core Flask Application
Flask==3.0.0
flask-socketio==5.3.6
flask-cors==4.0.0
python-socketio==5.11.0
eventlet==0.35.1

# TradingView Integration
tradingview-scraper==0.4.8
requests==2.31.0

# Database
prisma==0.12.0
python-dotenv==1.0.0
psycopg2-binary==2.9.9

# Production Server
gunicorn==21.2.0
gevent==23.9.1

# Utilities
python-dateutil==2.8.2
pytz==2023.3
```

### 2. **Procfile** (na raiz do projeto)
```
web: cd webapp && gunicorn --bind 0.0.0.0:5000 --workers 4 --worker-class eventlet --worker-connections 1000 --timeout 120 --keep-alive 2 --max-requests 1000 --max-requests-jitter 100 app:app
```

### 3. **runtime.txt** (na raiz do projeto)
```
python-3.11.0
```

## 🚀 Deploy

### 1. **Commit dos arquivos**
```bash
git add .
git commit -m "Configuração Easypanel sem Dockerfile"
git push origin main
```

### 2. **Configurar no Easypanel**
- Service Type: Python
- Python Version: 3.11
- Build Command: `pip install -r requirements.txt`
- Start Command: `cd webapp && gunicorn --bind 0.0.0.0:5000 --workers 4 --worker-class eventlet app:app`
- Working Directory: `/app/webapp`
- Port: 5000

### 3. **Deploy e teste**
```bash
curl https://seu-dominio.com/api/health
```

## 📊 Estrutura do Projeto

```
tradingview-scraper/
├── requirements.txt          # ← Dependências Python
├── Procfile                  # ← Comando de start
├── runtime.txt              # ← Versão do Python
└── webapp/                  # ← Código da aplicação
    ├── app.py
    ├── api_database.py
    ├── .env
    └── ...
```

## 🎯 Vantagens

- ✅ Sem necessidade de Dockerfile
- ✅ Usa imagem Python oficial
- ✅ Build mais rápido
- ✅ Configuração mais simples
- ✅ Fácil de debugar

## 🧪 Teste

Após o deploy:
```bash
curl https://seu-dominio.com/api/health
```

Deve retornar:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-07T12:36:24.000Z",
  "version": "1.0.0",
  "database": "healthy"
}
```

---

## 🎉 Conclusão

Esta configuração elimina a necessidade do Dockerfile e usa a funcionalidade nativa do Python do Easypanel.

🚀 **Solução mais simples e eficiente!**
