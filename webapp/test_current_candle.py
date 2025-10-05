#!/usr/bin/env python3
"""
Script de teste para a API de Current Candle
Testa a rota /api/current-candle
"""

import requests
import json
import time
from datetime import datetime

def test_current_candle_api():
    """Testa a API de current candle"""
    base_url = "http://localhost:5000"
    
    print("Testando API de Current Candle")
    print("=" * 50)
    
    # Verificar se o servidor está rodando
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("OK - Servidor está rodando")
        else:
            print("ERRO - Servidor não está respondendo corretamente")
            return
    except requests.exceptions.RequestException as e:
        print(f"ERRO - Erro ao conectar com o servidor: {e}")
        print("DICA - Certifique-se de que o servidor está rodando: python app.py")
        return
    
    print("\nTestando Current Candle...")
    
    # Teste 1: Bitcoin 1 minuto
    print("\nTeste 1: Bitcoin 1 minuto")
    test_symbol = "BINANCE:BTCUSDT"
    test_timeframe = "1m"
    
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/api/current-candle", params={
            'symbol': test_symbol,
            'timeframe': test_timeframe
        }, timeout=15)
        
        elapsed = time.time() - start_time
        print(f"Tempo: {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCESSO!")
            print(f"   Simbolo: {data['symbol']}")
            print(f"   Timeframe: {data['timeframe']}")
            print(f"   Preco: ${data['close']:,.2f}")
            print(f"   Abertura: ${data['open']:,.2f}")
            print(f"   Maxima: ${data['high']:,.2f}")
            print(f"   Minima: ${data['low']:,.2f}")
            print(f"   Volume: {data['volume']:,.2f}")
            print(f"   Mudanca: ${data['price_change']:+,.2f} ({data['price_change_percent']:+.2f}%)")
            print(f"   Status: {'Positivo' if data['is_positive'] else 'Negativo'}")
            print(f"   Timestamp: {data['datetime']}")
        else:
            print(f"ERRO: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Detalhes: {error_data}")
            except:
                print(f"   Resposta: {response.text}")
                
    except requests.exceptions.Timeout:
        print("TIMEOUT - A requisicao demorou muito para responder")
    except Exception as e:
        print(f"ERRO na requisicao: {e}")
    
    # Teste 2: Ethereum 5 minutos
    print("\nTeste 2: Ethereum 5 minutos")
    test_symbol = "BINANCE:ETHUSDT"
    test_timeframe = "5m"
    
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/api/current-candle", params={
            'symbol': test_symbol,
            'timeframe': test_timeframe
        }, timeout=15)
        
        elapsed = time.time() - start_time
        print(f"Tempo: {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCESSO!")
            print(f"   Simbolo: {data['symbol']}")
            print(f"   Preco: ${data['close']:,.2f}")
            print(f"   Mudanca: {data['price_change_percent']:+.2f}%")
        else:
            print(f"ERRO: {response.status_code}")
            
    except Exception as e:
        print(f"ERRO: {e}")
    
    # Teste 3: Erro - sem símbolo
    print("\nTeste 3: Erro - sem simbolo")
    try:
        response = requests.get(f"{base_url}/api/current-candle", timeout=5)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 400:
            data = response.json()
            print("ERRO ESPERADO!")
            print(f"   Mensagem: {data['error']}")
        else:
            print("Deveria ter retornado erro 400")
            
    except Exception as e:
        print(f"ERRO: {e}")
    
    # Teste 4: Erro - timeframe inválido
    print("\nTeste 4: Erro - timeframe invalido")
    try:
        response = requests.get(f"{base_url}/api/current-candle", params={
            'symbol': 'BINANCE:BTCUSDT',
            'timeframe': '2h'  # Timeframe inválido
        }, timeout=5)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 400:
            data = response.json()
            print("ERRO ESPERADO!")
            print(f"   Mensagem: {data['error']}")
        else:
            print("Deveria ter retornado erro 400")
            
    except Exception as e:
        print(f"ERRO: {e}")
    
    print("\nTestes concluidos!")
    print("\nExemplos de uso:")
    print(f"   curl \"{base_url}/api/current-candle?symbol=BINANCE:BTCUSDT&timeframe=1m\"")
    print(f"   curl \"{base_url}/api/current-candle?symbol=BINANCE:ETHUSDT&timeframe=5m\"")

if __name__ == "__main__":
    test_current_candle_api()
