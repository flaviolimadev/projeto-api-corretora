# 🔧 Troubleshooting - Database Connection

## ❌ **Erro: Can't reach database server**

### **Problema:**
```
Error: P1001: Can't reach database server at `localhost:51214`
```

Isso significa que o PostgreSQL não está rodando ou não está na porta esperada.

---

## 🔍 **Verificar PostgreSQL**

### **1. Verificar se está rodando:**
```powershell
# Verificar serviço PostgreSQL
Get-Service -Name "*postgres*"

# Verificar portas em uso
netstat -ano | findstr "5432"
netstat -ano | findstr "51214"
netstat -ano | findstr "51215"
```

### **2. Verificar qual porta PostgreSQL está usando:**
```powershell
# Procurar processos PostgreSQL
tasklist | findstr postgres

# Verificar conexões
netstat -ano | findstr LISTENING | findstr "5432"
```

---

## 🚀 **Soluções**

### **Solução 1: Usar PostgreSQL Padrão (Porta 5432)**

Se você tem PostgreSQL instalado localmente na porta padrão:

```env
# .env
DATABASE_URL="postgresql://postgres:suasenha@localhost:5432/trading_db?sslmode=disable"
```

Depois crie o banco:
```sql
CREATE DATABASE trading_db;
```

### **Solução 2: Usar Docker PostgreSQL**

Se preferir usar Docker:

```bash
# Iniciar PostgreSQL no Docker
docker run --name trading-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=trading_db \
  -p 5432:5432 \
  -d postgres:15

# Depois configure .env
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/trading_db?sslmode=disable"
```

### **Solução 3: Usar SQLite (Desenvolvimento)**

Para desenvolvimento rápido, use SQLite:

```prisma
// schema.prisma
datasource db {
  provider = "sqlite"
  url      = "file:./dev.db"
}
```

```bash
# Criar banco
prisma db push
```

### **Solução 4: Prisma Accelerate/Proxy**

Se você quer usar o Prisma Accelerate (cloud):

```bash
# Gerar com data proxy
prisma generate --data-proxy

# Use a URL original
DATABASE_URL="prisma+postgres://localhost:51213/..."
```

---

## 🔧 **Configuração Recomendada**

### **Para Desenvolvimento Local:**

1. **Instale PostgreSQL:**
   - Download: https://www.postgresql.org/download/windows/
   - Porta padrão: 5432
   - User: postgres
   - Password: postgres

2. **Crie o banco:**
   ```sql
   CREATE DATABASE trading_db;
   ```

3. **Configure .env:**
   ```env
   DATABASE_URL="postgresql://postgres:postgres@localhost:5432/trading_db?sslmode=disable"
   ```

4. **Execute:**
   ```bash
   prisma db push
   ```

---

## 📝 **Alternativas**

### **Opção A: SQLite (Mais Simples)**

**Vantagens:**
- ✅ Não precisa instalar PostgreSQL
- ✅ Arquivo local simples
- ✅ Perfeito para desenvolvimento

**Desvantagens:**
- ❌ Menos performático para produção
- ❌ Menos recursos avançados

**Como usar:**
```prisma
// schema.prisma
datasource db {
  provider = "sqlite"
  url      = "file:./trading.db"
}

generator client {
  provider = "prisma-client-py"
}
```

```bash
# Gerar e criar
prisma generate
prisma db push
```

### **Opção B: PostgreSQL Docker**

**Vantagens:**
- ✅ Isolado do sistema
- ✅ Fácil de resetar
- ✅ Compatível com produção

**Como usar:**
```bash
docker-compose up -d
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: trading_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### **Opção C: PostgreSQL Cloud**

**Provedores gratuitos:**
- Supabase: https://supabase.com
- Railway: https://railway.app
- Neon: https://neon.tech

---

## ✅ **Testar Conexão**

### **Python:**
```python
import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="trading_db",
        user="postgres",
        password="postgres"
    )
    print("✅ Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"❌ Erro: {e}")
```

### **PowerShell:**
```powershell
# Testar conexão com psql
psql -h localhost -p 5432 -U postgres -d trading_db
```

---

## 🎯 **Recomendação Final**

**Para começar rapidamente, use SQLite:**

1. Edite `prisma/schema.prisma`:
   ```prisma
   datasource db {
     provider = "sqlite"
     url      = "file:./trading.db"
   }
   ```

2. Execute:
   ```bash
   prisma generate
   prisma db push
   ```

3. Pronto! Banco criado em `trading.db`

**Quando estiver pronto para produção, migre para PostgreSQL.**

---

## 📞 **Precisa de Ajuda?**

Me diga:
1. Você tem PostgreSQL instalado?
2. Prefere usar SQLite por enquanto?
3. Quer usar Docker?

Vou ajustar a configuração de acordo! 🚀

