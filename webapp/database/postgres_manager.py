"""
Database Manager alternativo para PostgreSQL
Funciona diretamente com psycopg2, sem Prisma
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)

class PostgreSQLManager:
    """Gerenciador de banco PostgreSQL direto"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        
        # Configuração do banco
        self.db_config = {
            'host': 'easypainel.ctrlser.com',
            'port': 5435,
            'database': 'corretora',
            'user': 'postgres',
            'password': '6b7215f9594dea0d0673',
            'sslmode': 'disable'
        }
    
    def connect(self):
        """Conectar ao banco"""
        try:
            # Se já está conectado, retornar True
            if self.connection and not self.connection.closed:
                return True
            
            self.connection = psycopg2.connect(**self.db_config)
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            logger.info("Connected to PostgreSQL database")
            return True
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        """Desconectar do banco"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            logger.info("Disconnected from database")
        except Exception as e:
            logger.error(f"Error disconnecting: {e}")

    def commit(self):
        """Commitar transação"""
        if self.connection:
            self.connection.commit()

    def rollback(self):
        """Rollback transação"""
        if self.connection:
            self.connection.rollback()
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Executar query e retornar resultados"""
        try:
            # Verificar se a conexão está ativa
            if not self.connection or self.connection.closed:
                logger.warning("Connection is closed, reconnecting...")
                self.connect()
            
            self.cursor.execute(query, params)
            if query.strip().upper().startswith('SELECT'):
                return [dict(row) for row in self.cursor.fetchall()]
            else:
                self.connection.commit()
                return []
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            if self.connection and not self.connection.closed:
                self.connection.rollback()
            return []
    
    # ===== CATEGORIES =====
    
    def get_all_categories(self) -> List[Dict]:
        """Obter todas as categorias"""
        query = "SELECT * FROM categories ORDER BY name"
        return self.execute_query(query)
    
    def get_category_by_key(self, key: str) -> Optional[Dict]:
        """Obter categoria por chave"""
        query = "SELECT * FROM categories WHERE key = %s"
        results = self.execute_query(query, (key,))
        return results[0] if results else None
    
    def create_category(self, category_data: Dict) -> bool:
        """Criar nova categoria"""
        query = """
            INSERT INTO categories (key, name, description, icon, exchanges, timeframes)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (key) DO UPDATE SET
                name = EXCLUDED.name,
                description = EXCLUDED.description,
                icon = EXCLUDED.icon,
                exchanges = EXCLUDED.exchanges,
                timeframes = EXCLUDED.timeframes,
                "updatedAt" = CURRENT_TIMESTAMP
        """
        params = (
            category_data['key'],
            category_data['name'],
            category_data['description'],
            category_data['icon'],
            category_data['exchanges'],
            category_data['timeframes']
        )
        self.execute_query(query, params)
        return True
    
    # ===== ASSETS =====
    
    def get_all_assets(self, limit: int = 100) -> List[Dict]:
        """Obter todos os ativos"""
        query = "SELECT * FROM assets ORDER BY symbol LIMIT %s"
        return self.execute_query(query, (limit,))
    
    def get_active_assets(self, limit: int = 100) -> List[Dict]:
        """Obter apenas ativos ativos (isActive = true)"""
        query = "SELECT * FROM assets WHERE \"isActive\" = true ORDER BY symbol LIMIT %s"
        return self.execute_query(query, (limit,))
    
    def get_assets_by_category(self, category_key: str) -> List[Dict]:
        """Obter ativos por categoria"""
        query = "SELECT * FROM assets WHERE \"categoryKey\" = %s ORDER BY symbol"
        return self.execute_query(query, (category_key,))
    
    def get_asset_by_symbol(self, symbol: str) -> Optional[Dict]:
        """Obter ativo por símbolo"""
        query = "SELECT * FROM assets WHERE symbol = %s"
        results = self.execute_query(query, (symbol,))
        return results[0] if results else None
    
    def create_asset(self, asset_data: Dict) -> bool:
        """Criar novo ativo"""
        query = """
            INSERT INTO assets (symbol, exchange, ticker, description, type, "categoryKey", "searchQuery")
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (symbol) DO UPDATE SET
                exchange = EXCLUDED.exchange,
                ticker = EXCLUDED.ticker,
                description = EXCLUDED.description,
                type = EXCLUDED.type,
                "categoryKey" = EXCLUDED."categoryKey",
                "searchQuery" = EXCLUDED."searchQuery",
                "lastUpdate" = CURRENT_TIMESTAMP,
                "updatedAt" = CURRENT_TIMESTAMP
        """
        params = (
            asset_data['symbol'],
            asset_data['exchange'],
            asset_data['ticker'],
            asset_data['description'],
            asset_data['type'],
            asset_data['categoryKey'],
            asset_data.get('searchQuery')
        )
        self.execute_query(query, params)
        return True
    
    # ===== CANDLES =====
    
    def get_candles(self, symbol: str, timeframe: str, limit: int = 1000) -> List[Dict]:
        """Obter candles históricos"""
        query = """
            SELECT * FROM candles 
            WHERE symbol = %s AND timeframe = %s 
            ORDER BY timestamp DESC 
            LIMIT %s
        """
        return self.execute_query(query, (symbol, timeframe, limit))
    
    def create_candle(self, candle_data: Dict) -> bool:
        """Criar novo candle"""
        query = """
            INSERT INTO candles ("assetId", symbol, timeframe, timestamp, datetime, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT ("assetId", timeframe, timestamp) DO UPDATE SET
                datetime = EXCLUDED.datetime,
                open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low,
                close = EXCLUDED.close,
                volume = EXCLUDED.volume
        """
        params = (
            candle_data['assetId'],
            candle_data['symbol'],
            candle_data['timeframe'],
            candle_data['timestamp'],
            candle_data['datetime'],
            candle_data['open'],
            candle_data['high'],
            candle_data['low'],
            candle_data['close'],
            candle_data['volume']
        )
        self.execute_query(query, params)
        return True
    
    # ===== CURRENT CANDLES =====
    
    def get_all_current_candles(self) -> List[Dict]:
        """Obter todos os candles atuais"""
        query = "SELECT * FROM current_candles ORDER BY \"lastUpdate\" DESC"
        return self.execute_query(query)
    
    def get_current_candle(self, symbol: str) -> Optional[Dict]:
        """Obter candle atual por símbolo"""
        query = "SELECT * FROM current_candles WHERE symbol = %s"
        results = self.execute_query(query, (symbol,))
        return results[0] if results else None
    
    def get_candle_by_timestamp(self, asset_id: str, timeframe: str, timestamp: int) -> Optional[Dict]:
        """Buscar candle por asset ID, timeframe e timestamp"""
        query = "SELECT * FROM candles WHERE \"assetId\" = %s AND timeframe = %s AND timestamp = %s"
        results = self.execute_query(query, (asset_id, timeframe, timestamp))
        return results[0] if results else None
    
    def get_current_candle_by_asset_id(self, asset_id: str) -> Optional[Dict]:
        """Buscar candle atual por asset ID"""
        query = "SELECT * FROM current_candles WHERE \"assetId\" = %s"
        results = self.execute_query(query, (asset_id,))
        return results[0] if results else None
    
    def get_current_candle_by_symbol(self, symbol: str) -> Optional[Dict]:
        """Buscar candle atual por símbolo"""
        query = "SELECT * FROM current_candles WHERE symbol = %s"
        results = self.execute_query(query, (symbol,))
        return results[0] if results else None
    
    def create_current_candle(self, candle_data: Dict) -> bool:
        """Criar novo candle atual"""
        query = """
            INSERT INTO current_candles ("assetId", symbol, timeframe, timestamp, datetime, open, high, low, close, volume, "priceChange", "priceChangePercent", "isPositive")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            candle_data['assetId'],
            candle_data['symbol'],
            candle_data['timeframe'],
            candle_data['timestamp'],
            candle_data['datetime'],
            candle_data['open'],
            candle_data['high'],
            candle_data['low'],
            candle_data['close'],
            candle_data['volume'],
            candle_data['priceChange'],
            candle_data['priceChangePercent'],
            candle_data['isPositive']
        )
        self.execute_query(query, params)
        return True
    
    def update_current_candle(self, asset_id: str, candle_data: Dict) -> bool:
        """Atualizar candle atual por asset ID"""
        query = """
            UPDATE current_candles SET
                symbol = %s,
                timeframe = %s,
                timestamp = %s,
                datetime = %s,
                open = %s,
                high = %s,
                low = %s,
                close = %s,
                volume = %s,
                "priceChange" = %s,
                "priceChangePercent" = %s,
                "isPositive" = %s,
                "lastUpdate" = CURRENT_TIMESTAMP,
                "updatedAt" = CURRENT_TIMESTAMP
            WHERE "assetId" = %s
        """
        params = (
            candle_data['symbol'],
            candle_data['timeframe'],
            candle_data['timestamp'],
            candle_data['datetime'],
            candle_data['open'],
            candle_data['high'],
            candle_data['low'],
            candle_data['close'],
            candle_data['volume'],
            candle_data['priceChange'],
            candle_data['priceChangePercent'],
            candle_data['isPositive'],
            asset_id
        )
        self.execute_query(query, params)
        return True
    
    # ===== SYNC LOGS =====
    
    def create_sync_log(self, log_data: Dict) -> bool:
        """Criar log de sincronização"""
        query = """
            INSERT INTO sync_logs (type, status, "itemsCount", "errorMsg", duration, "startedAt", "finishedAt")
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            log_data['type'],
            log_data['status'],
            log_data.get('itemsCount', 0),
            log_data.get('errorMsg'),
            log_data.get('duration'),
            log_data['startedAt'],
            log_data.get('finishedAt')
        )
        self.execute_query(query, params)
        return True
    
    def get_recent_sync_logs(self, limit: int = 10) -> List[Dict]:
        """Obter logs recentes de sincronização"""
        query = "SELECT * FROM sync_logs ORDER BY \"startedAt\" DESC LIMIT %s"
        return self.execute_query(query, (limit,))
    
    # ===== CONFIGS =====
    
    def get_config(self, key: str) -> Optional[str]:
        """Obter configuração"""
        query = "SELECT value FROM configs WHERE key = %s"
        results = self.execute_query(query, (key,))
        return results[0]['value'] if results else None
    
    def set_config(self, key: str, value: str, description: str = None) -> bool:
        """Definir configuração"""
        query = """
            INSERT INTO configs (key, value, description)
            VALUES (%s, %s, %s)
            ON CONFLICT (key) DO UPDATE SET
                value = EXCLUDED.value,
                description = EXCLUDED.description,
                "updatedAt" = CURRENT_TIMESTAMP
        """
        self.execute_query(query, (key, value, description))
        return True


# Instância global
postgres_manager = PostgreSQLManager()
