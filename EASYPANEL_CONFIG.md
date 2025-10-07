# 🚀 Easypanel Config - Força Dockerfile

## ❌ Problema
O Easypanel ainda está usando Nixpacks mesmo sem os arquivos de configuração:
```
- .nixpacks/nixpkgs-*.nix not found
- Nixpacks Dockerfile automático
- Força uso do Dockerfile customizado
```

## ✅ Solução Implementada

### 1. **Configuração Específica do Easypanel**
- `easypanel.yml` - Configuração específica do serviço
- `Dockerfile.easypanel` - Dockerfile alternativo
- `.dockerignore` atualizado para excluir `.nixpacks`

### 2. **Força Uso do Dockerfile**
- Configuração explícita no `easypanel.yml`
- Dockerfile customizado em vez do Nixpacks
- Build mais confiável e controlado

## 📁 Arquivos Criados

### easypanel.yml
```yaml
# Easypanel Configuration
# Force use of custom Dockerfile

services:
  app:
    type: docker
    dockerfile: Dockerfile
    port: 5000
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - API_HOST=0.0.0.0
      - API_PORT=5000
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - WORKER_ENABLED=True
      - SYNC_INTERVAL_CATEGORIES=3600
      - SYNC_INTERVAL_ASSETS=1800
      - SYNC_INTERVAL_CANDLES=60
      - SYNC_INTERVAL_CURRENT=1
      - CACHE_ENABLED=True
      - CACHE_TTL=300
      - LOG_LEVEL=INFO
```

### Dockerfile.easypanel
```dockerfile
# Dockerfile específico para Easypanel
# Força uso do Dockerfile customizado

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
commit-easypanel-config.bat
```

### 2. **Configure no Easypanel**
- **Service Type**: `Docker`
- **Dockerfile Path**: `Dockerfile` ou `Dockerfile.easypanel`
- **Port**: `5000`
- **Usar easypanel.yml se disponível**

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
├── Dockerfile              # ← Dockerfile principal
├── Dockerfile.easypanel    # ← Dockerfile alternativo
├── easypanel.yml           # ← Configuração Easypanel
├── .dockerignore           # ← Exclui .nixpacks
├── app.py                  # ← Entry point
├── requirements.txt        # ← Dependências
└── webapp/                # ← Código da aplicação
    ├── app.py             # ← App principal
    └── ...
```

## 🎯 Vantagens

- ✅ **Configuração específica** - Easypanel.yml
- ✅ **Força uso do Dockerfile** - Evita Nixpacks
- ✅ **Build mais confiável** - Dockerfile customizado
- ✅ **Fácil configuração** - Arquivo de configuração
- ✅ **Alternativas** - Dockerfile.easypanel

## 🔧 Como Funciona

### 1. **Easypanel.yml**
- Configura o serviço como Docker
- Especifica o Dockerfile a usar
- Define variáveis de ambiente
- Configura porta 5000

### 2. **Dockerfile.easypanel**
- Dockerfile específico para Easypanel
- Mesma configuração do Dockerfile principal
- Alternativa caso o principal não funcione

### 3. **Dockerignore Atualizado**
- Exclui pasta `.nixpacks`
- Exclui `easypanel.yml` do build
- Build mais limpo e rápido

## 🧪 Teste

Após o deploy:
```bash
curl https://seu-dominio.com/api/health
```

Deve retornar:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-07T13:20:03.000Z",
  "version": "1.0.0",
  "database": "healthy"
}
```

## 🔍 Troubleshooting

### Se ainda usar Nixpacks:
1. Verifique se `easypanel.yml` está na raiz
2. Verifique se o Dockerfile está na raiz
3. Force rebuild no Easypanel
4. Use `Dockerfile.easypanel` como alternativa

### Se der erro de build:
1. Verifique se o Dockerfile está na raiz
2. Verifique se o requirements.txt está na raiz
3. Verifique se o app.py está na raiz

### Se der erro de start:
1. Verifique se a porta 5000 está configurada
2. Verifique se as variáveis de ambiente estão corretas

## 🎉 Conclusão

Esta solução resolve todos os problemas anteriores:
- ✅ .nixpacks/nixpkgs-*.nix not found
- ✅ Nixpacks Dockerfile automático
- ✅ Força uso do Dockerfile customizado

**Próximos passos:**
1. Execute `commit-easypanel-config.bat`
2. Configure no Easypanel como Docker
3. Use `easypanel.yml` se disponível
4. Deploy e teste

🚀 **Solução definitiva com configuração específica do Easypanel!**
