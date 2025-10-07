"""
Worker para sincronizar candles históricos usando PostgreSQL Manager
"""

import asyncio
import logging
import requests
import json
from datetime import datetime, timedelta
import sys
import os
import time

# Adicionar o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.postgres_manager import PostgreSQLManager
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
    
    # Criar uma instância própria do manager para este worker
    postgres_manager = PostgreSQLManager()
    
    try:
        # Conectar ao banco
        if not postgres_manager.connect():
            raise Exception("Falha ao conectar ao banco de dados")
        
        # Obter ativos ativos
        assets = postgres_manager.get_all_assets(limit=50)  # Limitar para teste
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
                    
                    # Parse exchange and ticker
                    if ':' not in symbol:
                        logger.warning(f"Símbolo inválido: {symbol}")
                        continue
                    
                    exchange, ticker = symbol.split(':', 1)
                    
                    # Usar Streamer para obter dados históricos
                    streamer = Streamer(export_result=True, export_type='json')
                    historical_data = streamer.stream(
                        exchange=exchange,
                        symbol=ticker,
                        timeframe=timeframe,
                        numb_price_candles=1000  # Últimos 1000 candles
                    )
                    
                    candles_count = 0
                    
                    # Processar dados históricos
                    if historical_data and 'ohlc' in historical_data and historical_data['ohlc']:
                        for candle_data in historical_data['ohlc']:
                            try:
                                candle_record = {
                                    'assetId': asset_id,
                                    'symbol': symbol,
                                    'timeframe': timeframe,
                                    'timestamp': int(candle_data['timestamp']),
                                    'datetime': datetime.fromtimestamp(candle_data['timestamp']),
                                    'open': float(candle_data['open']),
                                    'high': float(candle_data['high']),
                                    'low': float(candle_data['low']),
                                    'close': float(candle_data['close']),
                                    'volume': float(candle_data['volume'])
                                }
                                
                                success = postgres_manager.create_candle(candle_record)
                                if success:
                                    candles_count += 1
                                    total_candles += 1
                            except Exception as e:
                                logger.warning(f"Erro ao salvar candle: {e}")
                    else:
                        logger.warning(f"Nenhum dado histórico encontrado para {symbol} {timeframe}")
                    
                    logger.info(f"  {candles_count} candles salvos para {timeframe}")
                    
                    # Pequena pausa entre timeframes
                    time.sleep(0.5)
                    
                except Exception as e:
                    logger.error(f"Erro ao processar {symbol} {timeframe}: {e}")
                    continue
            
            # Pausa entre ativos
            time.sleep(1)
        
        # Criar log de sincronização
        duration = (datetime.now() - start_time).total_seconds()
        log_data = {
            'type': 'candles',
            'status': 'completed',
            'itemsCount': total_candles,
            'startedAt': start_time,
            'finishedAt': datetime.now(),
            'duration': duration
        }
        
        postgres_manager.create_sync_log(log_data)
        
        logger.info(f"Sincronização concluída: {total_candles} candles")
        logger.info(f"Duração: {duration:.2f} segundos")
        
        postgres_manager.disconnect()
        return True
        
    except Exception as e:
        logger.error(f"Erro na sincronização: {e}")
        
        # Log de erro
        duration = (datetime.now() - start_time).total_seconds()
        log_data = {
            'type': 'candles',
            'status': 'error',
            'itemsCount': 0,
            'errorMsg': str(e),
            'startedAt': start_time,
            'finishedAt': datetime.now(),
            'duration': duration
        }
        
        try:
            postgres_manager.create_sync_log(log_data)
            postgres_manager.disconnect()
        except:
            pass
        
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("SINCRONIZADOR DE CANDLES HISTORICOS - POSTGRESQL")
    print("=" * 60)
    print()
    
    success = sync_candles()
    
    if success:
        print()
        print("=" * 60)
        print("SINCRONIZACAO CONCLUIDA COM SUCESSO!")
        print("=" * 60)
        print()
        print("Próximos passos:")
        print("  1. python workers/sync_current_candles_postgres.py")
        print("  2. python workers/main_worker.py")
    else:
        print()
        print("=" * 60)
        print("ERRO NA SINCRONIZACAO!")
        print("=" * 60)
        print()
        print("Verifique:")
        print("  - Conexão com PostgreSQL")
        print("  - Tabelas criadas")
        print("  - Logs de erro acima")

