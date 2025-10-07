# 🚀 Configuração Easypanel - TradingView API

## 📋 Configuração no Easypanel

### 1. Repository Settings
- **Repository URL**: URL do seu repositório Git
- **Branch**: `main` ou `master`
- **Build Context**: `webapp` (pasta webapp)
- **Dockerfile Path**: `Dockerfile` (dentro da pasta webapp)

### 2. Environment Variables
Adicione as seguintes variáveis de ambiente no painel do Easypanel:

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
```

### 3. Port Configuration
- **Port**: `5000`
- **Protocol**: `HTTP`

### 4. Domain Configuration (Opcional)
- Adicione seu domínio personalizado
- Configure SSL se necessário

## 🐳 Estrutura do Projeto

```
tradingview-scraper/
├── webapp/                    # ← Build Context no Easypanel
│   ├── Dockerfile            # ← Dockerfile aqui
│   ├── app.py
│   ├── api_database.py
│   ├── requirements.production.txt
│   ├── .env
│   └── ...
└── ...
```

## 🚀 Deploy

### 1. Commit e Push
```bash
git add .
git commit -m "Ajuste docker para Easypanel - Dockerfile na pasta webapp"
git push origin main
```

### 2. Deploy no Easypanel
1. Vá para o painel do Easypanel
2. Configure o projeto com as configurações acima
3. Clique em "Deploy"
4. Aguarde o build completar

### 3. Verificar Deploy
```bash
# Health check
curl https://seu-dominio.com/api/health

# Documentação
curl https://seu-dominio.com/api/docs
```

## 📊 Endpoints da API

Após o deploy, sua API estará disponível em:

- **Health Check**: `https://seu-dominio.com/api/health`
- **Documentação**: `https://seu-dominio.com/api/docs`
- **Candles**: `https://seu-dominio.com/api/candles`
- **Candle Atual**: `https://seu-dominio.com/api/current-candle`
- **Categorias**: `https://seu-dominio.com/api/categories`
- **WebSocket**: `https://seu-dominio.com/socket.io/`

## 🔍 Troubleshooting

### Erro: "Dockerfile not found"
**Solução**: Certifique-se de que:
- Build Context está configurado como `webapp`
- Dockerfile Path está configurado como `Dockerfile`
- O Dockerfile existe na pasta webapp

### Erro: "Module not found"
**Solução**: Verifique se todas as dependências estão no `requirements.production.txt`

### Erro: "Database connection failed"
**Solução**: Verifique se a `DATABASE_URL` está correta

## 📈 Monitoramento

### Logs
No Easypanel, você pode ver os logs em:
- **Logs**: Seção "Logs" do serviço
- **Build Logs**: Logs do processo de build

### Health Check
O Easypanel automaticamente verifica a saúde da aplicação usando o endpoint `/api/health`.

---

## 🎉 Resultado

Após o deploy, você terá:
- ✅ API funcionando no Easypanel
- ✅ Endpoints de health check
- ✅ Documentação automática
- ✅ Logs estruturados
- ✅ Deploy automatizado via Git

🚀 **Sua API TradingView estará online e pronta para uso!**
