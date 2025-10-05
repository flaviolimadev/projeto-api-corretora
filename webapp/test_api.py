#!/usr/bin/env python3
"""
Teste da API de Candles
"""

import requests
import json
import time
from datetime import datetime

# Configuração
BASE_URL = "http://localhost:5000/api"
TEST_SYMBOLS = [
    "BINANCE:BTCUSDT",
    "BINANCE:ETHUSDT", 
    "BINANCE:ADAUSDT"
]
TEST_TIMEFRAMES = ["1m", "5m", "15m", "1h", "1d"]
TEST_LIMITS = [10, 100, 500]

def test_api_endpoint(symbol, timeframe, limit):
    """Testa um endpoint específico"""
    url = f"{BASE_URL}/candles"
    params = {
        'symbol': symbol,
        'timeframe': timeframe,
        'limit': limit
    }
    
    print(f"\n🧪 Testando: {symbol} ({timeframe}) - {limit} candles")
    print(f"URL: {url}")
    print(f"Params: {params}")
    
    try:
        start_time = time.time()
        response = requests.get(url, params=params, timeout=30)
        end_time = time.time()
        
        print(f"⏱️  Tempo: {end_time - start_time:.2f}s")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sucesso!")
            print(f"   - Total candles: {data.get('total_candles', 0)}")
            print(f"   - Current candle: {'Sim' if data.get('current_candle') else 'Não'}")
            print(f"   - Generated at: {data.get('generated_at', 'N/A')}")
            
            # Mostrar alguns candles
            candles = data.get('historical_candles', [])
            if candles:
                print(f"   - Primeiro candle: {candles[0]['datetime']} - Close: ${candles[0]['close']}")
                print(f"   - Último candle: {candles[-1]['datetime']} - Close: ${candles[-1]['close']}")
            
            return True
        else:
            print(f"❌ Erro: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   - Mensagem: {error_data.get('error', 'N/A')}")
            except:
                print(f"   - Resposta: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"⏰ Timeout (30s)")
        return False
    except requests.exceptions.ConnectionError:
        print(f"🔌 Erro de conexão - Servidor não está rodando?")
        return False
    except Exception as e:
        print(f"💥 Erro inesperado: {e}")
        return False

def test_error_cases():
    """Testa casos de erro"""
    print(f"\n🚨 Testando casos de erro...")
    
    # Sem símbolo
    test_api_endpoint("", "1h", 100)
    
    # Símbolo inválido
    test_api_endpoint("BTCUSDT", "1h", 100)
    
    # Timeframe inválido
    test_api_endpoint("BINANCE:BTCUSDT", "2h", 100)
    
    # Limit muito alto
    test_api_endpoint("BINANCE:BTCUSDT", "1h", 2000)

def test_performance():
    """Testa performance com diferentes parâmetros"""
    print(f"\n⚡ Testando performance...")
    
    for limit in [10, 100, 500, 1000]:
        test_api_endpoint("BINANCE:BTCUSDT", "1h", limit)

def main():
    """Função principal"""
    print("🚀 Iniciando testes da API de Candles")
    print("=" * 50)
    
    # Verificar se o servidor está rodando
    try:
        response = requests.get(f"{BASE_URL}/candles", timeout=5)
        print("✅ Servidor está rodando")
    except:
        print("❌ Servidor não está rodando!")
        print("   Execute: cd tradingview-scraper/webapp && python app.py")
        return
    
    # Testes básicos
    print(f"\n📊 Testes básicos...")
    success_count = 0
    total_tests = 0
    
    for symbol in TEST_SYMBOLS[:1]:  # Apenas Bitcoin para teste rápido
        for timeframe in TEST_TIMEFRAMES[:2]:  # Apenas 1m e 1h
            for limit in [10, 100]:
                total_tests += 1
                if test_api_endpoint(symbol, timeframe, limit):
                    success_count += 1
                time.sleep(1)  # Pausa entre requests
    
    # Testes de erro
    test_error_cases()
    
    # Teste de performance
    test_performance()
    
    # Resumo
    print(f"\n📈 Resumo dos Testes")
    print("=" * 30)
    print(f"✅ Sucessos: {success_count}/{total_tests}")
    print(f"❌ Falhas: {total_tests - success_count}/{total_tests}")
    print(f"📊 Taxa de sucesso: {(success_count/total_tests)*100:.1f}%")
    
    if success_count == total_tests:
        print(f"\n🎉 Todos os testes passaram! API funcionando perfeitamente!")
    else:
        print(f"\n⚠️  Alguns testes falharam. Verifique os logs acima.")

if __name__ == "__main__":
    main()
