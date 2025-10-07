"""
Worker para sincronizar candles atuais usando PostgreSQL Manager
"""

import asyncio
import logging
import requests
import json
from datetime import datetime
import sys
import os
import time

# Adicionar o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.postgres_manager import postgres_manager
from tradingview_scraper.symbols.stream import RealTimeData

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def sync_current_candles():
    """Sincronizar candles atuais do TradingView para PostgreSQL"""
    start_time = datetime.now()
    logger.info("Iniciando sincronização de candles atuais...")
    
    try:
        # Conectar ao banco
        if not postgres_manager.connect():
            raise Exception("Falha ao conectar ao banco de dados")
        
        # Obter ativos ativos
        assets = postgres_manager.get_active_assets(limit=20)  # Limitar para teste
        logger.info(f"Encontrados {len(assets)} ativos para sincronizar")
        
        total_updated = 0
        timeframe = '1m'  # Focar em 1 minuto para candles atuais
        
        # Para cada ativo, buscar candle atual
        for asset in assets:
            symbol = asset['symbol']
            asset_id = asset['id']
            
            try:
                logger.info(f"Atualizando candle atual para {symbol}...")
                
                # Usar RealTimeData para obter candle atual
                real_time_data = RealTimeData()
                data_generator = real_time_data.get_ohlcv(exchange_symbol=symbol)
                
                current_candle = None
                timeout = 5  # 5 segundos de timeout
                start_time_asset = time.time()
                
                for packet in data_generator:
                    if time.time() - start_time_asset > timeout:
                        logger.warning(f"Timeout para {symbol}")
                        break
                        
                    if packet and 'm' in packet and packet['m'] == 'du' and 'p' in packet:
                        data = packet['p']
                        if len(data) > 1 and isinstance(data[1], dict):
                            sds_data = data[1].get('sds_1', {})
                            if 's' in sds_data and len(sds_data['s']) > 0:
                                candle_data = sds_data['s'][0].get('v', [])
                                
                                if len(candle_data) >= 6:
                                    timestamp, open_price, high, low, close, volume = candle_data[:6]
                                    
                                    # Calcular mudança de preço
                                    price_change = float(close) - float(open_price)
                                    price_change_percent = (price_change / float(open_price)) * 100 if float(open_price) != 0 else 0
                                    
                                    current_candle = {
                                        'assetId': asset_id,
                                        'symbol': symbol,
                                        'timeframe': timeframe,
                                        'timestamp': int(timestamp),
                                        'datetime': datetime.fromtimestamp(timestamp),
                                        'open': float(open_price),
                                        'high': float(high),
                                        'low': float(low),
                                        'close': float(close),
                                        'volume': float(volume),
                                        'priceChange': price_change,
                                        'priceChangePercent': price_change_percent,
                                        'isPositive': price_change >= 0
                                    }
                                    break
                
                if current_candle:
                    try:
                        success = postgres_manager.update_current_candle(asset_id, current_candle)
                        if success:
                            total_updated += 1
                            logger.info(f"  {symbol}: ${current_candle['close']:.4f} ({current_candle['priceChangePercent']:+.2f}%)")
                        else:
                            logger.error(f"Erro ao salvar candle atual para {symbol}")
                    except Exception as e:
                        logger.error(f"Erro ao salvar candle atual para {symbol}: {e}")
                else:
                    logger.warning(f"Não foi possível obter candle atual para {symbol}")
                
                # Pequena pausa entre ativos
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Erro ao processar {symbol}: {e}")
                continue
        
        # Criar log de sincronização
        duration = (datetime.now() - start_time).total_seconds()
        log_data = {
            'type': 'current_candles',
            'status': 'completed',
            'itemsCount': total_updated,
            'startedAt': start_time,
            'finishedAt': datetime.now(),
            'duration': duration
        }
        
        postgres_manager.create_sync_log(log_data)
        
        logger.info(f"Sincronização concluída: {total_updated} candles atuais atualizados")
        logger.info(f"Duração: {duration:.2f} segundos")
        
        postgres_manager.disconnect()
        return True
        
    except Exception as e:
        logger.error(f"Erro na sincronização: {e}")
        
        # Log de erro
        duration = (datetime.now() - start_time).total_seconds()
        log_data = {
            'type': 'current_candles',
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
    print("SINCRONIZADOR DE CANDLES ATUAIS - POSTGRESQL")
    print("=" * 60)
    print()
    
    success = sync_current_candles()
    
    if success:
        print()
        print("=" * 60)
        print("SINCRONIZACAO CONCLUIDA COM SUCESSO!")
        print("=" * 60)
        print()
        print("Próximos passos:")
        print("  1. python workers/main_worker.py")
        print("  2. Criar API REST endpoints")
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
