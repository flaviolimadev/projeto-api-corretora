"""
Worker para sincronizar categorias usando PostgreSQL Manager direto
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

from database.postgres_manager import PostgreSQLManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def sync_categories():
    """Sincronizar categorias do TradingView para PostgreSQL"""
    start_time = datetime.now()
    logger.info("Iniciando sincronização de categorias...")
    
    # Criar uma instância própria do manager para este worker
    postgres_manager = PostgreSQLManager()
    
    try:
        # Conectar ao banco
        if not postgres_manager.connect():
            raise Exception("Falha ao conectar ao banco de dados")
        
        # Dados das categorias (mesmo da API /api/categories)
        categories_data = {
            'forex': {
                'name': 'Forex',
                'description': 'Moedas e pares de câmbio',
                'icon': '💱',
                'exchanges': ['FX_IDC', 'FXCM', 'OANDA', 'FX_IDC'],
                'timeframes': ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']
            },
            'crypto': {
                'name': 'Crypto',
                'description': 'Criptomoedas e tokens digitais',
                'icon': '₿',
                'exchanges': ['BINANCE', 'COINBASE', 'KRAKEN', 'BITFINEX', 'HUOBI', 'KUCOIN'],
                'timeframes': ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']
            },
            'stocks': {
                'name': 'Stocks',
                'description': 'Ações de empresas',
                'icon': '📈',
                'exchanges': ['NASDAQ', 'NYSE', 'AMEX', 'LSE', 'TSE', 'HKEX', 'SSE'],
                'timeframes': ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']
            },
            'indices': {
                'name': 'Indices',
                'description': 'Índices de mercado',
                'icon': '📊',
                'exchanges': ['NASDAQ', 'NYSE', 'CBOE', 'CME'],
                'timeframes': ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']
            },
            'commodities': {
                'name': 'Commodities',
                'description': 'Mercadorias e matérias-primas',
                'icon': '🥇',
                'exchanges': ['COMEX', 'NYMEX', 'CBOT', 'LME'],
                'timeframes': ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']
            },
            'bonds': {
                'name': 'Bonds',
                'description': 'Títulos e obrigações',
                'icon': '🏛️',
                'exchanges': ['CBOT', 'EUREX', 'TSE'],
                'timeframes': ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']
            },
            'etfs': {
                'name': 'ETFs',
                'description': 'Fundos negociados em bolsa',
                'icon': '📦',
                'exchanges': ['NYSE', 'NASDAQ', 'AMEX'],
                'timeframes': ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']
            },
            'futures': {
                'name': 'Futures',
                'description': 'Contratos futuros',
                'icon': '⏰',
                'exchanges': ['CME', 'CBOT', 'NYMEX', 'COMEX', 'EUREX'],
                'timeframes': ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']
            }
        }
        
        # Sincronizar cada categoria
        synced_count = 0
        for key, data in categories_data.items():
            try:
                category_data = {
                    'key': key,
                    'name': data['name'],
                    'description': data['description'],
                    'icon': data['icon'],
                    'exchanges': data['exchanges'],
                    'timeframes': data['timeframes']
                }
                
                success = postgres_manager.create_category(category_data)
                if success:
                    synced_count += 1
                    logger.info(f"Categoria '{key}' sincronizada")
                else:
                    logger.error(f"Erro ao sincronizar categoria '{key}'")
                    
            except Exception as e:
                logger.error(f"Erro ao processar categoria '{key}': {e}")
        
        # Criar log de sincronização
        duration = (datetime.now() - start_time).total_seconds()
        log_data = {
            'type': 'categories',
            'status': 'completed',
            'itemsCount': synced_count,
            'startedAt': start_time,
            'finishedAt': datetime.now(),
            'duration': duration
        }
        
        postgres_manager.create_sync_log(log_data)
        
        logger.info(f"Sincronização concluída: {synced_count}/{len(categories_data)} categorias")
        logger.info(f"Duração: {duration:.2f} segundos")
        
        # Verificar categorias no banco
        categories = postgres_manager.get_all_categories()
        logger.info(f"Total de categorias no banco: {len(categories)}")
        
        for cat in categories:
            logger.info(f"  - {cat['key']}: {cat['name']} ({len(cat['exchanges'])} exchanges)")
        
        postgres_manager.disconnect()
        return True
        
    except Exception as e:
        logger.error(f"Erro na sincronização: {e}")
        
        # Log de erro
        duration = (datetime.now() - start_time).total_seconds()
        log_data = {
            'type': 'categories',
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
    print("SINCRONIZADOR DE CATEGORIAS - POSTGRESQL")
    print("=" * 60)
    print()
    
    success = sync_categories()
    
    if success:
        print()
        print("=" * 60)
        print("SINCRONIZACAO CONCLUIDA COM SUCESSO!")
        print("=" * 60)
        print()
        print("Próximos passos:")
        print("  1. python workers/sync_assets_postgres.py")
        print("  2. Verificar: python -c \"from database.postgres_manager import postgres_manager; postgres_manager.connect(); cats = postgres_manager.get_all_categories(); print(f'Categorias: {len(cats)}'); postgres_manager.disconnect()\"")
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

