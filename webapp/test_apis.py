"""
Testar APIs modificadas para usar banco de dados
"""

import requests
import json

def test_api(url, description):
    """Testar uma API"""
    print(f"\n{'='*60}")
    print(f"TESTANDO: {description}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"OK - Status: {response.status_code}")
            
            # Mostrar informações relevantes
            if 'categories' in data:
                print(f"Categorias: {data.get('statistics', {}).get('total_categories', 0)}")
                print(f"Source: {data.get('source', 'N/A')}")
                for key, cat in list(data['categories'].items())[:3]:
                    print(f"  - {key}: {cat['name']}")
            
            elif 'assets' in data:
                print(f"Ativos: {data.get('total_assets', 0)}")
                print(f"Source: {data.get('source', 'N/A')}")
                for asset in data['assets'][:3]:
                    print(f"  - {asset['symbol']}: {asset['description']}")
            
            elif 'candles' in data:
                print(f"Candles: {data.get('total_candles', 0)}")
                print(f"Source: {data.get('source', 'N/A')}")
                if data['candles']:
                    candle = data['candles'][0]
                    print(f"  - Último: ${candle['close']} ({candle['datetime']})")
            
            elif 'symbol' in data and 'close' in data:
                print(f"Candle Atual: ${data['close']}")
                print(f"Source: {data.get('source', 'N/A')}")
                print(f"Last Update: {data.get('last_update', 'N/A')}")
            
            print(f"Generated: {data.get('generated_at', 'N/A')}")
            
        else:
            print(f"ERRO - Status: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Erro: {error_data.get('error', 'Erro desconhecido')}")
            except:
                print(f"Resposta: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("ERRO: Não foi possível conectar ao servidor")
        print("Certifique-se de que o app.py está rodando na porta 5000")
    
    except Exception as e:
        print(f"ERRO: {e}")

def main():
    """Executar todos os testes"""
    print("=" * 70)
    print("TESTE DAS APIs MODIFICADAS - BANCO DE DADOS")
    print("=" * 70)
    print("Base URL: http://localhost:5000")
    
    # Lista de APIs para testar
    apis = [
        ("http://localhost:5000/api/categories", "Categorias do Banco"),
        ("http://localhost:5000/api/category-assets?category=crypto&exchange=BINANCE&limit=5", "Ativos Crypto do Banco"),
        ("http://localhost:5000/api/category-assets?category=forex&exchange=FX_IDC&limit=3", "Ativos Forex do Banco"),
        ("http://localhost:5000/api/category-assets?category=stocks&exchange=NASDAQ&limit=3", "Ativos Stocks do Banco"),
        ("http://localhost:5000/api/current-candle?symbol=BINANCE:BTCUSDT&timeframe=1m", "Candle Atual do Banco"),
        ("http://localhost:5000/api/current-candle?symbol=FX_IDC:EURUSD&timeframe=1m", "Candle Atual Forex do Banco"),
    ]
    
    # Testar cada API
    for url, description in apis:
        test_api(url, description)
    
    print(f"\n{'='*70}")
    print("TESTE CONCLUÍDO!")
    print(f"{'='*70}")
    print()
    print("Se você viu 'Source: database' nas respostas,")
    print("as APIs estão funcionando com o banco PostgreSQL!")

if __name__ == "__main__":
    main()

