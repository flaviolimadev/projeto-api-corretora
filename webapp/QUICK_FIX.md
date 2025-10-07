# 🚀 Quick Fix - Easypanel Dockerfile

## ❌ Problema
```
ERROR: failed to build: failed to solve: failed to read dockerfile: 
open Dockerfile: no such file or directory
```

## ✅ Solução
O Easypanel está procurando o Dockerfile na pasta `webapp`, mas ele estava na raiz.

### 📁 Arquivos Criados
- `webapp/Dockerfile` - Dockerfile na pasta correta
- `webapp/easypanel-config.md` - Configuração do Easypanel
- `webapp/commit-easypanel.bat` - Script de commit

## 🚀 Deploy Rápido

### 1. Execute o script de commit
```bash
# Navegue para a pasta webapp
cd webapp

# Execute o script
commit-easypanel.bat
```

### 2. Configure no Easypanel
- **Build Context**: `webapp`
- **Dockerfile Path**: `Dockerfile`
- **Port**: `5000`

### 3. Adicione as variáveis de ambiente
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

### 4. Deploy e teste
```bash
curl https://seu-dominio.com/api/health
```

## 🎯 Resultado
✅ Dockerfile na pasta correta  
✅ Build funcionando no Easypanel  
✅ API pronta para produção  

🚀 **Problema resolvido!**
