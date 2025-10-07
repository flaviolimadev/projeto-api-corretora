"""
Testar API REST do banco de dados
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5001"

def test_endpoint(endpoint, description):
    """Testar um endpoint da API"""
    print(f"\n{'='*60}")
    print(f"TESTANDO: {description}")
    print(f"URL: {BASE_URL}{endpoint}")
    print(f"{'='*60}")
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCESSO - Status: {response.status_code}")
            
            # Mostrar informações relevantes
            if 'categories' in data:
                print(f"📊 Categorias: {data.get('total', 0)}")
                for cat in data['categories'][:3]:  # Mostrar apenas 3
                    print(f"   - {cat['key']}: {cat['name']}")
            
            elif 'assets' in data:
                print(f"📈 Ativos: {data.get('total', 0)}")
                for asset in data['assets'][:3]:  # Mostrar apenas 3
                    print(f"   - {asset['symbol']}: {asset['description']}")
            
            elif 'current_candles' in data:
                print(f"🕐 Candles atuais: {data.get('total', 0)}")
                for candle in data['current_candles'][:3]:  # Mostrar apenas 3
                    print(f"   - {candle['symbol']}: ${candle['close']:.4f}")
            
            elif 'statistics' in data:
                stats = data['statistics']
                print(f"📊 Estatísticas:")
                print(f"   - Categorias: {stats['categories']['total']}")
                print(f"   - Ativos: {stats['assets']['total']}")
                print(f"   - Candles atuais: {stats['current_candles']['total']}")
            
            elif 'status' in data:
                print(f"🏥 Status: {data['status']}")
                print(f"   - Mensagem: {data['message']}")
            
            print(f"⏰ Gerado em: {data.get('generated_at', 'N/A')}")
            
        else:
            print(f"❌ ERRO - Status: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Erro: {error_data.get('error', 'Erro desconhecido')}")
            except:
                print(f"   Resposta: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("❌ ERRO: Não foi possível conectar ao servidor")
        print("   Certifique-se de que a API está rodando na porta 5001")
    
    except Exception as e:
        print(f"❌ ERRO: {e}")


def main():
    """Executar todos os testes"""
    print("=" * 70)
    print("TESTE DA API REST DO BANCO DE DADOS")
    print("=" * 70)
    print(f"Base URL: {BASE_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    # Lista de endpoints para testar
    endpoints = [
        ("/db/health", "Health Check do Banco"),
        ("/db/statistics", "Estatísticas do Banco"),
        ("/db/categories", "Todas as Categorias"),
        ("/db/categories/crypto", "Categoria Crypto"),
        ("/db/assets", "Todos os Ativos"),
        ("/db/assets?category=crypto&limit=5", "Ativos Crypto (limitado)"),
        ("/db/current-candles", "Candles Atuais"),
        ("/db/sync-logs?limit=5", "Logs de Sincronização")
    ]
    
    # Testar cada endpoint
    for endpoint, description in endpoints:
        test_endpoint(endpoint, description)
    
    print(f"\n{'='*70}")
    print("TESTE CONCLUÍDO!")
    print(f"{'='*70}")
    print()
    print("Para iniciar a API:")
    print("  python api_database.py")
    print()
    print("Para iniciar os workers:")
    print("  python workers/main_worker.py")


if __name__ == "__main__":
    main()

