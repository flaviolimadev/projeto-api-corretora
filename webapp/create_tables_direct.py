"""
Criar tabelas diretamente via psycopg2 (mais rápido para conexões remotas)
"""

import asyncio
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Configuração do banco
DB_CONFIG = {
    'host': 'easypainel.ctrlser.com',
    'port': 5434,
    'database': 'api-corretora',
    'user': 'postgres',
    'password': '98b4306b2302c1c00a06',
    'sslmode': 'disable'
}

# SQL para cada tabela (executado separadamente)
TABLES = {
    'categories': """
        CREATE TABLE IF NOT EXISTS categories (
            id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
            key TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            icon TEXT NOT NULL,
            exchanges TEXT[] NOT NULL,
            timeframes TEXT[] NOT NULL,
            "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS categories_key_idx ON categories(key);
    """,
    
    'assets': """
        CREATE TABLE IF NOT EXISTS assets (
            id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
            symbol TEXT UNIQUE NOT NULL,
            exchange TEXT NOT NULL,
            ticker TEXT NOT NULL,
            description TEXT NOT NULL,
            type TEXT NOT NULL,
            "categoryKey" TEXT NOT NULL,
            "searchQuery" TEXT,
            "isActive" BOOLEAN NOT NULL DEFAULT TRUE,
            "lastUpdate" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY ("categoryKey") REFERENCES categories(key) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS assets_symbol_idx ON assets(symbol);
        CREATE INDEX IF NOT EXISTS assets_exchange_idx ON assets(exchange);
        CREATE INDEX IF NOT EXISTS assets_categoryKey_idx ON assets("categoryKey");
        CREATE INDEX IF NOT EXISTS assets_isActive_idx ON assets("isActive");
    """,
    
    'candles': """
        CREATE TABLE IF NOT EXISTS candles (
            id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
            "assetId" TEXT NOT NULL,
            symbol TEXT NOT NULL,
            timeframe TEXT NOT NULL,
            timestamp BIGINT NOT NULL,
            datetime TIMESTAMP NOT NULL,
            open DOUBLE PRECISION NOT NULL,
            high DOUBLE PRECISION NOT NULL,
            low DOUBLE PRECISION NOT NULL,
            close DOUBLE PRECISION NOT NULL,
            volume DOUBLE PRECISION NOT NULL,
            "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY ("assetId") REFERENCES assets(id) ON DELETE CASCADE,
            UNIQUE ("assetId", timeframe, timestamp)
        );
        CREATE INDEX IF NOT EXISTS candles_symbol_timeframe_timestamp_idx ON candles(symbol, timeframe, timestamp);
        CREATE INDEX IF NOT EXISTS candles_assetId_timeframe_idx ON candles("assetId", timeframe);
        CREATE INDEX IF NOT EXISTS candles_timestamp_idx ON candles(timestamp);
    """,
    
    'current_candles': """
        CREATE TABLE IF NOT EXISTS current_candles (
            id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
            "assetId" TEXT UNIQUE NOT NULL,
            symbol TEXT UNIQUE NOT NULL,
            timeframe TEXT NOT NULL,
            timestamp BIGINT NOT NULL,
            datetime TIMESTAMP NOT NULL,
            open DOUBLE PRECISION NOT NULL,
            high DOUBLE PRECISION NOT NULL,
            low DOUBLE PRECISION NOT NULL,
            close DOUBLE PRECISION NOT NULL,
            volume DOUBLE PRECISION NOT NULL,
            "priceChange" DOUBLE PRECISION NOT NULL,
            "priceChangePercent" DOUBLE PRECISION NOT NULL,
            "isPositive" BOOLEAN NOT NULL,
            "lastUpdate" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY ("assetId") REFERENCES assets(id) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS current_candles_symbol_idx ON current_candles(symbol);
        CREATE INDEX IF NOT EXISTS current_candles_lastUpdate_idx ON current_candles("lastUpdate");
    """,
    
    'sync_logs': """
        CREATE TABLE IF NOT EXISTS sync_logs (
            id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
            type TEXT NOT NULL,
            status TEXT NOT NULL,
            "itemsCount" INTEGER NOT NULL DEFAULT 0,
            "errorMsg" TEXT,
            duration DOUBLE PRECISION,
            "startedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "finishedAt" TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS sync_logs_type_status_idx ON sync_logs(type, status);
        CREATE INDEX IF NOT EXISTS sync_logs_startedAt_idx ON sync_logs("startedAt");
    """,
    
    'configs': """
        CREATE TABLE IF NOT EXISTS configs (
            id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
            key TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL,
            description TEXT,
            "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """
}


def create_tables():
    """Criar todas as tabelas"""
    print("=" * 60)
    print("CRIANDO TABELAS NO POSTGRESQL")
    print("=" * 60)
    print(f"Host: {DB_CONFIG['host']}")
    print(f"Database: {DB_CONFIG['database']}")
    print()
    
    try:
        # Conectar ao banco
        print("Conectando ao banco de dados...")
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        print("OK - Conectado!")
        print()
        
        # Criar cada tabela
        for table_name, sql in TABLES.items():
            try:
                print(f"Criando tabela '{table_name}'...")
                cursor.execute(sql)
                print(f"OK - Tabela '{table_name}' criada!")
            except Exception as e:
                print(f"ERRO ao criar '{table_name}': {e}")
        
        # Verificar tabelas criadas
        print()
        print("Verificando tabelas criadas...")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print(f"\nOK - {len(tables)} tabelas encontradas:")
        for table in tables:
            print(f"   - {table[0]}")
        
        cursor.close()
        conn.close()
        
        print()
        print("=" * 60)
        print("TABELAS CRIADAS COM SUCESSO!")
        print("=" * 60)
        print()
        print("Próximos passos:")
        print("  1. python workers/sync_categories.py")
        print("  2. prisma studio")
        print()
        
    except Exception as e:
        print(f"\nERRO: {e}")
        print()
        print("Verifique:")
        print("  - Conexao com internet")
        print("  - Credenciais do banco")
        print("  - Firewall/VPN")
        return False
    
    return True


if __name__ == "__main__":
    # Instalar psycopg2 se necessário
    try:
        import psycopg2
    except ImportError:
        print("Instalando psycopg2...")
        import subprocess
        subprocess.run(['pip', 'install', 'psycopg2-binary'], check=True)
        import psycopg2
    
    create_tables()
