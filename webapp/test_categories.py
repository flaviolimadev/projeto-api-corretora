#!/usr/bin/env python3
"""
Script de teste para a API de Categorias
Testa as rotas /api/categories e /api/categories/<category>
"""

import requests
import json
import time

def test_categories_api():
    """Testa a API de categorias"""
    base_url = "http://localhost:5000"
    
    print("Teste da API de Categorias")
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
    
    # Teste 1: Listar todas as categorias
    print("\nTeste 1: Listar todas as categorias")
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/api/categories", timeout=10)
        elapsed = time.time() - start_time
        
        print(f"Tempo: {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCESSO!")
            print(f"   Total de categorias: {data['statistics']['total_categories']}")
            print(f"   Total de exchanges: {data['statistics']['total_exchanges']}")
            print(f"   Total de símbolos populares: {data['statistics']['total_popular_symbols']}")
            print(f"   Timeframes suportados: {len(data['statistics']['supported_timeframes'])}")
            
            print("\n   Categorias disponíveis:")
            for category_id, category in data['categories'].items():
                print(f"   - {category['icon']} {category['name']}: {category['description']}")
                print(f"     Exchanges: {', '.join(category['exchanges'][:3])}{'...' if len(category['exchanges']) > 3 else ''}")
                print(f"     Símbolos: {len(category['popular_symbols'])} populares")
        else:
            print(f"ERRO: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Detalhes: {error_data}")
            except:
                print(f"   Resposta: {response.text}")
                
    except Exception as e:
        print(f"ERRO: {e}")
    
    # Teste 2: Detalhes da categoria Crypto
    print("\nTeste 2: Detalhes da categoria Crypto")
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/api/categories/crypto", timeout=10)
        elapsed = time.time() - start_time
        
        print(f"Tempo: {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCESSO!")
            print(f"   Nome: {data['name']}")
            print(f"   Descrição: {data['description']}")
            print(f"   Ícone: {data['icon']}")
            print(f"   Total de exchanges: {data['total_exchanges']}")
            print(f"   Total de símbolos: {data['total_symbols']}")
            print(f"   Exchanges: {', '.join(data['exchanges'])}")
            print(f"   Símbolos populares:")
            for symbol in data['popular_symbols'][:5]:
                print(f"     - {symbol}")
            if len(data['popular_symbols']) > 5:
                print(f"     ... e mais {len(data['popular_symbols']) - 5} símbolos")
        else:
            print(f"ERRO: {response.status_code}")
            
    except Exception as e:
        print(f"ERRO: {e}")
    
    # Teste 3: Detalhes da categoria Forex
    print("\nTeste 3: Detalhes da categoria Forex")
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/api/categories/forex", timeout=10)
        elapsed = time.time() - start_time
        
        print(f"Tempo: {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCESSO!")
            print(f"   Nome: {data['name']}")
            print(f"   Descrição: {data['description']}")
            print(f"   Ícone: {data['icon']}")
            print(f"   Total de exchanges: {data['total_exchanges']}")
            print(f"   Total de símbolos: {data['total_symbols']}")
            print(f"   Símbolos populares:")
            for symbol in data['popular_symbols'][:5]:
                print(f"     - {symbol}")
        else:
            print(f"ERRO: {response.status_code}")
            
    except Exception as e:
        print(f"ERRO: {e}")
    
    # Teste 4: Detalhes da categoria Stocks
    print("\nTeste 4: Detalhes da categoria Stocks")
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/api/categories/stocks", timeout=10)
        elapsed = time.time() - start_time
        
        print(f"Tempo: {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCESSO!")
            print(f"   Nome: {data['name']}")
            print(f"   Descrição: {data['description']}")
            print(f"   Ícone: {data['icon']}")
            print(f"   Total de exchanges: {data['total_exchanges']}")
            print(f"   Total de símbolos: {data['total_symbols']}")
            print(f"   Exchanges: {', '.join(data['exchanges'])}")
        else:
            print(f"ERRO: {response.status_code}")
            
    except Exception as e:
        print(f"ERRO: {e}")
    
    # Teste 5: Categoria inexistente
    print("\nTeste 5: Categoria inexistente")
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/api/categories/invalid", timeout=10)
        elapsed = time.time() - start_time
        
        print(f"Tempo: {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 404:
            data = response.json()
            print("ERRO ESPERADO!")
            print(f"   Mensagem: {data['error']}")
            print(f"   Categorias disponíveis: {', '.join(data['available_categories'])}")
        else:
            print(f"ERRO: Deveria ter retornado 404, mas retornou {response.status_code}")
            
    except Exception as e:
        print(f"ERRO: {e}")
    
    # Teste 6: Testar todas as categorias
    print("\nTeste 6: Testar todas as categorias")
    categories_to_test = ['forex', 'crypto', 'stocks', 'indices', 'commodities', 'bonds', 'etfs', 'futures']
    
    for category in categories_to_test:
        start_time = time.time()
        try:
            response = requests.get(f"{base_url}/api/categories/{category}", timeout=5)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                print(f"   {data['icon']} {data['name']}: {elapsed:.2f}s - {data['total_symbols']} símbolos")
            else:
                print(f"   {category}: ERRO {response.status_code}")
                
        except Exception as e:
            print(f"   {category}: ERRO {e}")
    
    print("\nTeste de Categorias Concluído!")
    print("\nExemplos de uso:")
    print(f"   curl \"{base_url}/api/categories\"")
    print(f"   curl \"{base_url}/api/categories/crypto\"")
    print(f"   curl \"{base_url}/api/categories/forex\"")
    print(f"   curl \"{base_url}/api/categories/stocks\"")

if __name__ == "__main__":
    test_categories_api()

