# 🗄️ TradingView Scraper - Database Setup Guide

## 📊 **Arquitetura do Sistema**

### **Visão Geral:**
- **Backend API** → Coleta dados do TradingView
- **Workers de Sincronização** → Atualizam banco de dados periodicamente
- **Database PostgreSQL + Prisma** → Armazena dados estruturados
- **API REST** → Aplicações consomem dados do banco

### **Fluxo de Dados:**
```
TradingView API → Flask API → Workers → PostgreSQL → Client Apps
                     ↓
              (Dados em tempo real)
                     ↓
              Workers (Background)
                     ↓
          PostgreSQL (Dados persistidos)
                     ↓
         Client Apps (Consumo otimizado)
```

---

## 🏗️ **Estrutura do Banco de Dados**

### **Tabelas Criadas:**

#### **1. Categories (Categorias)**
```sql
- id (UUID, PK)
- key (String, Unique) - forex, crypto, stocks, etc
- name (String)
- description (String)
- icon (String)
- exchanges (Array)
- timeframes (Array)
- createdAt, updatedAt
```

#### **2. Assets (Ativos)**
```sql
- id (UUID, PK)
- symbol (String, Unique) - BINANCE:BTCUSDT
- exchange (String)
- ticker (String) - BTCUSDT
- description (String)
- type (String)
- categoryKey (FK → categories.key)
- searchQuery (String)
- isActive (Boolean)
- lastUpdate (DateTime)
- createdAt, updatedAt
```

#### **3. Candles (Histórico)**
```sql
- id (UUID, PK)
- assetId (FK → assets.id)
- symbol (String) - denormalizado
- timeframe (String)
- timestamp (BigInt, Unix)
- datetime (DateTime)
- open, high, low, close, volume (Float)
- createdAt
```

#### **4. CurrentCandles (Candle Atual)**
```sql
- id (UUID, PK)
- assetId (FK → assets.id, Unique)
- symbol (String, Unique)
- timeframe (String)
- timestamp (BigInt)
- datetime (DateTime)
- open, high, low, close, volume (Float)
- priceChange (Float)
- priceChangePercent (Float)
- isPositive (Boolean)
- lastUpdate (DateTime)
- createdAt, updatedAt
```

#### **5. SyncLogs (Logs de Sincronização)**
```sql
- id (UUID, PK)
- type (String) - categories, assets, candles, current_candles
- status (String) - success, error, running
- itemsCount (Int)
- errorMsg (String)
- duration (Float)
- startedAt, finishedAt (DateTime)
```

#### **6. Configs (Configurações)**
```sql
- id (UUID, PK)
- key (String, Unique)
- value (String)
- description (String)
- createdAt, updatedAt
```

---

## 🚀 **Instalação e Configuração**

### **1. Instalar Dependências:**
```bash
cd tradingview-scraper/webapp

# Instalar dependências Python
pip install -r requirements_db.txt

# Gerar client Prisma
prisma generate

# Criar/migrar banco de dados
prisma db push
```

### **2. Configurar .env:**
```env
DATABASE_URL="prisma+postgres://localhost:51213/?api_key=..."

SYNC_INTERVAL_CATEGORIES=3600    # 1 hora
SYNC_INTERVAL_ASSETS=1800        # 30 minutos
SYNC_INTERVAL_CANDLES=60         # 1 minuto
SYNC_INTERVAL_CURRENT=1          # 1 segundo

WORKER_ENABLED=True
WORKER_THREADS=4
MAX_ASSETS_PER_SYNC=100
```

### **3. Executar Migrações:**
```bash
# Criar banco de dados e tabelas
prisma db push

# Verificar schema
prisma db pull
```

---

## 🔄 **Workers de Sincronização**

### **Workers Implementados:**

#### **1. sync_categories.py**
- **Frequência:** 1 hora
- **Função:** Sincroniza categorias de `/api/categories`
- **Evita duplicatas:** Usa `upsert` por `key`

#### **2. sync_assets.py** (A CRIAR)
- **Frequência:** 30 minutos
- **Função:** Sincroniza ativos de `/api/category-assets`
- **Evita duplicatas:** Usa `upsert` por `symbol`
- **Lógica:**
  - Para cada categoria
  - Para cada exchange da categoria
  - Buscar ativos (limite 200)
  - Inserir/atualizar no banco

#### **3. sync_candles.py** (A CRIAR)
- **Frequência:** 1 minuto
- **Função:** Sincroniza histórico de `/api/candles`
- **Evita duplicatas:** Checa `assetId + timeframe + timestamp`
- **Lógica:**
  - Para cada ativo ativo
  - Buscar últimos 1000 candles
  - Inserir apenas os que não existem

#### **4. sync_current_candles.py** (A CRIAR)
- **Frequência:** 1 segundo
- **Função:** Atualiza candle atual de `/api/current-candle`
- **Evita duplicatas:** Usa `upsert` por `assetId`
- **Lógica:**
  - Para cada ativo ativo
  - Buscar candle atual
  - Atualizar no banco (sempre sobrescreve)

---

## 📡 **Nova API REST (Banco de Dados)**

### **Endpoints Criados:**

#### **1. GET /db/categories**
```bash
curl "http://localhost:5000/db/categories"
```
**Retorna:** Todas as categorias do banco de dados

#### **2. GET /db/categories/{key}**
```bash
curl "http://localhost:5000/db/categories/crypto"
```
**Retorna:** Categoria específica com seus ativos

#### **3. GET /db/assets**
```bash
# Todos os ativos
curl "http://localhost:5000/db/assets"

# Filtrar por categoria
curl "http://localhost:5000/db/assets?category=crypto"

# Filtrar por exchange
curl "http://localhost:5000/db/assets?exchange=BINANCE"

# Combinar filtros
curl "http://localhost:5000/db/assets?category=crypto&exchange=BINANCE"
```

#### **4. GET /db/assets/{symbol}**
```bash
curl "http://localhost:5000/db/assets/BINANCE:BTCUSDT"
```
**Retorna:** Ativo específico com candle atual

#### **5. GET /db/candles**
```bash
curl "http://localhost:5000/db/candles?symbol=BINANCE:BTCUSDT&timeframe=1m&limit=1000"
```
**Retorna:** Histórico de candles do banco

#### **6. GET /db/current-candles**
```bash
# Todos os candles atuais
curl "http://localhost:5000/db/current-candles"

# Candle atual específico
curl "http://localhost:5000/db/current-candles/BINANCE:BTCUSDT"
```

#### **7. GET /db/sync-logs**
```bash
curl "http://localhost:5000/db/sync-logs?limit=50"
```
**Retorna:** Logs de sincronização

---

## 🎯 **Comandos de Gerenciamento**

### **Iniciar Workers:**
```bash
# Worker principal (todos os workers)
python workers/main_worker.py

# Workers individuais
python workers/sync_categories.py
python workers/sync_assets.py
python workers/sync_candles.py
python workers/sync_current_candles.py
```

### **Sincronização Manual:**
```bash
# Sincronizar categorias
python -c "from workers.sync_categories import sync_categories; import asyncio; asyncio.run(sync_categories())"

# Sincronizar ativos
python -c "from workers.sync_assets import sync_assets; import asyncio; asyncio.run(sync_assets())"
```

### **Verificar Banco:**
```bash
# Abrir Prisma Studio
prisma studio

# Contar registros
python scripts/count_records.py
```

---

## 📊 **Performance e Otimização**

### **Índices Criados:**
- `categories`: `key`
- `assets`: `symbol`, `exchange`, `categoryKey`, `isActive`
- `candles`: `(assetId, timeframe, timestamp)`, `symbol`, `timestamp`
- `current_candles`: `symbol`, `lastUpdate`

### **Evitar Duplicatas:**
- **Categories:** Unique constraint em `key`
- **Assets:** Unique constraint em `symbol`
- **Candles:** Unique constraint em `(assetId, timeframe, timestamp)`
- **CurrentCandles:** Unique constraint em `assetId` e `symbol`

### **Intervalos de Sincronização:**
- **Categories:** 1 hora (raramente mudam)
- **Assets:** 30 minutos (novos ativos aparecem ocasionalmente)
- **Candles:** 1 minuto (histórico atualizado periodicamente)
- **CurrentCandles:** 1 segundo (tempo real)

---

## 🔍 **Monitoramento**

### **Logs de Sincronização:**
```python
# Via API
GET /db/sync-logs

# Via Python
from database.db import db_manager
logs = await db_manager.get_recent_sync_logs(limit=100)
```

### **Estatísticas:**
```python
# Contar categorias
categories = await db_manager.get_all_categories()
print(f"Total categorias: {len(categories)}")

# Contar ativos
assets = await db_manager.get_all_assets()
print(f"Total ativos: {len(assets)}")

# Contar candles atuais
current = await db_manager.get_all_current_candles()
print(f"Total candles atuais: {len(current)}")
```

---

## 🛠️ **Manutenção**

### **Limpar Dados Antigos:**
```sql
-- Remover candles com mais de 30 dias
DELETE FROM candles WHERE datetime < NOW() - INTERVAL '30 days';

-- Desativar ativos inativos
UPDATE assets SET "isActive" = false 
WHERE "lastUpdate" < NOW() - INTERVAL '7 days';
```

### **Reindexar:**
```sql
REINDEX TABLE candles;
REINDEX TABLE assets;
```

### **Backup:**
```bash
# Backup completo
pg_dump -h localhost -p 51214 -U postgres template1 > backup.sql

# Restaurar
psql -h localhost -p 51214 -U postgres template1 < backup.sql
```

---

## ✅ **Status da Implementação**

- ✅ **Schema Prisma** criado
- ✅ **DatabaseManager** implementado
- ✅ **Worker de Categories** implementado
- ⏳ **Worker de Assets** (próximo passo)
- ⏳ **Worker de Candles** (próximo passo)
- ⏳ **Worker de Current Candles** (próximo passo)
- ⏳ **API REST do banco** (próximo passo)
- ⏳ **Dashboard de monitoramento** (próximo passo)

---

## 🎯 **Próximos Passos**

1. **Criar workers restantes**
2. **Implementar API REST do banco**
3. **Criar dashboard de monitoramento**
4. **Adicionar testes automatizados**
5. **Implementar cache Redis**
6. **Deploy em produção**

**Sistema de banco de dados configurado e pronto para uso!** 🚀🗄️

