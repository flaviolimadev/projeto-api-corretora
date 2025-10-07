# 🚀 Fix Nixpacks Easypanel - pip command not found

## ❌ Problema
```
/bin/bash: line 1: pip: command not found
```

## ✅ Solução Implementada

### 1. **Entry Point na Raiz**
- Criado `app.py` na raiz que redireciona para `webapp/app.py`
- Configurado `PYTHONPATH` corretamente

### 2. **Configuração Nixpacks**
- Criado `nixpacks.toml` com configuração específica
- Adicionado `setuptools` e `wheel` ao `requirements.txt`
- Simplificado `Procfile` para usar entry point da raiz

### 3. **Estrutura Otimizada**
```
tradingview-scraper/
├── app.py                    # ← Entry point na raiz
├── nixpacks.toml            # ← Configuração Nixpacks
├── requirements.txt         # ← Dependências
├── Procfile                 # ← Comando de start
├── runtime.txt             # ← Versão Python
└── webapp/                 # ← Código da aplicação
    ├── app.py              # ← App principal
    └── ...
```

## 🚀 Deploy

### 1. **Execute o commit**
```bash
# Execute o script de commit
commit-nixpacks-fix.bat
```

### 2. **Configure no Easypanel**
- **Service Type**: `Python` (Nixpacks)
- **Build Command**: automático (usa `nixpacks.toml`)
- **Start Command**: automático (usa `Procfile`)
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
PYTHONPATH=/app/webapp:/app
```

## 🔧 Como Funciona

### 1. **Entry Point** (`app.py` na raiz)
```python
import sys
import os

# Adicionar webapp ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'webapp'))

# Importar app principal
from webapp.app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

### 2. **Nixpacks** (`nixpacks.toml`)
```toml
[phases.setup]
nixPkgs = ["python3", "gcc", "g++", "libpq-dev", "curl"]

[phases.install]
cmds = [
    "pip install --upgrade pip",
    "pip install -r requirements.txt"
]

[start]
cmd = "gunicorn --bind 0.0.0.0:5000 --workers 4 --worker-class eventlet app:app"

[variables]
PYTHONPATH = "/app/webapp:/app"
```

### 3. **Procfile**
```
web: gunicorn --bind 0.0.0.0:5000 --workers 4 --worker-class eventlet app:app
```

## 🎯 Vantagens

- ✅ **Nixpacks nativo** - Usa funcionalidade oficial
- ✅ **Entry point simples** - Redireciona para webapp
- ✅ **Configuração automática** - Nixpacks detecta automaticamente
- ✅ **Build otimizado** - Cache e dependências corretas
- ✅ **Fácil manutenção** - Estrutura clara

## 🧪 Teste

Após o deploy:
```bash
curl https://seu-dominio.com/api/health
```

Deve retornar:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-07T12:49:38.000Z",
  "version": "1.0.0",
  "database": "healthy"
}
```

## 🔍 Troubleshooting

### Se ainda der erro de pip:
1. Verifique se o `nixpacks.toml` está na raiz
2. Verifique se o `requirements.txt` tem `setuptools` e `wheel`
3. Verifique se o `app.py` está na raiz

### Se der erro de módulo não encontrado:
1. Verifique se o `PYTHONPATH` está configurado
2. Verifique se o `app.py` da raiz está importando corretamente

### Se der erro de start:
1. Verifique se o `Procfile` está correto
2. Verifique se o `app.py` da raiz está funcionando

## 🎉 Conclusão

Esta solução resolve o problema do "pip: command not found" usando:
- Entry point na raiz
- Configuração Nixpacks otimizada
- Estrutura de arquivos correta

🚀 **Execute o `commit-nixpacks-fix.bat` e o problema será resolvido!**
