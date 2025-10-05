"""
Database Manager using Prisma
"""

import os
import asyncio
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from prisma import Prisma
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manager for database operations"""
    
    def __init__(self):
        self.db: Optional[Prisma] = None
        self.is_connected = False
    
    async def connect(self):
        """Connect to database"""
        if self.is_connected:
            return
        
        try:
            self.db = Prisma()
            await self.db.connect()
            self.is_connected = True
            logger.info("✅ Connected to database")
        except Exception as e:
            logger.error(f"❌ Error connecting to database: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from database"""
        if self.db and self.is_connected:
            await self.db.disconnect()
            self.is_connected = False
            logger.info("Disconnected from database")
    
    # ==================== CATEGORIES ====================
    
    async def upsert_category(self, category_data: Dict[str, Any]) -> Any:
        """Insert or update category"""
        try:
            return await self.db.category.upsert(
                where={'key': category_data['key']},
                data={
                    'create': category_data,
                    'update': {
                        'name': category_data['name'],
                        'description': category_data['description'],
                        'icon': category_data['icon'],
                        'exchanges': category_data['exchanges'],
                        'timeframes': category_data['timeframes']
                    }
                }
            )
        except Exception as e:
            logger.error(f"Error upserting category {category_data.get('key')}: {e}")
            raise
    
    async def get_all_categories(self) -> List[Any]:
        """Get all categories"""
        try:
            return await self.db.category.find_many(
                order={'name': 'asc'}
            )
        except Exception as e:
            logger.error(f"Error getting categories: {e}")
            return []
    
    async def get_category(self, key: str) -> Optional[Any]:
        """Get category by key"""
        try:
            return await self.db.category.find_unique(
                where={'key': key},
                include={'assets': True}
            )
        except Exception as e:
            logger.error(f"Error getting category {key}: {e}")
            return None
    
    # ==================== ASSETS ====================
    
    async def upsert_asset(self, asset_data: Dict[str, Any]) -> Any:
        """Insert or update asset"""
        try:
            return await self.db.asset.upsert(
                where={'symbol': asset_data['symbol']},
                data={
                    'create': asset_data,
                    'update': {
                        'exchange': asset_data['exchange'],
                        'ticker': asset_data['ticker'],
                        'description': asset_data['description'],
                        'type': asset_data['type'],
                        'categoryKey': asset_data['categoryKey'],
                        'searchQuery': asset_data.get('searchQuery'),
                        'isActive': asset_data.get('isActive', True),
                        'lastUpdate': datetime.now()
                    }
                }
            )
        except Exception as e:
            logger.error(f"Error upserting asset {asset_data.get('symbol')}: {e}")
            raise
    
    async def get_all_assets(self, category_key: Optional[str] = None, 
                            exchange: Optional[str] = None,
                            is_active: bool = True) -> List[Any]:
        """Get all assets with filters"""
        try:
            where = {'isActive': is_active}
            if category_key:
                where['categoryKey'] = category_key
            if exchange:
                where['exchange'] = exchange
            
            return await self.db.asset.find_many(
                where=where,
                include={'category': True},
                order={'symbol': 'asc'}
            )
        except Exception as e:
            logger.error(f"Error getting assets: {e}")
            return []
    
    async def get_asset(self, symbol: str) -> Optional[Any]:
        """Get asset by symbol"""
        try:
            return await self.db.asset.find_unique(
                where={'symbol': symbol},
                include={'category': True, 'currentCandle': True}
            )
        except Exception as e:
            logger.error(f"Error getting asset {symbol}: {e}")
            return None
    
    # ==================== CANDLES ====================
    
    async def insert_candle(self, candle_data: Dict[str, Any]) -> Any:
        """Insert candle (skip if already exists)"""
        try:
            # Check if candle already exists
            existing = await self.db.candle.find_first(
                where={
                    'assetId': candle_data['assetId'],
                    'timeframe': candle_data['timeframe'],
                    'timestamp': candle_data['timestamp']
                }
            )
            
            if existing:
                return existing
            
            return await self.db.candle.create(data=candle_data)
        except Exception as e:
            logger.error(f"Error inserting candle: {e}")
            return None
    
    async def insert_candles_bulk(self, candles_data: List[Dict[str, Any]]) -> int:
        """Insert multiple candles at once"""
        try:
            inserted = 0
            for candle in candles_data:
                result = await self.insert_candle(candle)
                if result:
                    inserted += 1
            return inserted
        except Exception as e:
            logger.error(f"Error bulk inserting candles: {e}")
            return 0
    
    async def get_candles(self, symbol: str, timeframe: str, 
                         limit: int = 1000) -> List[Any]:
        """Get candles for asset"""
        try:
            asset = await self.get_asset(symbol)
            if not asset:
                return []
            
            return await self.db.candle.find_many(
                where={
                    'assetId': asset.id,
                    'timeframe': timeframe
                },
                order={'timestamp': 'desc'},
                take=limit
            )
        except Exception as e:
            logger.error(f"Error getting candles for {symbol}: {e}")
            return []
    
    # ==================== CURRENT CANDLES ====================
    
    async def upsert_current_candle(self, current_data: Dict[str, Any]) -> Any:
        """Insert or update current candle"""
        try:
            asset = await self.get_asset(current_data['symbol'])
            if not asset:
                logger.warning(f"Asset not found for current candle: {current_data['symbol']}")
                return None
            
            current_data['assetId'] = asset.id
            
            return await self.db.currentcandle.upsert(
                where={'assetId': asset.id},
                data={
                    'create': current_data,
                    'update': {
                        'timeframe': current_data['timeframe'],
                        'timestamp': current_data['timestamp'],
                        'datetime': current_data['datetime'],
                        'open': current_data['open'],
                        'high': current_data['high'],
                        'low': current_data['low'],
                        'close': current_data['close'],
                        'volume': current_data['volume'],
                        'priceChange': current_data['priceChange'],
                        'priceChangePercent': current_data['priceChangePercent'],
                        'isPositive': current_data['isPositive'],
                        'lastUpdate': datetime.now()
                    }
                }
            )
        except Exception as e:
            logger.error(f"Error upserting current candle for {current_data.get('symbol')}: {e}")
            return None
    
    async def get_current_candle(self, symbol: str) -> Optional[Any]:
        """Get current candle for asset"""
        try:
            return await self.db.currentcandle.find_unique(
                where={'symbol': symbol},
                include={'asset': True}
            )
        except Exception as e:
            logger.error(f"Error getting current candle for {symbol}: {e}")
            return None
    
    async def get_all_current_candles(self) -> List[Any]:
        """Get all current candles"""
        try:
            return await self.db.currentcandle.find_many(
                include={'asset': True},
                order={'lastUpdate': 'desc'}
            )
        except Exception as e:
            logger.error(f"Error getting all current candles: {e}")
            return []
    
    # ==================== SYNC LOGS ====================
    
    async def create_sync_log(self, log_data: Dict[str, Any]) -> Any:
        """Create sync log"""
        try:
            return await self.db.synclog.create(data=log_data)
        except Exception as e:
            logger.error(f"Error creating sync log: {e}")
            return None
    
    async def update_sync_log(self, log_id: str, update_data: Dict[str, Any]) -> Any:
        """Update sync log"""
        try:
            return await self.db.synclog.update(
                where={'id': log_id},
                data=update_data
            )
        except Exception as e:
            logger.error(f"Error updating sync log {log_id}: {e}")
            return None
    
    async def get_recent_sync_logs(self, limit: int = 100) -> List[Any]:
        """Get recent sync logs"""
        try:
            return await self.db.synclog.find_many(
                order={'startedAt': 'desc'},
                take=limit
            )
        except Exception as e:
            logger.error(f"Error getting sync logs: {e}")
            return []
    
    # ==================== CONFIG ====================
    
    async def get_config(self, key: str) -> Optional[str]:
        """Get config value"""
        try:
            config = await self.db.config.find_unique(where={'key': key})
            return config.value if config else None
        except Exception as e:
            logger.error(f"Error getting config {key}: {e}")
            return None
    
    async def set_config(self, key: str, value: str, description: str = None) -> Any:
        """Set config value"""
        try:
            return await self.db.config.upsert(
                where={'key': key},
                data={
                    'create': {'key': key, 'value': value, 'description': description},
                    'update': {'value': value, 'description': description}
                }
            )
        except Exception as e:
            logger.error(f"Error setting config {key}: {e}")
            return None


# Global database manager instance
db_manager = DatabaseManager()
