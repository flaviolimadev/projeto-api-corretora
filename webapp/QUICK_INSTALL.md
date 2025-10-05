# ⚡ Instalação Rápida - Database System

## 🚀 **Passo a Passo (5 minutos)**

### **1. Instalar Prisma (✅ JÁ FEITO!)**
```bash
pip install prisma python-dotenv aiohttp APScheduler python-dateutil
```

### **2. Gerar Prisma Client**
```bash
cd tradingview-scraper/webapp
prisma generate
```

### **3. Criar Banco de Dados**
```bash
prisma db push
```

### **4. Testar Conexão**
```python
python -c "from database.db import db_manager; import asyncio; asyncio.run(db_manager.connect()); print('✅ Conectado!')"
```

### **5. Primeira Sincronização**
```bash
# Sincronizar categorias
python workers/sync_categories.py
```

---

## 📊 **Resultado Esperado**

Após executar `prisma db push`, você deverá ver:
```
✔ Created table "categories"
✔ Created table "assets"
✔ Created table "candles"
✔ Created table "current_candles"
✔ Created table "sync_logs"
✔ Created table "configs"

✔ Generated Prisma Client Python
```

---

## 🔍 **Verificar Banco**

### **Abrir Prisma Studio (Interface Visual):**
```bash
prisma studio
```

Isso abrirá uma interface web em `http://localhost:5555` onde você pode ver todas as tabelas e dados.

### **Verificar via Python:**
```python
from database.db import db_manager
import asyncio

async def check():
    await db_manager.connect()
    
    # Verificar categorias
    categories = await db_manager.get_all_categories()
    print(f"Categorias: {len(categories)}")
    
    # Verificar ativos
    assets = await db_manager.get_all_assets()
    print(f"Ativos: {len(assets)}")
    
    await db_manager.disconnect()

asyncio.run(check())
```

---

## ⚠️ **Problemas Comuns**

### **Erro: "prisma command not found"**
```bash
# Reinstalar Prisma
pip uninstall prisma
pip install prisma
```

### **Erro: "DATABASE_URL not set"**
Verifique se o arquivo `.env` existe em `tradingview-scraper/webapp/.env`

### **Erro: "Cannot connect to database"**
Verifique se o PostgreSQL está rodando:
- Porta: 51214
- Database: template1
- User: postgres
- Password: postgres

---

## 📝 **Próximos Passos**

Após instalação bem-sucedida:

1. **Sincronizar dados:**
   ```bash
   python workers/sync_categories.py
   ```

2. **Criar workers restantes** (vou criar para você)

3. **Iniciar API do banco** (vou criar para você)

4. **Dashboard de monitoramento** (opcional)

---

## 🎯 **Comandos Úteis**

```bash
# Gerar client Prisma
prisma generate

# Criar/atualizar banco
prisma db push

# Abrir interface visual
prisma studio

# Ver schema atual
prisma db pull

# Resetar banco (CUIDADO!)
prisma db push --force-reset
```

---

## ✅ **Status da Instalação**

- ✅ Prisma instalado
- ⏳ Gerar client (`prisma generate`)
- ⏳ Criar banco (`prisma db push`)
- ⏳ Testar conexão
- ⏳ Primeira sincronização

**Execute os comandos acima nesta ordem!** 🚀
