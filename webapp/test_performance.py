#!/usr/bin/env python3
"""
Script de teste de performance para a API Current Candle
Testa cache e velocidade de resposta
"""

import requests
import time
import statistics

def test_performance():
    """Testa a performance da API com cache"""
    base_url = "http://localhost:5000"
    
    print("Teste de Performance - API Current Candle")
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
    
    # Teste 1: Primeira requisição (sem cache)
    print("\nTeste 1: Primeira requisição (sem cache)")
    symbol = "BINANCE:BTCUSDT"
    timeframe = "1m"
    
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/api/current-candle", params={
            'symbol': symbol,
            'timeframe': timeframe
        }, timeout=10)
        
        elapsed = time.time() - start_time
        print(f"Tempo: {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCESSO!")
            print(f"   Preco: ${data['close']:,.2f}")
            print(f"   Cache: {data.get('cached', 'N/A')}")
        else:
            print(f"ERRO: {response.status_code}")
            return
            
    except Exception as e:
        print(f"ERRO: {e}")
        return
    
    # Teste 2: Segunda requisição (com cache)
    print("\nTeste 2: Segunda requisição (com cache)")
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/api/current-candle", params={
            'symbol': symbol,
            'timeframe': timeframe
        }, timeout=10)
        
        elapsed = time.time() - start_time
        print(f"Tempo: {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCESSO!")
            print(f"   Preco: ${data['close']:,.2f}")
            print(f"   Cache: {data.get('cached', 'N/A')}")
        else:
            print(f"ERRO: {response.status_code}")
            
    except Exception as e:
        print(f"ERRO: {e}")
    
    # Teste 3: Múltiplas requisições para testar cache
    print("\nTeste 3: Múltiplas requisições (teste de cache)")
    times = []
    
    for i in range(5):
        start_time = time.time()
        try:
            response = requests.get(f"{base_url}/api/current-candle", params={
                'symbol': symbol,
                'timeframe': timeframe
            }, timeout=10)
            
            elapsed = time.time() - start_time
            times.append(elapsed)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Requisição {i+1}: {elapsed:.3f}s - ${data['close']:,.2f} (Cache: {data.get('cached', 'N/A')})")
            else:
                print(f"   Requisição {i+1}: ERRO {response.status_code}")
                
        except Exception as e:
            print(f"   Requisição {i+1}: ERRO {e}")
    
    if times:
        print(f"\nEstatísticas:")
        print(f"   Tempo médio: {statistics.mean(times):.3f}s")
        print(f"   Tempo mínimo: {min(times):.3f}s")
        print(f"   Tempo máximo: {max(times):.3f}s")
        print(f"   Desvio padrão: {statistics.stdev(times) if len(times) > 1 else 0:.3f}s")
    
    # Teste 4: Forçar refresh
    print("\nTeste 4: Forçar refresh (bypass cache)")
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/api/current-candle", params={
            'symbol': symbol,
            'timeframe': timeframe,
            'force_refresh': 'true'
        }, timeout=10)
        
        elapsed = time.time() - start_time
        print(f"Tempo: {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCESSO!")
            print(f"   Preco: ${data['close']:,.2f}")
            print(f"   Cache: {data.get('cached', 'N/A')}")
        else:
            print(f"ERRO: {response.status_code}")
            
    except Exception as e:
        print(f"ERRO: {e}")
    
    # Teste 5: Status do cache
    print("\nTeste 5: Status do cache")
    try:
        response = requests.get(f"{base_url}/api/cache/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("Status do Cache:")
            print(f"   Total em cache: {data['total_cached']}")
            print(f"   Caches ativos: {data['active_caches']}")
            print(f"   Caches expirados: {data['expired_caches']}")
            print(f"   Timeout: {data['cache_timeout']}s")
            print(f"   Símbolos: {data['cached_symbols']}")
        else:
            print(f"ERRO ao obter status: {response.status_code}")
    except Exception as e:
        print(f"ERRO: {e}")
    
    # Teste 6: Diferentes símbolos
    print("\nTeste 6: Diferentes símbolos")
    symbols = ["BINANCE:ETHUSDT", "BINANCE:ADAUSDT"]
    
    for test_symbol in symbols:
        start_time = time.time()
        try:
            response = requests.get(f"{base_url}/api/current-candle", params={
                'symbol': test_symbol,
                'timeframe': '1m'
            }, timeout=10)
            
            elapsed = time.time() - start_time
            print(f"   {test_symbol}: {elapsed:.2f}s - Status: {response.status_code}")
            
        except Exception as e:
            print(f"   {test_symbol}: ERRO {e}")
    
    print("\nTeste de Performance Concluído!")
    print("\nDicas de otimização:")
    print("   - Use cache para requisições frequentes")
    print("   - Use force_refresh=true apenas quando necessário")
    print("   - Monitore o status do cache com /api/cache/status")
    print("   - Limpe o cache com /api/cache/clear se necessário")

if __name__ == "__main__":
    test_performance()

