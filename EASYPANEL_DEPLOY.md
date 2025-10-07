# 🚀 Deploy no Easypanel - TradingView API

Este guia mostra como fazer deploy da API TradingView no Easypanel.

## 📋 Pré-requisitos

- Conta no Easypanel
- Repositório Git configurado
- Banco PostgreSQL configurado no Easypanel

## 🔧 Configuração no Easypanel

### 1. Criar Novo Projeto

1. Acesse seu painel do Easypanel
2. Clique em "New Project"
3. Nome: `tradingview-api`
4. Selecione "From Git Repository"

### 2. Configurar Repositório

1. **Repository URL**: URL do seu repositório Git
2. **Branch**: `main` ou `master`
3. **Build Context**: Deixe vazio (usará o diretório raiz)
4. **Dockerfile Path**: `Dockerfile` (está na raiz)

### 3. Configurar Variáveis de Ambiente

No painel do Easypanel, adicione as seguintes variáveis de ambiente:

```env
# Database
DATABASE_URL=postgres://postgres:6b7215f9594dea0d0673@easypainel.ctrlser.com:5435/corretora?sslmode=disable

# API
API_HOST=0.0.0.0
API_PORT=5000
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta-super-segura

# Worker
WORKER_ENABLED=True
SYNC_INTERVAL_CATEGORIES=3600
SYNC_INTERVAL_ASSETS=1800
SYNC_INTERVAL_CANDLES=60
SYNC_INTERVAL_CURRENT=1

# Cache
CACHE_ENABLED=True
CACHE_TTL=300

# Logging
LOG_LEVEL=INFO
```

### 4. Configurar Porta

- **Port**: `5000`
- **Protocol**: `HTTP`

### 5. Configurar Domínio (Opcional)

1. Vá para "Domains"
2. Adicione seu domínio personalizado
3. Configure SSL se necessário

## 🐳 Estrutura do Projeto

```
tradingview-scraper/
├── Dockerfile              # ← Dockerfile na raiz (para Easypanel)
├── easypanel.yml           # Configuração específica
├── .env.easypanel          # Variáveis de ambiente
├── EASYPANEL_DEPLOY.md     # Este guia
└── webapp/                 # Código da aplicação
    ├── app.py
    ├── api_database.py
    ├── requirements.production.txt
    └── ...
```

## 🚀 Deploy

### 1. Push do Código

```bash
# Adicionar arquivos
git add .
git commit -m "Ajuste docker para Easypanel"
git push origin main
```

### 2. Deploy no Easypanel

1. No painel do Easypanel, clique em "Deploy"
2. Aguarde o build completar
3. Verifique os logs se houver problemas

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

**Solução**: Certifique-se de que o Dockerfile está na raiz do repositório, não na pasta `webapp`.

### Erro: "Module not found"

**Solução**: Verifique se o `PYTHONPATH` está configurado corretamente no Dockerfile.

### Erro: "Database connection failed"

**Solução**: Verifique se a `DATABASE_URL` está correta e se o banco está acessível.

### Erro: "Port already in use"

**Solução**: Certifique-se de que a porta 5000 está configurada corretamente no Easypanel.

## 📈 Monitoramento

### Logs

No Easypanel, você pode ver os logs em:
- **Logs**: Seção "Logs" do serviço
- **Build Logs**: Logs do processo de build

### Health Check

O Easypanel automaticamente verifica a saúde da aplicação usando o endpoint `/api/health`.

### Métricas

Para monitoramento avançado, considere:
- Configurar Prometheus/Grafana
- Usar serviços de monitoramento externos
- Configurar alertas no Easypanel

## 🔄 Atualizações

Para atualizar a aplicação:

1. Faça as alterações no código
2. Commit e push para o repositório
3. No Easypanel, clique em "Deploy"
4. Aguarde o novo build

## 📞 Suporte

### Logs Importantes

- **Build Logs**: Verificar erros de build
- **Application Logs**: Verificar erros de runtime
- **Health Check**: Verificar status da aplicação

### Comandos Úteis

```bash
# Testar API localmente
curl https://seu-dominio.com/api/health

# Verificar documentação
curl https://seu-dominio.com/api/docs

# Testar endpoint específico
curl "https://seu-dominio.com/api/candles?symbol=BINANCE:BTCUSDT&timeframe=1h&limit=10"
```

---

## 🎉 Conclusão

Sua API TradingView está agora configurada para deploy no Easypanel!

**Próximos passos:**
1. ✅ Dockerfile na raiz
2. ✅ Variáveis de ambiente configuradas
3. ✅ Deploy no Easypanel
4. ✅ Testar endpoints
5. ✅ Configurar domínio personalizado

🚀 **Sua API está pronta para produção no Easypanel!**
