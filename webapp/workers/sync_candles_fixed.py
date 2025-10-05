"""
Worker corrigido para sincronizar candles históricos usando PostgreSQL Manager
"""

import logging
import json
from datetime import datetime, timedelta
import sys
import os
import time

# Adicionar o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.postgres_manager import postgres_manager
from tradingview_scraper.symbols.stream import Streamer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def sync_candles():
    """Sincronizar candles históricos do TradingView para PostgreSQL"""
    start_time = datetime.now()
    logger.info("Iniciando sincronização de candles históricos...")
    
    try:
        # Conectar ao banco
        if not postgres_manager.connect():
            raise Exception("Falha ao conectar ao banco de dados")
        
        # Obter apenas ativos ativos
        assets = postgres_manager.get_active_assets(limit=10)  # Limitar para teste
        logger.info(f"Encontrados {len(assets)} ativos para sincronizar")
        
        total_candles = 0
        timeframes = ['1m', '5m', '15m', '1h', '4h', '1d']
        
        # Para cada ativo, buscar candles
        for asset in assets:
            symbol = asset['symbol']
            asset_id = asset['id']
            
            logger.info(f"Processando {symbol}...")
            
            for timeframe in timeframes:
                try:
                    logger.info(f"  Buscando candles {timeframe}...")
                    
                    # Usar Streamer para obter dados históricos
                    streamer = Streamer(export_result=True, export_type='json')
                    
                    # Parse exchange and symbol
                    exchange, ticker = symbol.split(':')
                    
                    historical_data = streamer.stream(
                        exchange=exchange,
                        symbol=ticker,
                        timeframe=timeframe,
                        numb_price_candles=1000  # Últimos 1000 candles
                    )
                    
                    candles_count = 0
                    if 'ohlc' in historical_data and historical_data['ohlc']:
                        for candle in historical_data['ohlc']:
                            candle_record = {
                                'assetId': asset_id,
                                'symbol': symbol,
                                'timeframe': timeframe,
                                'timestamp': int(candle['timestamp']),
                                'datetime': datetime.fromtimestamp(candle['timestamp']).isoformat(),
                                'open': float(candle['open']),
                                'high': float(candle['high']),
                                'low': float(candle['low']),
                                'close': float(candle['close']),
                                'volume': float(candle['volume'])
                            }
                            
                            # Verificar se candle já existe
                            existing_candle = postgres_manager.get_candle_by_timestamp(
                                asset_id, timeframe, int(candle['timestamp'])
                            )
                            
                            if not existing_candle:
                                success = postgres_manager.create_candle(candle_record)
                                if success:
                                    candles_count += 1
                                    total_candles += 1
                            else:
                                postgres_manager.update_candle(existing_candle['id'], candle_record)
                        
                        logger.info(f"    {candles_count} candles {timeframe} processados")
                    else:
                        logger.warning(f"    Nenhum dado histórico encontrado para {symbol} {timeframe}")
                    
                    # Pausa entre timeframes
                    time.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Erro ao processar {symbol} {timeframe}: {e}")
                    continue
            
            # Pausa entre ativos
            time.sleep(2)
        
        # Commit das alterações
        postgres_manager.commit()
        logger.info(f"Sincronização concluída: {total_candles} candles")
        
        # Log de sincronização
        postgres_manager.create_sync_log('candles', 'success', total_candles, None, (datetime.now() - start_time).total_seconds())
        
        return True
        
    except Exception as e:
        logger.error(f"Erro na sincronização: {e}")
        postgres_manager.rollback()
        postgres_manager.create_sync_log('candles', 'error', 0, str(e), (datetime.now() - start_time).total_seconds())
        return False
    finally:
        postgres_manager.disconnect()


if __name__ == '__main__':
    print("=" * 60)
    print("SINCRONIZADOR DE CANDLES HISTÓRICOS - CORRIGIDO")
    print("=" * 60)
    
    if sync_candles():
        print("\n" + "=" * 60)
        print("SINCRONIZACAO CONCLUIDA COM SUCESSO!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("ERRO NA SINCRONIZACAO!")
        print("=" * 60)
