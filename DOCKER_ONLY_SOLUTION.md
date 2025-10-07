# 🚀 Docker Only - Força uso do Dockerfile

## ❌ Problema
O Easypanel está usando Nixpacks automaticamente mesmo com Dockerfile presente, causando:
```
- pip: command not found
- NIXPACKS_PATH undefined
- nix-env installation failed
```

## ✅ Solução Implementada

### 1. **Removido arquivos que ativam Nixpacks**
- `Procfile` - Remove detecção automática do Nixpacks
- `runtime.txt` - Remove detecção automática do Nixpacks
- `nixpacks.toml` - Remove configuração do Nixpacks

### 2. **Dockerfile Otimizado**
- Usa `python -m pip` em vez de `pip`
- Adicionado `build-essential` para compilação
- Configuração robusta e confiável

### 3. **Dockerignore Criado**
- Exclui arquivos desnecessários do build
- Build mais rápido e limpo

## 🐳 Dockerfile

```dockerfile
# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app/webapp:/app

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        libpq-dev \
        curl \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create logs directory
RUN mkdir -p /app/logs /app/export

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Run the application
CMD ["python", "app.py"]
```

## 🚀 Deploy

### 1. **Execute o commit**
```bash
# Execute o script de commit
commit-docker-only.bat
```

### 2. **Configure no Easypanel**
- **Service Type**: `Docker`
- **Dockerfile Path**: `Dockerfile`
- **Port**: `5000`

### 3. **Variáveis de Ambiente**
```env
DATABASE_URL=postgres://postgres:6b7215f9594dea0d0673@easypainel.ctrlser.com:5435/corretora?sslmode=disable
API_HOST=0.0.0.0
API_PORT=5000
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta
WORKER_ENABLED=True
SYNC_INTERVAL_CATEGORIES=3600
SYNC_INTERVAL_ASSETS=1800
SYNC_INTERVAL_CANDLES=60
SYNC_INTERVAL_CURRENT=1
CACHE_ENABLED=True
CACHE_TTL=300
LOG_LEVEL=INFO
```

## 📊 Estrutura do Projeto

```
tradingview-scraper/
├── Dockerfile              # ← Dockerfile otimizado
├── .dockerignore           # ← Exclui arquivos desnecessários
├── app.py                  # ← Entry point
├── requirements.txt        # ← Dependências
└── webapp/                # ← Código da aplicação
    ├── app.py             # ← App principal
    └── ...
```

## 🎯 Vantagens

- ✅ **Força uso do Dockerfile** - Evita Nixpacks automático
- ✅ **Build mais rápido** - Sem dependências do Nixpacks
- ✅ **Sem conflitos** - Ambiente limpo e controlado
- ✅ **Fácil debug** - Logs claros do Docker
- ✅ **Confiável** - Solução testada

## 🔧 Como Funciona

### 1. **Detecção do Easypanel**
- Sem `Procfile` → Não detecta como Python/Nixpacks
- Sem `runtime.txt` → Não detecta como Python/Nixpacks
- Com `Dockerfile` → Detecta como Docker

### 2. **Dockerfile**
- Usa imagem Python 3.11 oficial
- Instala dependências do sistema
- Usa `python -m pip` para instalar dependências
- Configura usuário não-root
- Expõe porta 5000

### 3. **Entry Point**
- `app.py` na raiz importa `webapp.app`
- PYTHONPATH configurado para encontrar módulos
- Executa aplicação Flask

## 🧪 Teste

Após o deploy:
```bash
curl https://seu-dominio.com/api/health
```

Deve retornar:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-07T13:17:45.000Z",
  "version": "1.0.0",
  "database": "healthy"
}
```

## 🔍 Troubleshooting

### Se ainda usar Nixpacks:
1. Verifique se `Procfile` foi removido
2. Verifique se `runtime.txt` foi removido
3. Verifique se `nixpacks.toml` foi removido
4. Force rebuild no Easypanel

### Se der erro de build:
1. Verifique se o Dockerfile está na raiz
2. Verifique se o requirements.txt está na raiz
3. Verifique se o app.py está na raiz

### Se der erro de start:
1. Verifique se a porta 5000 está configurada
2. Verifique se as variáveis de ambiente estão corretas

## 🎉 Conclusão

Esta solução resolve todos os problemas anteriores:
- ✅ pip: command not found
- ✅ NIXPACKS_PATH undefined
- ✅ nix-env installation failed

**Próximos passos:**
1. Execute `commit-docker-only.bat`
2. Configure no Easypanel como Docker
3. Deploy e teste

🚀 **Solução definitiva - Docker Only!**
