#!/usr/bin/env python3
"""
Script de teste para a API de Category Assets
Testa a rota /api/category-assets
"""

import requests
import json
import time

def test_category_assets_api():
    """Testa a API de category assets"""
    base_url = "http://localhost:5000"
    
    print("Teste da API de Category Assets")
    print("=" * 50)
    
    # Verificar se o servidor está rodando
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code != 200:
            print("ERRO - Servidor não está respondendo")
            return
    except requests.exceptions.RequestException as e:
        print(f"ERRO - Não foi possível conectar: {e}")
        return
    
    print("OK - Servidor está rodando")
    
    # Teste 1: Crypto da BINANCE
    print("\nTeste 1: Criptomoedas da BINANCE")
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/api/category-assets", params={
            'category': 'crypto',
            'exchange': 'BINANCE',
            'limit': 10
        }, timeout=15)
        elapsed = time.time() - start_time
        
        print(f"Tempo: {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCESSO!")
            print(f"   Categoria: {data['category']}")
            print(f"   Exchange: {data['exchange']}")
            print(f"   Total de ativos: {data['total_assets']}")
            print(f"   Limite: {data['limit']}")
            print(f"   Ativos encontrados:")
            for i, asset in enumerate(data['assets'][:5], 1):
                print(f"     {i}. {asset['symbol']} - {asset['description']}")
            if len(data['assets']) > 5:
                print(f"     ... e mais {len(data['assets']) - 5} ativos")
        else:
            print(f"ERRO: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Detalhes: {error_data}")
            except:
                print(f"   Resposta: {response.text}")
                
    except Exception as e:
        print(f"ERRO: {e}")
    
    # Teste 2: Stocks da NASDAQ
    print("\nTeste 2: Ações da NASDAQ")
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/api/category-assets", params={
            'category': 'stocks',
            'exchange': 'NASDAQ',
            'limit': 15
        }, timeout=15)
        elapsed = time.time() - start_time
        
        print(f"Tempo: {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCESSO!")
            print(f"   Categoria: {data['category']}")
            print(f"   Exchange: {data['exchange']}")
            print(f"   Total de ativos: {data['total_assets']}")
            print(f"   Ativos encontrados:")
            for i, asset in enumerate(data['assets'][:5], 1):
                print(f"     {i}. {asset['symbol']} - {asset['description']}")
        else:
            print(f"ERRO: {response.status_code}")
            
    except Exception as e:
        print(f"ERRO: {e}")
    
    # Teste 3: Forex da FX_IDC
    print("\nTeste 3: Forex da FX_IDC")
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/api/category-assets", params={
            'category': 'forex',
            'exchange': 'FX_IDC',
            'limit': 8
        }, timeout=15)
        elapsed = time.time() - start_time
        
        print(f"Tempo: {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCESSO!")
            print(f"   Categoria: {data['category']}")
            print(f"   Exchange: {data['exchange']}")
            print(f"   Total de ativos: {data['total_assets']}")
            print(f"   Ativos encontrados:")
            for i, asset in enumerate(data['assets'][:5], 1):
                print(f"     {i}. {asset['symbol']} - {asset['description']}")
        else:
            print(f"ERRO: {response.status_code}")
            
    except Exception as e:
        print(f"ERRO: {e}")
    
    # Teste 4: Busca com termo específico
    print("\nTeste 4: Busca por termo específico (BTC)")
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/api/category-assets", params={
            'category': 'crypto',
            'exchange': 'BINANCE',
            'search': 'BTC',
            'limit': 5
        }, timeout=15)
        elapsed = time.time() - start_time
        
        print(f"Tempo: {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCESSO!")
            print(f"   Termo de busca: {data['search_term']}")
            print(f"   Total de ativos: {data['total_assets']}")
            print(f"   Ativos encontrados:")
            for i, asset in enumerate(data['assets'], 1):
                print(f"     {i}. {asset['symbol']} - {asset['description']}")
        else:
            print(f"ERRO: {response.status_code}")
            
    except Exception as e:
        print(f"ERRO: {e}")
    
    # Teste 5: Erro - categoria inválida
    print("\nTeste 5: Erro - categoria inválida")
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/api/category-assets", params={
            'category': 'invalid',
            'exchange': 'BINANCE'
        }, timeout=10)
        elapsed = time.time() - start_time
        
        print(f"Tempo: {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 400:
            data = response.json()
            print("ERRO ESPERADO!")
            print(f"   Mensagem: {data['error']}")
            print(f"   Categorias válidas: {', '.join(data['valid_categories'])}")
        else:
            print(f"ERRO: Deveria ter retornado 400, mas retornou {response.status_code}")
            
    except Exception as e:
        print(f"ERRO: {e}")
    
    # Teste 6: Erro - exchange não suportada
    print("\nTeste 6: Erro - exchange não suportada")
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/api/category-assets", params={
            'category': 'crypto',
            'exchange': 'INVALID'
        }, timeout=10)
        elapsed = time.time() - start_time
        
        print(f"Tempo: {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 400:
            data = response.json()
            print("ERRO ESPERADO!")
            print(f"   Mensagem: {data['error']}")
            print(f"   Exchanges suportadas: {', '.join(data['supported_exchanges'])}")
        else:
            print(f"ERRO: Deveria ter retornado 400, mas retornou {response.status_code}")
            
    except Exception as e:
        print(f"ERRO: {e}")
    
    # Teste 7: Testar diferentes combinações
    print("\nTeste 7: Diferentes combinações categoria/exchange")
    test_combinations = [
        ('crypto', 'COINBASE', 5),
        ('stocks', 'NYSE', 8),
        ('indices', 'NASDAQ', 6),
        ('etfs', 'NYSE', 5)
    ]
    
    for category, exchange, limit in test_combinations:
        start_time = time.time()
        try:
            response = requests.get(f"{base_url}/api/category-assets", params={
                'category': category,
                'exchange': exchange,
                'limit': limit
            }, timeout=10)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                print(f"   {category.upper()} - {exchange}: {elapsed:.2f}s - {data['total_assets']} ativos")
            else:
                print(f"   {category.upper()} - {exchange}: ERRO {response.status_code}")
                
        except Exception as e:
            print(f"   {category.upper()} - {exchange}: ERRO {e}")
    
    print("\nTeste de Category Assets Concluido!")
    print("\nExemplos de uso:")
    print(f"   curl \"{base_url}/api/category-assets?category=crypto&exchange=BINANCE&limit=10\"")
    print(f"   curl \"{base_url}/api/category-assets?category=stocks&exchange=NASDAQ&limit=15\"")
    print(f"   curl \"{base_url}/api/category-assets?category=forex&exchange=FX_IDC&search=EUR&limit=5\"")

if __name__ == "__main__":
    test_category_assets_api()

