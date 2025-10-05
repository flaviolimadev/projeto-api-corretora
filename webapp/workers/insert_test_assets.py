"""
Inserir ativos de teste para validar o sistema
"""

import sys
import os
from datetime import datetime

# Adicionar o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.postgres_manager import postgres_manager

def insert_test_assets():
    """Inserir ativos de teste"""
    print("Inserindo ativos de teste...")
    
    try:
        # Conectar ao banco
        if not postgres_manager.connect():
            raise Exception("Falha ao conectar ao banco")
        
        # Ativos de teste
        test_assets = [
            # Crypto
            {'symbol': 'BINANCE:BTCUSDT', 'exchange': 'BINANCE', 'ticker': 'BTCUSDT', 'description': 'Bitcoin / Tether', 'type': 'crypto', 'categoryKey': 'crypto'},
            {'symbol': 'BINANCE:ETHUSDT', 'exchange': 'BINANCE', 'ticker': 'ETHUSDT', 'description': 'Ethereum / Tether', 'type': 'crypto', 'categoryKey': 'crypto'},
            {'symbol': 'BINANCE:ADAUSDT', 'exchange': 'BINANCE', 'ticker': 'ADAUSDT', 'description': 'Cardano / Tether', 'type': 'crypto', 'categoryKey': 'crypto'},
            {'symbol': 'BINANCE:DOTUSDT', 'exchange': 'BINANCE', 'ticker': 'DOTUSDT', 'description': 'Polkadot / Tether', 'type': 'crypto', 'categoryKey': 'crypto'},
            {'symbol': 'BINANCE:LINKUSDT', 'exchange': 'BINANCE', 'ticker': 'LINKUSDT', 'description': 'Chainlink / Tether', 'type': 'crypto', 'categoryKey': 'crypto'},
            
            # Forex
            {'symbol': 'FX_IDC:EURUSD', 'exchange': 'FX_IDC', 'ticker': 'EURUSD', 'description': 'Euro / US Dollar', 'type': 'forex', 'categoryKey': 'forex'},
            {'symbol': 'FX_IDC:GBPUSD', 'exchange': 'FX_IDC', 'ticker': 'GBPUSD', 'description': 'British Pound / US Dollar', 'type': 'forex', 'categoryKey': 'forex'},
            {'symbol': 'FX_IDC:USDJPY', 'exchange': 'FX_IDC', 'ticker': 'USDJPY', 'description': 'US Dollar / Japanese Yen', 'type': 'forex', 'categoryKey': 'forex'},
            {'symbol': 'FX_IDC:USDCHF', 'exchange': 'FX_IDC', 'ticker': 'USDCHF', 'description': 'US Dollar / Swiss Franc', 'type': 'forex', 'categoryKey': 'forex'},
            {'symbol': 'FX_IDC:AUDUSD', 'exchange': 'FX_IDC', 'ticker': 'AUDUSD', 'description': 'Australian Dollar / US Dollar', 'type': 'forex', 'categoryKey': 'forex'},
            
            # Stocks
            {'symbol': 'NASDAQ:AAPL', 'exchange': 'NASDAQ', 'ticker': 'AAPL', 'description': 'Apple Inc.', 'type': 'stock', 'categoryKey': 'stocks'},
            {'symbol': 'NASDAQ:GOOGL', 'exchange': 'NASDAQ', 'ticker': 'GOOGL', 'description': 'Alphabet Inc.', 'type': 'stock', 'categoryKey': 'stocks'},
            {'symbol': 'NASDAQ:MSFT', 'exchange': 'NASDAQ', 'ticker': 'MSFT', 'description': 'Microsoft Corporation', 'type': 'stock', 'categoryKey': 'stocks'},
            {'symbol': 'NASDAQ:AMZN', 'exchange': 'NASDAQ', 'ticker': 'AMZN', 'description': 'Amazon.com Inc.', 'type': 'stock', 'categoryKey': 'stocks'},
            {'symbol': 'NASDAQ:TSLA', 'exchange': 'NASDAQ', 'ticker': 'TSLA', 'description': 'Tesla Inc.', 'type': 'stock', 'categoryKey': 'stocks'},
            
            # Indices
            {'symbol': 'NASDAQ:NDX', 'exchange': 'NASDAQ', 'ticker': 'NDX', 'description': 'NASDAQ 100', 'type': 'index', 'categoryKey': 'indices'},
            {'symbol': 'NYSE:SPX', 'exchange': 'NYSE', 'ticker': 'SPX', 'description': 'S&P 500', 'type': 'index', 'categoryKey': 'indices'},
            {'symbol': 'NYSE:DJI', 'exchange': 'NYSE', 'ticker': 'DJI', 'description': 'Dow Jones Industrial Average', 'type': 'index', 'categoryKey': 'indices'},
            
            # Commodities
            {'symbol': 'COMEX:GC1!', 'exchange': 'COMEX', 'ticker': 'GC1!', 'description': 'Gold Futures', 'type': 'commodity', 'categoryKey': 'commodities'},
            {'symbol': 'NYMEX:CL1!', 'exchange': 'NYMEX', 'ticker': 'CL1!', 'description': 'Crude Oil Futures', 'type': 'commodity', 'categoryKey': 'commodities'},
        ]
        
        # Inserir ativos
        inserted_count = 0
        for asset_data in test_assets:
            try:
                success = postgres_manager.create_asset(asset_data)
                if success:
                    inserted_count += 1
                    print(f"OK - {asset_data['symbol']} - {asset_data['description']}")
                else:
                    print(f"ERRO - Erro ao inserir {asset_data['symbol']}")
            except Exception as e:
                print(f"ERRO - Erro ao inserir {asset_data['symbol']}: {e}")
        
        print(f"\nOK - {inserted_count}/{len(test_assets)} ativos inseridos com sucesso!")
        
        # Verificar total de ativos
        assets = postgres_manager.get_all_assets()
        print(f"Total de ativos no banco: {len(assets)}")
        
        postgres_manager.disconnect()
        return True
        
    except Exception as e:
        print(f"ERRO: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("INSERINDO ATIVOS DE TESTE")
    print("=" * 60)
    print()
    
    success = insert_test_assets()
    
    if success:
        print()
        print("=" * 60)
        print("ATIVOS DE TESTE INSERIDOS COM SUCESSO!")
        print("=" * 60)
        print()
        print("Próximos passos:")
        print("  1. python workers/sync_current_candles_postgres.py")
        print("  2. python api_database.py")
        print("  3. python test_database_api.py")
    else:
        print()
        print("=" * 60)
        print("ERRO AO INSERIR ATIVOS!")
        print("=" * 60)
