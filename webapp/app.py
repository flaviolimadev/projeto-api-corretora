"""
Flask application for real-time crypto price visualization
"""
import sys
import os
import logging
import time
from threading import Lock
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import requests as http_requests

# Add parent directory to path to import tradingview_scraper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tradingview_scraper.symbols.stream import RealTimeData, Streamer
from database.postgres_manager import postgres_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Thread lock and state management
thread_lock = Lock()
active_connections = {}
real_time_data = None
start_time = time.time()


def background_price_stream(symbol, timeframe, sid):
    """Background thread to stream real-time price data"""
    global real_time_data
    
    try:
        logger.info(f"Starting price stream for {symbol} ({timeframe}) - SID: {sid}")
        
        # Parse exchange and symbol
        exchange, ticker = symbol.split(':')
        
        # First, get historical data
        streamer = Streamer(export_result=True, export_type='json')
        historical_data = streamer.stream(
            exchange=exchange,
            symbol=ticker,
            timeframe=timeframe,
            numb_price_candles=1000  # Load last 1000 candles
        )
        
        # Send historical data to client
        if 'ohlc' in historical_data and historical_data['ohlc']:
            logger.info(f"Sending {len(historical_data['ohlc'])} historical candles for {symbol} ({timeframe})")
            for i, candle in enumerate(historical_data['ohlc']):
                if sid not in active_connections:
                    break
                    
                price_data = {
                    'timestamp': candle['timestamp'],
                    'open': float(candle['open']),
                    'high': float(candle['high']),
                    'low': float(candle['low']),
                    'close': float(candle['close']),
                    'volume': float(candle['volume'])
                }
                socketio.emit('price_update', price_data, room=sid)
                
                # Log every 100 candles
                if i % 100 == 0:
                    logger.info(f"Sent {i+1}/{len(historical_data['ohlc'])} candles")
        else:
            logger.warning(f"No historical data found for {symbol} ({timeframe})")
        
        # Now start real-time streaming
        real_time_data = RealTimeData()
        data_generator = real_time_data.get_ohlcv(exchange_symbol=symbol)
        
        # Stream data
        for packet in data_generator:
            # Check if connection is still active
            if sid not in active_connections:
                logger.info(f"Connection {sid} closed, stopping stream")
                break
                
            if packet and 'm' in packet:
                # Parse OHLCV data
                if packet['m'] == 'du' and 'p' in packet:
                    try:
                        data = packet['p']
                        if len(data) > 1 and isinstance(data[1], dict):
                            sds_data = data[1].get('sds_1', {})
                            if 's' in sds_data and len(sds_data['s']) > 0:
                                candle_data = sds_data['s'][0].get('v', [])
                                
                                if len(candle_data) >= 6:
                                    timestamp, open_price, high, low, close, volume = candle_data[:6]
                                    
                                    price_data = {
                                        'timestamp': timestamp,
                                        'open': float(open_price),
                                        'high': float(high),
                                        'low': float(low),
                                        'close': float(close),
                                        'volume': float(volume)
                                    }
                                    
                                    # Emit to specific client
                                    socketio.emit('price_update', price_data, room=sid)
                                    logger.debug(f"Sent price update: {price_data['close']}")
                    except Exception as e:
                        logger.error(f"Error parsing OHLCV data: {e}")
                        
    except Exception as e:
        logger.error(f"Error in background stream: {e}")
        socketio.emit('error', {'message': str(e)}, room=sid)
    finally:
        if sid in active_connections:
            del active_connections[sid]
        logger.info(f"Stream ended for SID: {sid}")


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/api/health')
def health_check():
    """Health check endpoint for load balancers and monitoring"""
    try:
        # Test database connection
        db_status = "healthy"
        if not postgres_manager.connect():
            db_status = "unhealthy"
        else:
            postgres_manager.disconnect()
        
        # Get basic stats
        stats = {
            'status': 'healthy' if db_status == 'healthy' else 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'database': db_status,
            'active_connections': len(active_connections),
            'cache_size': len(current_candle_cache),
            'uptime': time.time() - start_time if 'start_time' in globals() else 0
        }
        
        status_code = 200 if db_status == 'healthy' else 503
        return jsonify(stats), status_code
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 503


@app.route('/api/docs')
def api_docs():
    """API documentation endpoint"""
    docs = {
        'title': 'TradingView API',
        'version': '1.0.0',
        'description': 'API para dados de trading em tempo real',
        'endpoints': {
            'GET /api/health': 'Health check da API',
            'GET /api/candles': 'Dados históricos de candles',
            'GET /api/current-candle': 'Candle atual com cache',
            'GET /api/categories': 'Lista de categorias disponíveis',
            'GET /api/categories/<category>': 'Detalhes de uma categoria',
            'GET /api/category-assets': 'Ativos de uma categoria',
            'GET /api/search-symbols': 'Buscar símbolos',
            'GET /api/cache/status': 'Status do cache',
            'GET /api/cache/clear': 'Limpar cache',
            'WebSocket /socket.io/': 'Stream de dados em tempo real'
        },
        'parameters': {
            'symbol': 'Formato: EXCHANGE:SYMBOL (ex: BINANCE:BTCUSDT)',
            'timeframe': '1m, 5m, 15m, 30m, 1h, 2h, 4h, 1d, 1w, 1M',
            'limit': 'Número máximo de resultados (padrão: 1000)',
            'category': 'crypto, forex, stocks, indices, commodities, bonds, etfs, futures',
            'exchange': 'BINANCE, NASDAQ, NYSE, FXOPEN, etc.'
        },
        'examples': {
            'candles': '/api/candles?symbol=BINANCE:BTCUSDT&timeframe=1h&limit=100',
            'current_candle': '/api/current-candle?symbol=BINANCE:BTCUSDT&timeframe=1m',
            'categories': '/api/categories',
            'category_assets': '/api/category-assets?category=crypto&exchange=BINANCE&limit=20'
        }
    }
    return jsonify(docs)


@app.route('/api/search-symbols')
def search_symbols():
    """Search for symbols based on query"""
    query = request.args.get('q', '')
    
    if not query or len(query) < 2:
        return jsonify([])
    
    try:
        # TradingView symbol search API
        url = f"https://symbol-search.tradingview.com/symbol_search/?text={query}&type="
        response = http_requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            # Format results
            results = []
            for item in data[:15]:  # Limit to 15 results
                symbol = item.get('symbol', '')
                exchange = item.get('exchange', '')
                description = item.get('description', '')
                type_name = item.get('type', '')
                
                if exchange and symbol:
                    results.append({
                        'symbol': f"{exchange}:{symbol}",
                        'description': description,
                        'type': type_name,
                        'exchange': exchange
                    })
            
            return jsonify(results)
        else:
            return jsonify([])
    except Exception as e:
        logger.error(f"Error searching symbols: {e}")
        return jsonify([])

@app.route('/api/candles')
def get_candles():
    """
    API para obter dados de candles históricos e atuais
    
    Parâmetros:
    - symbol: Símbolo no formato EXCHANGE:SYMBOL (ex: BINANCE:BTCUSDT)
    - timeframe: Timeframe (1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1M)
    - limit: Número de candles (padrão: 1000, máximo: 1000)
    
    Exemplo:
    GET /api/candles?symbol=BINANCE:BTCUSDT&timeframe=1h&limit=500
    """
    try:
        # Obter parâmetros
        symbol = request.args.get('symbol', '').strip()
        timeframe = request.args.get('timeframe', '1m').strip()
        limit = min(int(request.args.get('limit', 1000)), 1000)  # Máximo 1000
        
        # Validar parâmetros obrigatórios
        if not symbol:
            return jsonify({
                'error': 'Parâmetro "symbol" é obrigatório',
                'example': '/api/candles?symbol=BINANCE:BTCUSDT&timeframe=1h'
            }), 400
        
        if ':' not in symbol:
            return jsonify({
                'error': 'Formato de símbolo inválido',
                'expected': 'EXCHANGE:SYMBOL (ex: BINANCE:BTCUSDT)',
                'received': symbol
            }), 400
        
        # Validar timeframe
        valid_timeframes = ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '1d', '1w', '1M']
        if timeframe not in valid_timeframes:
            return jsonify({
                'error': 'Timeframe inválido',
                'valid_timeframes': valid_timeframes,
                'received': timeframe
            }), 400
        
        logger.info(f"API Request: {symbol} ({timeframe}) - {limit} candles from database")
        
        # Conectar ao banco
        if not postgres_manager.connect():
            return jsonify({
                'error': 'Falha ao conectar ao banco de dados'
            }), 500
        
        # Buscar candles históricos do banco
        candles_db = postgres_manager.get_candles(symbol, timeframe, limit)
        postgres_manager.disconnect()
        
        # Converter para formato da API
        candles = []
        for candle_db in candles_db:
            candle = {
                'timestamp': candle_db['timestamp'],
                'datetime': candle_db['datetime'].isoformat() if hasattr(candle_db['datetime'], 'isoformat') else str(candle_db['datetime']),
                'open': candle_db['open'],
                'high': candle_db['high'],
                'low': candle_db['low'],
                'close': candle_db['close'],
                'volume': candle_db['volume']
            }
            candles.append(candle)
        
        # Ordenar por timestamp (mais recente primeiro)
        candles.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Preparar resposta
        response_data = {
            'symbol': symbol,
            'timeframe': timeframe,
            'total_candles': len(candles),
            'historical_candles': candles,
            'generated_at': datetime.now().isoformat(),
            'timezone': 'UTC',
            'source': 'database'
        }
        
        logger.info(f"API Response: {len(candles)} candles from database")
        
        return jsonify(response_data)
        
    except ValueError as e:
        return jsonify({
            'error': 'Parâmetro inválido',
            'details': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Error in /api/candles: {e}")
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500


# Cache para candles atuais
current_candle_cache = {}
cache_timeout = 5  # 5 segundos de cache

@app.route('/api/current-candle')
def get_current_candle():
    """
    API otimizada para obter apenas o candle atual com cache
    
    Parâmetros:
    - symbol: Símbolo no formato EXCHANGE:SYMBOL (ex: BINANCE:BTCUSDT)
    - timeframe: Timeframe (1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1M)
    - force_refresh: true para forçar atualização (opcional)
    
    Exemplo:
    GET /api/current-candle?symbol=BINANCE:BTCUSDT&timeframe=1m
    """
    try:
        # Obter parâmetros
        symbol = request.args.get('symbol', '').strip()
        timeframe = request.args.get('timeframe', '1m').strip()
        force_refresh = request.args.get('force_refresh', 'false').lower() == 'true'
        
        # Validar parâmetros obrigatórios
        if not symbol:
            return jsonify({
                'error': 'Parâmetro "symbol" é obrigatório',
                'example': '/api/current-candle?symbol=BINANCE:BTCUSDT&timeframe=1m'
            }), 400
        
        if ':' not in symbol:
            return jsonify({
                'error': 'Formato de símbolo inválido',
                'expected': 'EXCHANGE:SYMBOL (ex: BINANCE:BTCUSDT)',
                'received': symbol
            }), 400
        
        # Validar timeframe
        valid_timeframes = ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '1d', '1w', '1M']
        if timeframe not in valid_timeframes:
            return jsonify({
                'error': 'Timeframe inválido',
                'valid_timeframes': valid_timeframes,
                'received': timeframe
            }), 400
        
        cache_key = f"{symbol}_{timeframe}"
        current_time = time.time()
        
        # Verificar cache primeiro
        if not force_refresh and cache_key in current_candle_cache:
            cached_data = current_candle_cache[cache_key]
            if current_time - cached_data['timestamp'] < cache_timeout:
                logger.info(f"Cache hit for {symbol} ({timeframe})")
                return jsonify(cached_data['data'])
        
        logger.info(f"Current Candle Request: {symbol} ({timeframe}) from database")
        
        # Conectar ao banco
        if not postgres_manager.connect():
            return jsonify({
                'error': 'Falha ao conectar ao banco de dados'
            }), 500
        
        # Buscar candle atual do banco
        current_candle_db = postgres_manager.get_current_candle(symbol)
        postgres_manager.disconnect()
        
        if not current_candle_db:
            return jsonify({
                'error': 'Candle atual não encontrado no banco',
                'symbol': symbol,
                'timeframe': timeframe
            }), 404
        
        # Converter para formato da API
        current_candle = {
            'symbol': current_candle_db['symbol'],
            'timeframe': current_candle_db['timeframe'],
            'timestamp': current_candle_db['timestamp'],
            'datetime': current_candle_db['datetime'].isoformat() if hasattr(current_candle_db['datetime'], 'isoformat') else str(current_candle_db['datetime']),
            'open': current_candle_db['open'],
            'high': current_candle_db['high'],
            'low': current_candle_db['low'],
            'close': current_candle_db['close'],
            'volume': current_candle_db['volume'],
            'price_change': current_candle_db['priceChange'],
            'price_change_percent': current_candle_db['priceChangePercent'],
            'is_positive': current_candle_db['isPositive'],
            'generated_at': datetime.now().isoformat(),
            'timezone': 'UTC',
            'source': 'database',
            'last_update': current_candle_db['lastUpdate'].isoformat() if hasattr(current_candle_db['lastUpdate'], 'isoformat') else str(current_candle_db['lastUpdate'])
        }
        
        logger.info(f"Current Candle Response: {symbol} - ${current_candle['close']} ({current_candle['price_change_percent']:+.2f}%) from database")
        return jsonify(current_candle)
        
    except ValueError as e:
        return jsonify({
            'error': 'Parâmetro inválido',
            'details': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Error in /api/current-candle: {e}")
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500


@app.route('/api/cache/status')
def get_cache_status():
    """Status do cache de candles atuais"""
    current_time = time.time()
    active_caches = 0
    expired_caches = 0
    
    for key, data in current_candle_cache.items():
        if current_time - data['timestamp'] < cache_timeout:
            active_caches += 1
        else:
            expired_caches += 1
    
    return jsonify({
        'total_cached': len(current_candle_cache),
        'active_caches': active_caches,
        'expired_caches': expired_caches,
        'cache_timeout': cache_timeout,
        'cached_symbols': list(current_candle_cache.keys())
    })


@app.route('/api/cache/clear')
def clear_cache():
    """Limpar cache de candles atuais"""
    global current_candle_cache
    old_size = len(current_candle_cache)
    current_candle_cache.clear()
    
    return jsonify({
        'message': 'Cache limpo com sucesso',
        'cleared_items': old_size,
        'current_size': len(current_candle_cache)
    })


@app.route('/api/categories')
def get_categories():
    """
    API para obter todas as categorias do banco de dados
    
    Retorna categorias armazenadas no PostgreSQL
    """
    try:
        logger.info("Categories Request: Getting categories from database")
        
        # Conectar ao banco e obter categorias
        if not postgres_manager.connect():
            return jsonify({
                'error': 'Falha ao conectar ao banco de dados'
            }), 500
        
        categories_db = postgres_manager.get_all_categories()
        postgres_manager.disconnect()
        
        # Converter para formato da API original
        categories = {}
        for cat in categories_db:
            categories[cat['key']] = {
                'name': cat['name'],
                'description': cat['description'],
                'icon': cat['icon'],
                'exchanges': cat['exchanges'],
                'timeframes': cat['timeframes'],
                'popular_symbols': []  # Será preenchido pelos ativos
            }
        
        # Adicionar símbolos populares baseados nos ativos do banco
        if postgres_manager.connect():
            for category_key in categories.keys():
                assets = postgres_manager.get_assets_by_category(category_key)
                popular_symbols = [asset['symbol'] for asset in assets[:10]]  # Top 10
                categories[category_key]['popular_symbols'] = popular_symbols
            postgres_manager.disconnect()
        
        # Adicionar estatísticas
        total_categories = len(categories)
        total_exchanges = len(set(exchange for cat in categories.values() for exchange in cat['exchanges']))
        total_symbols = sum(len(cat['popular_symbols']) for cat in categories.values())
        
        response_data = {
            'categories': categories,
            'statistics': {
                'total_categories': total_categories,
                'total_exchanges': total_exchanges,
                'total_popular_symbols': total_symbols,
                'supported_timeframes': ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']
            },
            'generated_at': datetime.now().isoformat(),
            'timezone': 'UTC',
            'source': 'database'
        }
        
        logger.info(f"Categories Response: {total_categories} categories from database")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error in /api/categories: {e}")
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500


@app.route('/api/categories/<category_name>')
def get_category_details(category_name):
    """
    API para obter detalhes de uma categoria específica
    
    Parâmetros:
    - category_name: Nome da categoria (forex, crypto, stocks, etc.)
    """
    try:
        logger.info(f"Category Details Request: {category_name}")
        
        # Obter todas as categorias
        categories_response = get_categories()
        if isinstance(categories_response, tuple):  # Se retornou erro
            return categories_response
            
        categories_data = categories_response.get_json()
        categories = categories_data['categories']
        
        if category_name not in categories:
            return jsonify({
                'error': 'Categoria não encontrada',
                'available_categories': list(categories.keys()),
                'received': category_name
            }), 404
        
        category = categories[category_name]
        
        # Adicionar informações extras
        category['total_symbols'] = len(category['popular_symbols'])
        category['total_exchanges'] = len(category['exchanges'])
        
        logger.info(f"Category Details Response: {category_name} - {category['total_symbols']} symbols")
        return jsonify(category)
        
    except Exception as e:
        logger.error(f"Error in /api/categories/{category_name}: {e}")
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500


@app.route('/api/category-assets')
def get_category_assets():
    """
    API para obter todos os ativos de uma categoria específica do banco de dados
    
    Parâmetros:
    - category: Nome da categoria (forex, crypto, stocks, etc.)
    - exchange: Nome da exchange (BINANCE, NASDAQ, NYSE, etc.)
    - limit: Número máximo de ativos (padrão: 50, máximo: 200)
    - search: Termo de busca opcional para filtrar ativos
    
    Exemplo:
    GET /api/category-assets?category=crypto&exchange=BINANCE&limit=20
    """
    try:
        # Obter parâmetros
        category = request.args.get('category', '').strip().lower()
        exchange = request.args.get('exchange', '').strip().upper()
        limit = min(int(request.args.get('limit', 50)), 200)  # Máximo 200
        search_term = request.args.get('search', '').strip()
        
        # Validar parâmetros obrigatórios
        if not category:
            return jsonify({
                'error': 'Parâmetro "category" é obrigatório',
                'example': '/api/category-assets?category=crypto&exchange=BINANCE'
            }), 400
        
        if not exchange:
            return jsonify({
                'error': 'Parâmetro "exchange" é obrigatório',
                'example': '/api/category-assets?category=crypto&exchange=BINANCE'
            }), 400
        
        logger.info(f"Category Assets Request: {category} from {exchange} (limit: {limit})")
        
        # Conectar ao banco
        if not postgres_manager.connect():
            return jsonify({
                'error': 'Falha ao conectar ao banco de dados'
            }), 500
        
        # Verificar se a categoria existe
        category_db = postgres_manager.get_category_by_key(category)
        if not category_db:
            postgres_manager.disconnect()
            return jsonify({
                'error': 'Categoria não encontrada',
                'received': category
            }), 404
        
        # Verificar se a exchange é válida para esta categoria
        if exchange not in category_db['exchanges']:
            postgres_manager.disconnect()
            return jsonify({
                'error': 'Exchange não suportada para esta categoria',
                'category': category,
                'supported_exchanges': category_db['exchanges'],
                'received': exchange
            }), 400
        
        # Buscar ativos do banco
        assets_db = postgres_manager.get_assets_by_category(category)
        
        # Filtrar por exchange
        assets_filtered = [asset for asset in assets_db if asset['exchange'].upper() == exchange]
        
        # Filtrar por termo de busca se fornecido
        if search_term:
            search_lower = search_term.lower()
            assets_filtered = [
                asset for asset in assets_filtered 
                if (search_lower in asset['symbol'].lower() or 
                    search_lower in asset['description'].lower() or
                    search_lower in asset['ticker'].lower())
            ]
        
        # Limitar resultados
        assets_filtered = assets_filtered[:limit]
        
        # Converter para formato da API
        assets = []
        for asset_db in assets_filtered:
            asset = {
                'symbol': asset_db['symbol'],
                'exchange': asset_db['exchange'],
                'description': asset_db['description'],
                'type': asset_db['type'],
                'category': category,
                'ticker': asset_db['ticker'],
                'search_query': asset_db.get('searchQuery', '')
            }
            assets.append(asset)
        
        postgres_manager.disconnect()
        
        response_data = {
            'category': category,
            'exchange': exchange,
            'total_assets': len(assets),
            'limit': limit,
            'search_term': search_term,
            'assets': assets,
            'category_info': {
                'name': category_db['name'],
                'description': category_db['description'],
                'supported_exchanges': category_db['exchanges']
            },
            'generated_at': datetime.now().isoformat(),
            'timezone': 'UTC',
            'source': 'database'
        }
        
        logger.info(f"Category Assets Response: {len(assets)} assets found for {category} on {exchange} from database")
        return jsonify(response_data)
        
    except ValueError as e:
        return jsonify({
            'error': 'Parâmetro inválido',
            'details': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Error in /api/category-assets: {e}")
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500


def generate_search_queries(category, exchange, search_term):
    """Gerar queries de busca baseadas na categoria e exchange"""
    queries = []
    
    if search_term:
        # Se há termo de busca, usar ele
        queries.append(search_term)
    else:
        # Gerar queries baseadas na categoria e exchange
        if category == 'crypto':
            if exchange == 'BINANCE':
                queries = ['BTC', 'ETH', 'ADA', 'DOT', 'LINK', 'UNI', 'LTC', 'BCH', 'XRP', 'BNB']
            elif exchange == 'COINBASE':
                queries = ['BTC', 'ETH', 'ADA', 'DOT', 'LINK', 'UNI', 'LTC', 'BCH', 'XRP']
            else:
                queries = ['BTC', 'ETH', 'ADA', 'DOT', 'LINK']
        elif category == 'forex':
            queries = ['EUR', 'GBP', 'USD', 'JPY', 'CHF', 'AUD', 'CAD', 'NZD']
        elif category == 'stocks':
            if exchange == 'NASDAQ':
                queries = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'AMD', 'INTC']
            elif exchange == 'NYSE':
                queries = ['JPM', 'JNJ', 'V', 'PG', 'UNH', 'HD', 'MA', 'DIS', 'PYPL', 'ADBE']
            else:
                queries = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
        elif category == 'indices':
            queries = ['SPX', 'NDX', 'DJI', 'RUT', 'VIX', 'COMP']
        elif category == 'commodities':
            queries = ['GC', 'SI', 'CL', 'NG', 'ZC', 'ZS', 'ZW']
        elif category == 'bonds':
            queries = ['TY', 'US', 'UB', 'FGBL', 'FGBM', 'FGBS']
        elif category == 'etfs':
            queries = ['SPY', 'QQQ', 'IWM', 'VTI', 'VEA', 'VWO', 'GLD', 'SLV', 'TLT', 'HYG']
        elif category == 'futures':
            queries = ['ES', 'NQ', 'YM', 'RTY', 'ZC', 'ZS', 'CL', 'NG', 'GC', 'SI']
    
    return queries


def is_valid_asset_for_category(symbol, category, exchange):
    """Verificar se um símbolo é válido para a categoria"""
    symbol_upper = symbol.upper()
    
    if category == 'crypto':
        # Para crypto, aceitar símbolos que terminam com USDT, BTC, ETH, etc.
        crypto_suffixes = ['USDT', 'BTC', 'ETH', 'BNB', 'ADA', 'DOT', 'LINK', 'UNI', 'LTC', 'BCH', 'XRP']
        return any(symbol_upper.endswith(suffix) for suffix in crypto_suffixes)
    
    elif category == 'forex':
        # Para forex, aceitar pares de moedas
        forex_pairs = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'AUDUSD', 'USDCAD', 'NZDUSD', 'EURGBP', 'EURJPY', 'GBPJPY']
        return any(pair in symbol_upper for pair in forex_pairs)
    
    elif category == 'stocks':
        # Para stocks, aceitar símbolos de 1-5 caracteres
        return 1 <= len(symbol) <= 5 and symbol_upper.isalpha()
    
    elif category == 'indices':
        # Para índices, aceitar símbolos conhecidos
        index_symbols = ['SPX', 'NDX', 'DJI', 'RUT', 'VIX', 'COMP', 'ES', 'NQ', 'YM', 'RTY']
        return any(index in symbol_upper for index in index_symbols)
    
    elif category == 'commodities':
        # Para commodities, aceitar símbolos conhecidos
        commodity_symbols = ['GC', 'SI', 'CL', 'NG', 'ZC', 'ZS', 'ZW', 'CAD', 'ALI', 'ZNI']
        return any(commodity in symbol_upper for commodity in commodity_symbols)
    
    elif category == 'bonds':
        # Para bonds, aceitar símbolos conhecidos
        bond_symbols = ['TY', 'US', 'UB', 'FGBL', 'FGBM', 'FGBS', 'JGB']
        return any(bond in symbol_upper for bond in bond_symbols)
    
    elif category == 'etfs':
        # Para ETFs, aceitar símbolos conhecidos
        etf_symbols = ['SPY', 'QQQ', 'IWM', 'VTI', 'VEA', 'VWO', 'GLD', 'SLV', 'TLT', 'HYG']
        return any(etf in symbol_upper for etf in etf_symbols)
    
    elif category == 'futures':
        # Para futures, aceitar símbolos que terminam com !
        return symbol_upper.endswith('!')
    
    return True  # Por padrão, aceitar todos os símbolos


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info(f"Client connected: {request.sid}")
    active_connections[request.sid] = True
    emit('connected', {'status': 'connected'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {request.sid}")
    if request.sid in active_connections:
        del active_connections[request.sid]


@socketio.on('start_stream')
def handle_start_stream(data):
    """Start streaming price data for a symbol"""
    symbol = data.get('symbol', 'BINANCE:BTCUSDT')
    timeframe = data.get('timeframe', '1m')
    
    logger.info(f"Starting stream for {symbol} ({timeframe}) - SID: {request.sid}")
    
    # Start background thread
    socketio.start_background_task(background_price_stream, symbol, timeframe, request.sid)
    emit('stream_started', {'symbol': symbol, 'timeframe': timeframe})


@socketio.on('stop_stream')
def handle_stop_stream():
    """Stop streaming price data"""
    logger.info(f"Stopping stream for SID: {request.sid}")
    if request.sid in active_connections:
        del active_connections[request.sid]
    emit('stream_stopped', {'status': 'stopped'})


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)

