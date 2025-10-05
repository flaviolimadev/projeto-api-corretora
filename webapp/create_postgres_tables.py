"""
Criar tabelas PostgreSQL diretamente via psycopg2
Alternativa ao Prisma para conexões lentas
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import uuid
import json

# Configuração do banco PostgreSQL
DB_CONFIG = {
    'host': 'easypainel.ctrlser.com',
    'port': 5435,
    'database': 'corretora',
    'user': 'postgres',
    'password': '6b7215f9594dea0d0673',
    'sslmode': 'disable'
}

def create_tables():
    """Criar todas as tabelas no PostgreSQL"""
    print("=" * 70)
    print("CRIANDO TABELAS NO POSTGRESQL")
    print("=" * 70)
    print(f"Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print(f"Database: {DB_CONFIG['database']}")
    print()
    
    try:
        # Conectar ao banco
        print("Conectando ao PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        print("OK - Conectado ao PostgreSQL!")
        print()
        
        # 1. Criar tabela categories
        print("1. Criando tabela 'categories'...")
        cursor.execute("""
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
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS categories_key_idx ON categories(key);")
        print("OK - Tabela 'categories' criada!")
        
        # 2. Criar tabela assets
        print("2. Criando tabela 'assets'...")
        cursor.execute("""
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
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS assets_symbol_idx ON assets(symbol);")
        cursor.execute("CREATE INDEX IF NOT EXISTS assets_exchange_idx ON assets(exchange);")
        cursor.execute("CREATE INDEX IF NOT EXISTS assets_categoryKey_idx ON assets(\"categoryKey\");")
        cursor.execute("CREATE INDEX IF NOT EXISTS assets_isActive_idx ON assets(\"isActive\");")
        print("OK - Tabela 'assets' criada!")
        
        # 3. Criar tabela candles
        print("3. Criando tabela 'candles'...")
        cursor.execute("""
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
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS candles_symbol_timeframe_timestamp_idx ON candles(symbol, timeframe, timestamp);")
        cursor.execute("CREATE INDEX IF NOT EXISTS candles_assetId_timeframe_idx ON candles(\"assetId\", timeframe);")
        cursor.execute("CREATE INDEX IF NOT EXISTS candles_timestamp_idx ON candles(timestamp);")
        print("OK - Tabela 'candles' criada!")
        
        # 4. Criar tabela current_candles
        print("4. Criando tabela 'current_candles'...")
        cursor.execute("""
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
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS current_candles_symbol_idx ON current_candles(symbol);")
        cursor.execute("CREATE INDEX IF NOT EXISTS current_candles_lastUpdate_idx ON current_candles(\"lastUpdate\");")
        print("OK - Tabela 'current_candles' criada!")
        
        # 5. Criar tabela sync_logs
        print("5. Criando tabela 'sync_logs'...")
        cursor.execute("""
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
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS sync_logs_type_status_idx ON sync_logs(type, status);")
        cursor.execute("CREATE INDEX IF NOT EXISTS sync_logs_startedAt_idx ON sync_logs(\"startedAt\");")
        print("OK - Tabela 'sync_logs' criada!")
        
        # 6. Criar tabela configs
        print("6. Criando tabela 'configs'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS configs (
                id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                description TEXT,
                "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("OK - Tabela 'configs' criada!")
        
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
        
        # Inserir categorias iniciais
        print()
        print("Inserindo categorias iniciais...")
        categories_data = [
            ('forex', 'Forex', 'Moedas e pares de câmbio', '💱', ['FX_IDC', 'FXCM', 'OANDA'], ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']),
            ('crypto', 'Crypto', 'Criptomoedas e tokens digitais', '₿', ['BINANCE', 'COINBASE', 'KRAKEN', 'BITFINEX'], ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']),
            ('stocks', 'Stocks', 'Ações de empresas', '📈', ['NASDAQ', 'NYSE', 'AMEX', 'LSE'], ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']),
            ('indices', 'Indices', 'Índices de mercado', '📊', ['NASDAQ', 'NYSE', 'CBOE', 'CME'], ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']),
            ('commodities', 'Commodities', 'Mercadorias e matérias-primas', '🥇', ['COMEX', 'NYMEX', 'CBOT', 'LME'], ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']),
            ('bonds', 'Bonds', 'Títulos e obrigações', '🏛️', ['CBOT', 'EUREX', 'TSE'], ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']),
            ('etfs', 'ETFs', 'Fundos negociados em bolsa', '📦', ['NYSE', 'NASDAQ', 'AMEX'], ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']),
            ('futures', 'Futures', 'Contratos futuros', '⏰', ['CME', 'CBOT', 'NYMEX', 'COMEX', 'EUREX'], ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M'])
        ]
        
        for cat_data in categories_data:
            try:
                cursor.execute("""
                    INSERT INTO categories (key, name, description, icon, exchanges, timeframes)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (key) DO NOTHING;
                """, cat_data)
            except Exception as e:
                print(f"Erro ao inserir categoria {cat_data[0]}: {e}")
        
        print("OK - Categorias inseridas!")
        
        cursor.close()
        conn.close()
        
        print()
        print("=" * 70)
        print("TABELAS CRIADAS COM SUCESSO NO POSTGRESQL!")
        print("=" * 70)
        print()
        print("Próximos passos:")
        print("  1. python workers/sync_categories.py")
        print("  2. python workers/sync_assets.py")
        print("  3. prisma studio")
        print()
        
    except Exception as e:
        print(f"\nERRO: {e}")
        print()
        print("Verifique:")
        print("  - Conexao com internet")
        print("  - Credenciais do banco")
        print("  - Firewall/VPN")
        print("  - Servidor PostgreSQL ativo")
        return False
    
    return True


if __name__ == "__main__":
    # Instalar psycopg2 se necessário
    try:
        import psycopg2
    except ImportError:
        print("Instalando psycopg2-binary...")
        import subprocess
        subprocess.run(['pip', 'install', 'psycopg2-binary'], check=True)
        import psycopg2
    
    create_tables()
