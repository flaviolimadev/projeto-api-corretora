# 🚀 Fix pip command not found - Nixpacks

## ❌ Problema
```
/bin/bash: line 1: pip: command not found
```

## ✅ Solução Implementada

### 1. **Nixpacks.toml Atualizado**
- Adicionado `python3Packages.pip` aos nixPkgs
- Usar `python3 -m pip` em vez de `pip`
- Configurado PATH para `/opt/venv/bin`

### 2. **Procfile Atualizado**
- Usar `python3 -m gunicorn` em vez de `gunicorn`

### 3. **Build Script**
- Criado `build.sh` com comandos corretos

## 🔧 Configuração

### nixpacks.toml
```toml
[phases.setup]
nixPkgs = ["python3", "python3Packages.pip", "gcc", "g++", "libpq-dev", "curl"]

[phases.install]
cmds = [
    "python3 -m pip install --upgrade pip",
    "python3 -m pip install -r requirements.txt"
]

[phases.build]
cmds = [
    "python3 -m pip install -r requirements.txt"
]

[start]
cmd = "cd webapp && python3 -m gunicorn --bind 0.0.0.0:5000 --workers 4 --worker-class eventlet app:app"

[variables]
PYTHONPATH = "/app/webapp:/app"
FLASK_APP = "webapp/app.py"
FLASK_ENV = "production"
PATH = "/opt/venv/bin:$PATH"
```

### Procfile
```
web: python3 -m gunicorn --bind 0.0.0.0:5000 --workers 4 --worker-class eventlet app:app
```

### build.sh
```bash
#!/bin/bash
echo "🚀 Building TradingView API with Nixpacks"
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
mkdir -p logs
mkdir -p export
echo "✅ Build completed successfully!"
```

## 🚀 Deploy

### 1. **Execute o commit**
```bash
# Execute o script de commit
commit-pip-fix.bat
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

## 🎯 Como Funciona

### 1. **Nixpacks Setup**
- Instala `python3` e `python3Packages.pip`
- Configura ambiente Python correto

### 2. **Install Phase**
- Usa `python3 -m pip` para instalar dependências
- Atualiza pip antes de instalar

### 3. **Build Phase**
- Reinstala dependências para garantir consistência

### 4. **Start Phase**
- Usa `python3 -m gunicorn` para iniciar aplicação
- Configura PATH corretamente

## 🧪 Teste

Após o deploy:
```bash
curl https://seu-dominio.com/api/health
```

Deve retornar:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-07T12:53:05.000Z",
  "version": "1.0.0",
  "database": "healthy"
}
```

## 🔍 Troubleshooting

### Se ainda der erro de pip:
1. Verifique se o `nixpacks.toml` tem `python3Packages.pip`
2. Verifique se está usando `python3 -m pip`
3. Verifique se o PATH está configurado

### Se der erro de gunicorn:
1. Verifique se está usando `python3 -m gunicorn`
2. Verifique se o gunicorn está instalado
3. Verifique se o entry point está correto

### Se der erro de módulo não encontrado:
1. Verifique se o `PYTHONPATH` está configurado
2. Verifique se o `app.py` da raiz está importando corretamente

## 🎉 Conclusão

Esta solução resolve o problema do "pip: command not found" usando:
- `python3 -m pip` em vez de `pip`
- `python3Packages.pip` nos nixPkgs
- PATH configurado corretamente
- Comandos atualizados em todos os arquivos

🚀 **Execute o `commit-pip-fix.bat` e o problema será resolvido!**
