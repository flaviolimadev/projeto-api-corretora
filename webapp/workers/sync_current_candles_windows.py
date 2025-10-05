import sys
import os
import logging
from datetime import datetime
import time
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.postgres_manager import postgres_manager
from tradingview_scraper.symbols.stream import RealTimeData

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_current_candle_worker(symbol):
    """Worker para obter candle atual de um símbolo"""
    try:
        real_time_data = RealTimeData()
        data_generator = real_time_data.get_ohlcv(exchange_symbol=symbol)
        
        start_time = time.time()
        timeout = 5  # 5 segundos timeout
        
        for packet in data_generator:
            if time.time() - start_time > timeout:
                logger.warning(f"Timeout para {symbol}")
                return None
                
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
        
        return None
        
    except Exception as e:
        logger.error(f"Erro ao obter candle para {symbol}: {e}")
        return None

def sync_current_candles_windows():
    """Sincroniza candles atuais usando ThreadPoolExecutor para controle de timeout"""
    logger.info("Iniciando sincronização Windows de candles atuais...")
    start_time = datetime.now()
    
    if not postgres_manager.connect():
        logger.error("Falha ao conectar ao banco de dados.")
        return False

    try:
        assets = postgres_manager.get_active_assets()
        logger.info(f"Encontrados {len(assets)} ativos para sincronizar")
        
        updated_count = 0
        failed_count = 0
        
        # Processar em lotes de 5 para não sobrecarregar
        batch_size = 5
        for i in range(0, len(assets), batch_size):
            batch = assets[i:i + batch_size]
            logger.info(f"Processando lote {i//batch_size + 1}/{(len(assets) + batch_size - 1)//batch_size}")
            
            with ThreadPoolExecutor(max_workers=batch_size) as executor:
                # Submeter tarefas
                future_to_asset = {
                    executor.submit(get_current_candle_worker, asset['symbol']): asset 
                    for asset in batch
                }
                
                # Processar resultados
                for future in future_to_asset:
                    asset = future_to_asset[future]
                    symbol = asset['symbol']
                    
                    try:
                        current_candle_data = future.result(timeout=10)  # 10 segundos por símbolo
                        
                        if current_candle_data:
                            current_candle_data['assetId'] = asset['id']
                            current_candle_data['symbol'] = symbol
                            current_candle_data['timeframe'] = '1m'
                            
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
                            
                    except TimeoutError:
                        failed_count += 1
                        logger.warning(f"  ⏰ Timeout para {symbol}")
                    except Exception as e:
                        failed_count += 1
                        logger.error(f"  ❌ Erro para {symbol}: {e}")
            
            # Pausa entre lotes
            if i + batch_size < len(assets):
                time.sleep(2)

        postgres_manager.commit()
        logger.info(f"Sincronização concluída: {updated_count} sucessos, {failed_count} falhas")
        
        postgres_manager.create_sync_log({
            'type': 'current_candles_windows',
            'status': 'success',
            'itemsCount': updated_count,
            'errorMsg': None,
            'duration': (datetime.now() - start_time).total_seconds(),
            'startedAt': start_time.isoformat(),
            'finishedAt': datetime.now().isoformat()
        })
        return True
        
    except Exception as e:
        logger.error(f"Erro na sincronização: {e}")
        postgres_manager.create_sync_log({
            'type': 'current_candles_windows',
            'status': 'error',
            'itemsCount': 0,
            'errorMsg': str(e),
            'duration': (datetime.now() - start_time).total_seconds(),
            'startedAt': start_time.isoformat(),
            'finishedAt': datetime.now().isoformat()
        })
        return False
    finally:
        postgres_manager.disconnect()

if __name__ == '__main__':
    print("=" * 60)
    print("SINCRONIZADOR WINDOWS DE CANDLES ATUAIS")
    print("=" * 60)
    
    if sync_current_candles_windows():
        print("\n" + "=" * 60)
        print("SINCRONIZACAO WINDOWS CONCLUIDA COM SUCESSO!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("ERRO NA SINCRONIZACAO WINDOWS!")
        print("=" * 60)
