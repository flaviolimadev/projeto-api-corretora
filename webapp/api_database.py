"""
API REST para servir dados do banco PostgreSQL
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from datetime import datetime
import sys
import os

# Adicionar o diretório pai ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.postgres_manager import postgres_manager

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar app Flask
app = Flask(__name__)
CORS(app)

# ===== CATEGORIES =====

@app.route('/db/categories', methods=['GET'])
def get_db_categories():
    """Obter todas as categorias do banco"""
    try:
        if not postgres_manager.connect():
            return jsonify({'error': 'Falha ao conectar ao banco'}), 500
        
        categories = postgres_manager.get_all_categories()
        postgres_manager.disconnect()
        
        return jsonify({
            'categories': categories,
            'total': len(categories),
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro em /db/categories: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/db/categories/<category_key>', methods=['GET'])
def get_db_category(category_key):
    """Obter categoria específica do banco"""
    try:
        if not postgres_manager.connect():
            return jsonify({'error': 'Falha ao conectar ao banco'}), 500
        
        category = postgres_manager.get_category_by_key(category_key)
        postgres_manager.disconnect()
        
        if not category:
            return jsonify({'error': 'Categoria não encontrada'}), 404
        
        return jsonify({
            'category': category,
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro em /db/categories/{category_key}: {e}")
        return jsonify({'error': str(e)}), 500


# ===== ASSETS =====

@app.route('/db/assets', methods=['GET'])
def get_db_assets():
    """Obter todos os ativos do banco"""
    try:
        # Parâmetros
        limit = int(request.args.get('limit', 100))
        category = request.args.get('category', '').strip()
        exchange = request.args.get('exchange', '').strip()
        
        if not postgres_manager.connect():
            return jsonify({'error': 'Falha ao conectar ao banco'}), 500
        
        if category:
            assets = postgres_manager.get_assets_by_category(category)
        else:
            assets = postgres_manager.get_all_assets(limit=limit)
        
        # Filtrar por exchange se especificado
        if exchange:
            assets = [asset for asset in assets if asset['exchange'].upper() == exchange.upper()]
        
        postgres_manager.disconnect()
        
        return jsonify({
            'assets': assets,
            'total': len(assets),
            'filters': {
                'category': category,
                'exchange': exchange,
                'limit': limit
            },
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro em /db/assets: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/db/assets/<symbol>', methods=['GET'])
def get_db_asset(symbol):
    """Obter ativo específico do banco"""
    try:
        if not postgres_manager.connect():
            return jsonify({'error': 'Falha ao conectar ao banco'}), 500
        
        asset = postgres_manager.get_asset_by_symbol(symbol)
        postgres_manager.disconnect()
        
        if not asset:
            return jsonify({'error': 'Ativo não encontrado'}), 404
        
        return jsonify({
            'asset': asset,
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro em /db/assets/{symbol}: {e}")
        return jsonify({'error': str(e)}), 500


# ===== CANDLES =====

@app.route('/db/candles', methods=['GET'])
def get_db_candles():
    """Obter candles históricos do banco"""
    try:
        # Parâmetros obrigatórios
        symbol = request.args.get('symbol', '').strip()
        timeframe = request.args.get('timeframe', '1m').strip()
        limit = int(request.args.get('limit', 1000))
        
        if not symbol:
            return jsonify({'error': 'Parâmetro "symbol" é obrigatório'}), 400
        
        if not postgres_manager.connect():
            return jsonify({'error': 'Falha ao conectar ao banco'}), 500
        
        candles = postgres_manager.get_candles(symbol, timeframe, limit)
        postgres_manager.disconnect()
        
        return jsonify({
            'candles': candles,
            'total': len(candles),
            'symbol': symbol,
            'timeframe': timeframe,
            'limit': limit,
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro em /db/candles: {e}")
        return jsonify({'error': str(e)}), 500


# ===== CURRENT CANDLES =====

@app.route('/db/current-candles', methods=['GET'])
def get_db_current_candles():
    """Obter todos os candles atuais do banco"""
    try:
        # Parâmetros opcionais
        symbol = request.args.get('symbol', '').strip()
        limit = int(request.args.get('limit', 100))
        
        if not postgres_manager.connect():
            return jsonify({'error': 'Falha ao conectar ao banco'}), 500
        
        if symbol:
            current_candle = postgres_manager.get_current_candle(symbol)
            current_candles = [current_candle] if current_candle else []
        else:
            current_candles = postgres_manager.get_all_current_candles()
            current_candles = current_candles[:limit]
        
        postgres_manager.disconnect()
        
        return jsonify({
            'current_candles': current_candles,
            'total': len(current_candles),
            'filters': {
                'symbol': symbol,
                'limit': limit
            },
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro em /db/current-candles: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/db/current-candles/<symbol>', methods=['GET'])
def get_db_current_candle(symbol):
    """Obter candle atual específico do banco"""
    try:
        if not postgres_manager.connect():
            return jsonify({'error': 'Falha ao conectar ao banco'}), 500
        
        current_candle = postgres_manager.get_current_candle(symbol)
        postgres_manager.disconnect()
        
        if not current_candle:
            return jsonify({'error': 'Candle atual não encontrado'}), 404
        
        return jsonify({
            'current_candle': current_candle,
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro em /db/current-candles/{symbol}: {e}")
        return jsonify({'error': str(e)}), 500


# ===== SYNC LOGS =====

@app.route('/db/sync-logs', methods=['GET'])
def get_db_sync_logs():
    """Obter logs de sincronização do banco"""
    try:
        limit = int(request.args.get('limit', 50))
        
        if not postgres_manager.connect():
            return jsonify({'error': 'Falha ao conectar ao banco'}), 500
        
        logs = postgres_manager.get_recent_sync_logs(limit)
        postgres_manager.disconnect()
        
        return jsonify({
            'sync_logs': logs,
            'total': len(logs),
            'limit': limit,
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro em /db/sync-logs: {e}")
        return jsonify({'error': str(e)}), 500


# ===== STATISTICS =====

@app.route('/db/statistics', methods=['GET'])
def get_db_statistics():
    """Obter estatísticas do banco"""
    try:
        if not postgres_manager.connect():
            return jsonify({'error': 'Falha ao conectar ao banco'}), 500
        
        categories = postgres_manager.get_all_categories()
        assets = postgres_manager.get_all_assets(limit=10000)
        current_candles = postgres_manager.get_all_current_candles()
        recent_logs = postgres_manager.get_recent_sync_logs(limit=10)
        
        postgres_manager.disconnect()
        
        # Calcular estatísticas
        stats = {
            'categories': {
                'total': len(categories),
                'list': [cat['key'] for cat in categories]
            },
            'assets': {
                'total': len(assets),
                'by_category': {},
                'by_exchange': {}
            },
            'current_candles': {
                'total': len(current_candles),
                'updated_recently': len([c for c in current_candles if c['lastUpdate']])
            },
            'sync_logs': {
                'total_recent': len(recent_logs),
                'last_sync': recent_logs[0]['startedAt'] if recent_logs else None
            }
        }
        
        # Estatísticas por categoria
        for asset in assets:
            category = asset['categoryKey']
            if category not in stats['assets']['by_category']:
                stats['assets']['by_category'][category] = 0
            stats['assets']['by_category'][category] += 1
        
        # Estatísticas por exchange
        for asset in assets:
            exchange = asset['exchange']
            if exchange not in stats['assets']['by_exchange']:
                stats['assets']['by_exchange'][exchange] = 0
            stats['assets']['by_exchange'][exchange] += 1
        
        return jsonify({
            'statistics': stats,
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro em /db/statistics: {e}")
        return jsonify({'error': str(e)}), 500


# ===== HEALTH CHECK =====

@app.route('/db/health', methods=['GET'])
def get_db_health():
    """Verificar saúde do banco de dados"""
    try:
        if not postgres_manager.connect():
            return jsonify({
                'status': 'error',
                'message': 'Falha ao conectar ao banco',
                'timestamp': datetime.now().isoformat()
            }), 500
        
        # Teste simples
        categories = postgres_manager.get_all_categories()
        postgres_manager.disconnect()
        
        return jsonify({
            'status': 'healthy',
            'message': 'Banco de dados funcionando',
            'categories_count': len(categories),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("API REST DO BANCO DE DADOS")
    print("=" * 60)
    print()
    print("Endpoints disponíveis:")
    print("  GET /db/categories - Todas as categorias")
    print("  GET /db/categories/<key> - Categoria específica")
    print("  GET /db/assets - Todos os ativos")
    print("  GET /db/assets/<symbol> - Ativo específico")
    print("  GET /db/candles?symbol=X&timeframe=Y - Candles históricos")
    print("  GET /db/current-candles - Candles atuais")
    print("  GET /db/current-candles/<symbol> - Candle atual específico")
    print("  GET /db/sync-logs - Logs de sincronização")
    print("  GET /db/statistics - Estatísticas do banco")
    print("  GET /db/health - Health check")
    print()
    print("Iniciando servidor na porta 5001...")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5001, debug=True)
