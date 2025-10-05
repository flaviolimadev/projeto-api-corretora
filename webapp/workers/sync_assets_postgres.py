"""
Worker para sincronizar ativos usando PostgreSQL Manager
"""

import asyncio
import logging
import requests
import json
from datetime import datetime
import sys
import os

# Adicionar o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.postgres_manager import postgres_manager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def generate_search_queries(category, exchange, search_term=""):
    """Gerar queries de busca baseadas na categoria e exchange"""
    queries = []
    
    if search_term:
        queries.append(search_term)
    else:
        if category == 'crypto':
            if exchange == 'BINANCE':
                queries = ['BTC', 'ETH', 'ADA', 'DOT', 'LINK', 'UNI', 'LTC', 'BCH', 'XRP', 'BNB']
            elif exchange == 'COINBASE':
                queries = ['BTC', 'ETH', 'ADA', 'DOT', 'LINK', 'UNI', 'LTC', 'BCH', 'XRP']
            else:
                queries = ['BTC', 'ETH', 'ADA', 'DOT', 'LINK']
        elif category == 'forex':
            queries = ['EUR', 'GBP', 'USD', 'JPY', 'CHF', 'AUD', 'CAD', 'NZD']
        elif category == 'stocks':
            if exchange == 'NASDAQ':
                queries = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'AMD', 'INTC']
            elif exchange == 'NYSE':
                queries = ['JPM', 'JNJ', 'V', 'PG', 'UNH', 'HD', 'MA', 'DIS', 'PYPL', 'ADBE']
            else:
                queries = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
        elif category == 'indices':
            queries = ['SPX', 'NDX', 'DJI', 'RUT', 'VIX', 'COMP']
        elif category == 'commodities':
            queries = ['GC', 'SI', 'CL', 'NG', 'ZC', 'ZS', 'ZW']
        elif category == 'bonds':
            queries = ['TY', 'US', 'UB', 'FGBL', 'FGBM', 'FGBS']
        elif category == 'etfs':
            queries = ['SPY', 'QQQ', 'IWM', 'VTI', 'VEA', 'VWO', 'GLD', 'SLV', 'TLT', 'HYG']
        elif category == 'futures':
            queries = ['ES', 'NQ', 'YM', 'RTY', 'ZC', 'ZS', 'CL', 'NG', 'GC', 'SI']
    
    return queries


def is_valid_asset_for_category(symbol, category, exchange):
    """Verificar se um símbolo é válido para a categoria"""
    symbol_upper = symbol.upper()
    
    if category == 'crypto':
        crypto_suffixes = ['USDT', 'BTC', 'ETH', 'BNB', 'ADA', 'DOT', 'LINK', 'UNI', 'LTC', 'BCH', 'XRP']
        return any(symbol_upper.endswith(suffix) for suffix in crypto_suffixes)
    elif category == 'forex':
        forex_pairs = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'AUDUSD', 'USDCAD', 'NZDUSD', 'EURGBP', 'EURJPY', 'GBPJPY']
        return any(pair in symbol_upper for pair in forex_pairs)
    elif category == 'stocks':
        return 1 <= len(symbol) <= 5 and symbol_upper.isalpha()
    elif category == 'indices':
        index_symbols = ['SPX', 'NDX', 'DJI', 'RUT', 'VIX', 'COMP', 'ES', 'NQ', 'YM', 'RTY']
        return any(index in symbol_upper for index in index_symbols)
    elif category == 'commodities':
        commodity_symbols = ['GC', 'SI', 'CL', 'NG', 'ZC', 'ZS', 'ZW', 'CAD', 'ALI', 'ZNI']
        return any(commodity in symbol_upper for commodity in commodity_symbols)
    elif category == 'bonds':
        bond_symbols = ['TY', 'US', 'UB', 'FGBL', 'FGBM', 'FGBS', 'JGB']
        return any(bond in symbol_upper for bond in bond_symbols)
    elif category == 'etfs':
        etf_symbols = ['SPY', 'QQQ', 'IWM', 'VTI', 'VEA', 'VWO', 'GLD', 'SLV', 'TLT', 'HYG']
        return any(etf in symbol_upper for etf in etf_symbols)
    elif category == 'futures':
        return symbol_upper.endswith('!')
    
    return True


def sync_assets():
    """Sincronizar ativos do TradingView para PostgreSQL"""
    start_time = datetime.now()
    logger.info("Iniciando sincronização de ativos...")
    
    try:
        # Conectar ao banco
        if not postgres_manager.connect():
            raise Exception("Falha ao conectar ao banco de dados")
        
        # Obter categorias
        categories = postgres_manager.get_all_categories()
        logger.info(f"Encontradas {len(categories)} categorias")
        
        total_assets = 0
        
        # Para cada categoria, buscar ativos
        for category in categories:
            category_key = category['key']
            exchanges = category['exchanges']
            
            logger.info(f"Processando categoria: {category_key}")
            
            for exchange in exchanges:
                try:
                    logger.info(f"  Buscando ativos em {exchange}...")
                    
                    # Buscar ativos usando a API de busca do TradingView
                    assets = []
                    search_queries = generate_search_queries(category_key, exchange)
                    
                    for query in search_queries:
                        if len(assets) >= 20:  # Limite por exchange
                            break
                            
                        try:
                            url = f"https://symbol-search.tradingview.com/symbol_search/?text={query}&type="
                            response = requests.get(url, timeout=10)
                            
                            if response.status_code == 200:
                                data = response.json()
                                
                                for item in data:
                                    if len(assets) >= 20:
                                        break
                                    
                                    symbol = item.get('symbol', '')
                                    item_exchange = item.get('exchange', '')
                                    description = item.get('description', '')
                                    type_name = item.get('type', '')
                                    
                                    # Filtrar por exchange e categoria
                                    if (item_exchange.upper() == exchange and 
                                        symbol and 
                                        is_valid_asset_for_category(symbol, category_key, exchange)):
                                        
                                        asset_data = {
                                            'symbol': f"{exchange}:{symbol}",
                                            'exchange': exchange,
                                            'ticker': symbol,
                                            'description': description,
                                            'type': type_name,
                                            'categoryKey': category_key,
                                            'searchQuery': query
                                        }
                                        
                                        # Evitar duplicatas
                                        if not any(a['symbol'] == asset_data['symbol'] for a in assets):
                                            assets.append(asset_data)
                                            
                        except Exception as e:
                            logger.warning(f"Erro na busca com query '{query}': {e}")
                            continue
                    
                    # Salvar ativos no banco
                    for asset_data in assets:
                        try:
                            success = postgres_manager.create_asset(asset_data)
                            if success:
                                total_assets += 1
                        except Exception as e:
                            logger.error(f"Erro ao salvar ativo {asset_data['symbol']}: {e}")
                    
                    logger.info(f"  {len(assets)} ativos encontrados em {exchange}")
                    
                except Exception as e:
                    logger.error(f"Erro ao processar exchange {exchange}: {e}")
                    continue
        
        # Criar log de sincronização
        duration = (datetime.now() - start_time).total_seconds()
        log_data = {
            'type': 'assets',
            'status': 'completed',
            'itemsCount': total_assets,
            'startedAt': start_time,
            'finishedAt': datetime.now(),
            'duration': duration
        }
        
        postgres_manager.create_sync_log(log_data)
        
        logger.info(f"Sincronização concluída: {total_assets} ativos")
        logger.info(f"Duração: {duration:.2f} segundos")
        
        # Verificar ativos no banco
        assets = postgres_manager.get_all_assets(limit=100)
        logger.info(f"Total de ativos no banco: {len(assets)}")
        
        postgres_manager.disconnect()
        return True
        
    except Exception as e:
        logger.error(f"Erro na sincronização: {e}")
        
        # Log de erro
        duration = (datetime.now() - start_time).total_seconds()
        log_data = {
            'type': 'assets',
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
    print("SINCRONIZADOR DE ATIVOS - POSTGRESQL")
    print("=" * 60)
    print()
    
    success = sync_assets()
    
    if success:
        print()
        print("=" * 60)
        print("SINCRONIZACAO CONCLUIDA COM SUCESSO!")
        print("=" * 60)
        print()
        print("Próximos passos:")
        print("  1. python workers/sync_candles_postgres.py")
        print("  2. python workers/sync_current_candles_postgres.py")
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
