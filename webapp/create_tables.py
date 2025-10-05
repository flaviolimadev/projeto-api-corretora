"""
Script para criar tabelas diretamente via SQL
Mais rápido que prisma db push para conexões remotas
"""

import asyncio
import logging
from prisma import Prisma

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# SQL para criar todas as tabelas
CREATE_TABLES_SQL = """
-- Tabela de Categorias
CREATE TABLE IF NOT EXISTS categories (
    id TEXT PRIMARY KEY,
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

-- Tabela de Ativos
CREATE TABLE IF NOT EXISTS assets (
    id TEXT PRIMARY KEY,
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

-- Tabela de Candles (Histórico)
CREATE TABLE IF NOT EXISTS candles (
    id TEXT PRIMARY KEY,
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

-- Tabela de Candle Atual
CREATE TABLE IF NOT EXISTS current_candles (
    id TEXT PRIMARY KEY,
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

-- Tabela de Logs de Sincronização
CREATE TABLE IF NOT EXISTS sync_logs (
    id TEXT PRIMARY KEY,
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

-- Tabela de Configurações
CREATE TABLE IF NOT EXISTS configs (
    id TEXT PRIMARY KEY,
    key TEXT UNIQUE NOT NULL,
    value TEXT NOT NULL,
    description TEXT,
    "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


async def create_tables():
    """Criar tabelas no banco de dados"""
    db = Prisma()
    
    try:
        logger.info("Conectando ao banco de dados...")
        await db.connect()
        logger.info("✅ Conectado!")
        
        logger.info("Criando tabelas...")
        
        # Executar SQL diretamente
        await db.execute_raw(CREATE_TABLES_SQL)
        
        logger.info("✅ Tabelas criadas com sucesso!")
        logger.info("")
        logger.info("Tabelas criadas:")
        logger.info("  1. categories")
        logger.info("  2. assets")
        logger.info("  3. candles")
        logger.info("  4. current_candles")
        logger.info("  5. sync_logs")
        logger.info("  6. configs")
        logger.info("")
        logger.info("Próximos passos:")
        logger.info("  python workers/sync_categories.py")
        
        await db.disconnect()
        logger.info("Desconectado do banco")
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar tabelas: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(create_tables())
