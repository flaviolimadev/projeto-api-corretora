import sys
import os
import logging
from datetime import datetime
import time
import signal
import threading

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.postgres_manager import postgres_manager
from tradingview_scraper.symbols.stream import RealTimeData

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Timeout!")

def get_current_candle_with_timeout(symbol, timeout=3):
    """Obtém candle atual com timeout controlado"""
    try:
        # Configurar timeout
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)
        
        real_time_data = RealTimeData()
        data_generator = real_time_data.get_ohlcv(exchange_symbol=symbol)
        
        for packet in data_generator:
            if packet and 'm' in packet and packet['m'] == 'du' and 'p' in packet:
                data = packet['p']
                if len(data) > 1 and isinstance(data[1], dict):
                    sds_data = data[1].get('sds_1', {})
                    if 's' in sds_data and len(sds_data['s']) > 0:
                        candle_data = sds_data['s'][0].get('v', [])
                        
                        if len(candle_data) >= 6:
                            timestamp, open_price, high, low, close, volume = candle_data[:6]
                            
                            price_change = float(close) - float(open_price)
                            price_change_percent = (price_change / float(open_price)) * 100 if float(open_price) != 0 else 0
                            
                            signal.alarm(0)  # Cancelar timeout
                            return {
                                'timestamp': int(timestamp),
                                'datetime': datetime.fromtimestamp(timestamp).isoformat(),
                                'open': float(open_price),
                                'high': float(high),
                                'low': float(low),
                                'close': float(close),
                                'volume': float(volume),
                                'priceChange': round(price_change, 8),
                                'priceChangePercent': round(price_change_percent, 4),
                                'isPositive': price_change >= 0,
                                'lastUpdate': datetime.now().isoformat()
                            }
        
        signal.alarm(0)  # Cancelar timeout
        return None
        
    except TimeoutException:
        logger.warning(f"Timeout para {symbol}")
        return None
    except Exception as e:
        logger.error(f"Erro ao obter candle para {symbol}: {e}")
        return None
    finally:
        signal.alarm(0)  # Garantir que timeout seja cancelado

def sync_current_candles_optimized():
    """Sincroniza candles atuais de forma otimizada"""
    logger.info("Iniciando sincronização otimizada de candles atuais...")
    start_time = datetime.now()
    
    if not postgres_manager.connect():
        logger.error("Falha ao conectar ao banco de dados.")
        return False

    try:
        assets = postgres_manager.get_all_assets()
        logger.info(f"Encontrados {len(assets)} ativos para sincronizar")
        
        updated_count = 0
        failed_count = 0
        
        for i, asset in enumerate(assets):
            symbol = asset['symbol']
            timeframe = '1m'
            
            logger.info(f"[{i+1}/{len(assets)}] Atualizando {symbol}...")
            
            current_candle_data = get_current_candle_with_timeout(symbol, timeout=3)
            
            if current_candle_data:
                current_candle_data['assetId'] = asset['id']
                current_candle_data['symbol'] = symbol
                current_candle_data['timeframe'] = timeframe
                
                existing_current_candle = postgres_manager.get_current_candle_by_asset_id(asset['id'])
                if existing_current_candle:
                    postgres_manager.update_current_candle(asset['id'], current_candle_data)
                else:
                    postgres_manager.create_current_candle(current_candle_data)
                
                updated_count += 1
                logger.info(f"  ✅ {symbol}: ${current_candle_data['close']:.4f} ({current_candle_data['priceChangePercent']:+.2f}%)")
            else:
                failed_count += 1
                logger.warning(f"  ❌ Falha ao obter dados para {symbol}")
            
            # Pequena pausa entre requisições
            time.sleep(0.5)

        postgres_manager.commit()
        logger.info(f"Sincronização concluída: {updated_count} sucessos, {failed_count} falhas")
        
        postgres_manager.create_sync_log('current_candles_optimized', 'success', updated_count, None, (datetime.now() - start_time).total_seconds())
        return True
        
    except Exception as e:
        logger.error(f"Erro na sincronização: {e}")
        postgres_manager.rollback()
        postgres_manager.create_sync_log('current_candles_optimized', 'error', 0, str(e), (datetime.now() - start_time).total_seconds())
        return False
    finally:
        postgres_manager.disconnect()

if __name__ == '__main__':
    print("=" * 60)
    print("SINCRONIZADOR OTIMIZADO DE CANDLES ATUAIS")
    print("=" * 60)
    
    if sync_current_candles_optimized():
        print("\n" + "=" * 60)
        print("SINCRONIZACAO OTIMIZADA CONCLUIDA COM SUCESSO!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("ERRO NA SINCRONIZACAO OTIMIZADA!")
        print("=" * 60)
