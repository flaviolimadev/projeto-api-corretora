# 🚀 TradingView API - Guia de Deploy

Este guia completo mostra como colocar sua API TradingView online para funcionar como uma API para outras aplicações.

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Configuração Local](#configuração-local)
4. [Deploy com Docker](#deploy-com-docker)
5. [Deploy em Servidor](#deploy-em-servidor)
6. [Configuração de Domínio](#configuração-de-domínio)
7. [Monitoramento](#monitoramento)
8. [Troubleshooting](#troubleshooting)

## 🔧 Pré-requisitos

### Software Necessário
- **Docker** (versão 20.10+)
- **Docker Compose** (versão 2.0+)
- **Git** (para clonar o repositório)
- **Curl** (para testes)

### Servidor (VPS/Cloud)
- **RAM**: Mínimo 2GB (recomendado 4GB+)
- **CPU**: 2 cores (recomendado 4+ cores)
- **Disco**: 20GB+ de espaço livre
- **OS**: Ubuntu 20.04+ ou CentOS 8+

## 🏗️ Estrutura do Projeto

```
webapp/
├── 📁 api/                    # APIs principais
│   ├── app.py                 # API principal com WebSocket
│   └── api_database.py        # API do banco de dados
├── 📁 database/               # Gerenciamento do banco
│   └── postgres_manager.py    # Conexão PostgreSQL
├── 📁 workers/                # Workers de sincronização
│   └── main_worker.py         # Worker principal
├── 📁 static/                 # Arquivos estáticos
├── 📁 templates/              # Templates HTML
├── 🐳 Dockerfile              # Container da aplicação
├── 🐳 docker-compose.yml      # Orquestração dos serviços
├── ⚙️ nginx.conf              # Configuração do proxy
├── 📝 requirements.production.txt # Dependências produção
├── 🔧 .env.production         # Variáveis de ambiente
├── 🚀 deploy.sh               # Script de deploy (Linux/Mac)
├── 🚀 deploy.bat              # Script de deploy (Windows)
└── 📚 DEPLOY_GUIDE.md         # Este guia
```

## 🏠 Configuração Local

### 1. Clone o Repositório
```bash
git clone <seu-repositorio>
cd tradingview-scraper/webapp
```

### 2. Configure as Variáveis de Ambiente
```bash
# Copie o arquivo de exemplo
cp .env.production .env

# Edite as configurações
nano .env
```

**Configurações importantes:**
```env
# Database
DATABASE_URL="postgres://user:password@host:port/database"

# API
API_HOST=0.0.0.0
API_PORT=5000
SECRET_KEY="sua-chave-secreta-super-segura"

# Worker
WORKER_ENABLED=True
SYNC_INTERVAL_CANDLES=60
```

### 3. Teste Local
```bash
# Linux/Mac
chmod +x deploy.sh
./deploy.sh

# Windows
deploy.bat
```

## 🐳 Deploy com Docker

### Deploy Automático
```bash
# Execute o script de deploy
./deploy.sh
```

### Deploy Manual
```bash
# 1. Parar containers existentes
docker-compose down

# 2. Construir novas imagens
docker-compose build --no-cache

# 3. Iniciar serviços
docker-compose up -d

# 4. Verificar status
docker-compose ps
docker-compose logs -f
```

### Serviços Incluídos
- **API Principal** (porta 5000): API com WebSocket
- **API Database** (porta 5001): API do banco de dados
- **Nginx** (porta 80/443): Proxy reverso
- **Redis** (porta 6379): Cache
- **Worker**: Sincronização de dados

## 🌐 Deploy em Servidor

### 1. Preparar o Servidor
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
```

### 2. Configurar Firewall
```bash
# UFW (Ubuntu)
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable

# Ou iptables
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

### 3. Deploy da Aplicação
```bash
# Clonar repositório
git clone <seu-repositorio>
cd tradingview-scraper/webapp

# Configurar variáveis
cp .env.production .env
nano .env

# Deploy
./deploy.sh
```

### 4. Configurar Auto-start
```bash
# Criar serviço systemd
sudo nano /etc/systemd/system/tradingview-api.service
```

**Conteúdo do arquivo:**
```ini
[Unit]
Description=TradingView API
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/your/webapp
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

```bash
# Ativar serviço
sudo systemctl enable tradingview-api.service
sudo systemctl start tradingview-api.service
```

## 🌍 Configuração de Domínio

### 1. Configurar DNS
```
A    api.seudominio.com    -> IP_DO_SERVIDOR
A    www.seudominio.com    -> IP_DO_SERVIDOR
```

### 2. Configurar SSL (Let's Encrypt)
```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d api.seudominio.com -d www.seudominio.com

# Renovação automática
sudo crontab -e
# Adicionar: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 3. Atualizar Nginx
```bash
# Editar configuração
sudo nano nginx.conf

# Adicionar configuração SSL
server {
    listen 443 ssl http2;
    server_name api.seudominio.com;
    
    ssl_certificate /etc/letsencrypt/live/api.seudominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.seudominio.com/privkey.pem;
    
    # ... resto da configuração
}
```

## 📊 Monitoramento

### Endpoints de Monitoramento
```bash
# Health Check
curl http://seudominio.com/api/health

# Métricas detalhadas
curl http://seudominio.com/api/metrics

# Status dos serviços
curl http://seudominio.com/db/health
```

### Logs
```bash
# Ver logs em tempo real
docker-compose logs -f

# Logs específicos
docker-compose logs -f api
docker-compose logs -f db-api
docker-compose logs -f nginx
```

### Métricas do Sistema
```bash
# Uso de recursos
docker stats

# Espaço em disco
df -h

# Uso de memória
free -h
```

## 🔧 Troubleshooting

### Problemas Comuns

#### 1. Container não inicia
```bash
# Verificar logs
docker-compose logs api

# Verificar configuração
docker-compose config

# Reconstruir container
docker-compose build --no-cache api
```

#### 2. Erro de conexão com banco
```bash
# Testar conexão
docker-compose exec api python -c "
from database.postgres_manager import postgres_manager
print('Connected:', postgres_manager.connect())
"

# Verificar variáveis de ambiente
docker-compose exec api env | grep DATABASE
```

#### 3. Nginx não funciona
```bash
# Verificar configuração
nginx -t

# Recarregar configuração
docker-compose exec nginx nginx -s reload

# Verificar portas
netstat -tlnp | grep :80
```

#### 4. WebSocket não conecta
```bash
# Verificar se o serviço está rodando
curl -I http://localhost:5000/socket.io/

# Verificar logs do WebSocket
docker-compose logs -f api | grep socket
```

### Comandos Úteis

```bash
# Reiniciar todos os serviços
docker-compose restart

# Parar todos os serviços
docker-compose down

# Remover volumes (CUIDADO: apaga dados)
docker-compose down -v

# Backup do banco
docker-compose exec db pg_dump -U postgres database > backup.sql

# Restaurar backup
docker-compose exec -T db psql -U postgres database < backup.sql
```

## 📈 Escalabilidade

### Load Balancer
Para múltiplas instâncias, use um load balancer:

```yaml
# docker-compose.scale.yml
version: '3.8'
services:
  api:
    deploy:
      replicas: 3
  nginx:
    # Configurar upstream com múltiplas instâncias
```

### Cache Redis
O Redis já está configurado para cache. Para otimizar:

```bash
# Monitorar Redis
docker-compose exec redis redis-cli monitor

# Estatísticas
docker-compose exec redis redis-cli info stats
```

## 🔒 Segurança

### Configurações de Segurança
1. **Alterar senhas padrão**
2. **Configurar firewall**
3. **Usar HTTPS**
4. **Rate limiting** (já configurado no Nginx)
5. **Headers de segurança** (já configurado)

### Backup
```bash
# Script de backup automático
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec -T db pg_dump -U postgres database > "backup_$DATE.sql"
```

## 📞 Suporte

### Logs Importantes
- **Aplicação**: `docker-compose logs -f api`
- **Banco**: `docker-compose logs -f db-api`
- **Nginx**: `docker-compose logs -f nginx`
- **Worker**: `docker-compose logs -f worker`

### Endpoints de Diagnóstico
- Health Check: `/api/health`
- Métricas: `/api/metrics`
- Documentação: `/api/docs`
- Status do Banco: `/db/health`

---

## 🎉 Conclusão

Sua API TradingView está agora configurada para produção! 

**Endpoints principais:**
- `http://seudominio.com/api/candles` - Dados históricos
- `http://seudominio.com/api/current-candle` - Candle atual
- `http://seudominio.com/api/categories` - Categorias
- `http://seudominio.com/socket.io/` - WebSocket

**Para atualizações futuras:**
```bash
git pull
./deploy.sh
```

🚀 **Sua API está pronta para ser usada por outras aplicações!**
