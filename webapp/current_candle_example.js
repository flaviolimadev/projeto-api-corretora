/**
 * Exemplo de uso da API Current Candle
 * Demonstra como consumir a rota /api/current-candle
 */

// Configuração
const API_BASE_URL = 'http://localhost:5000';
const DEFAULT_SYMBOL = 'BINANCE:BTCUSDT';
const DEFAULT_TIMEFRAME = '1m';

/**
 * Obter candle atual
 * @param {string} symbol - Símbolo (ex: BINANCE:BTCUSDT)
 * @param {string} timeframe - Timeframe (ex: 1m, 5m, 1h)
 * @returns {Promise<Object>} Dados do candle atual
 */
async function getCurrentCandle(symbol = DEFAULT_SYMBOL, timeframe = DEFAULT_TIMEFRAME) {
    try {
        const url = `${API_BASE_URL}/api/current-candle`;
        const params = new URLSearchParams({
            symbol: symbol,
            timeframe: timeframe
        });
        
        console.log(`🔍 Buscando candle atual: ${symbol} (${timeframe})`);
        
        const response = await fetch(`${url}?${params}`);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || `HTTP ${response.status}`);
        }
        
        return data;
    } catch (error) {
        console.error('❌ Erro ao obter candle atual:', error);
        throw error;
    }
}

/**
 * Exibir dados do candle de forma formatada
 * @param {Object} candle - Dados do candle
 */
function displayCandle(candle) {
    const changeIcon = candle.is_positive ? '🟢' : '🔴';
    const changeSign = candle.price_change >= 0 ? '+' : '';
    
    console.log('\n📊 CANDLE ATUAL');
    console.log('='.repeat(40));
    console.log(`📈 Símbolo: ${candle.symbol}`);
    console.log(`⏰ Timeframe: ${candle.timeframe}`);
    console.log(`🕐 Data/Hora: ${candle.datetime}`);
    console.log('');
    console.log(`💰 Preço Atual: $${candle.close.toLocaleString('pt-BR', {minimumFractionDigits: 2})}`);
    console.log(`📊 Abertura: $${candle.open.toLocaleString('pt-BR', {minimumFractionDigits: 2})}`);
    console.log(`🔺 Máxima: $${candle.high.toLocaleString('pt-BR', {minimumFractionDigits: 2})}`);
    console.log(`🔻 Mínima: $${candle.low.toLocaleString('pt-BR', {minimumFractionDigits: 2})}`);
    console.log(`📦 Volume: ${candle.volume.toLocaleString('pt-BR', {minimumFractionDigits: 2})}`);
    console.log('');
    console.log(`💹 Mudança: ${changeIcon} ${changeSign}$${candle.price_change.toFixed(2)} (${changeSign}${candle.price_change_percent.toFixed(2)}%)`);
    console.log(`🎯 Status: ${candle.is_positive ? 'Positivo' : 'Negativo'}`);
    console.log('='.repeat(40));
}

/**
 * Atualizar preço em tempo real (simulação)
 * @param {string} symbol - Símbolo
 * @param {string} timeframe - Timeframe
 * @param {number} interval - Intervalo em milissegundos
 */
function startRealTimeUpdates(symbol = DEFAULT_SYMBOL, timeframe = DEFAULT_TIMEFRAME, interval = 10000) {
    console.log(`🚀 Iniciando atualizações em tempo real: ${symbol} (${timeframe})`);
    console.log(`⏱️  Intervalo: ${interval/1000} segundos`);
    
    // Primeira atualização imediata
    updatePrice(symbol, timeframe);
    
    // Atualizações periódicas
    setInterval(() => {
        updatePrice(symbol, timeframe);
    }, interval);
}

/**
 * Atualizar preço
 * @param {string} symbol - Símbolo
 * @param {string} timeframe - Timeframe
 */
async function updatePrice(symbol, timeframe) {
    try {
        const candle = await getCurrentCandle(symbol, timeframe);
        displayCandle(candle);
        
        // Atualizar elemento HTML se existir
        updatePriceElement(candle);
        
    } catch (error) {
        console.error('❌ Erro ao atualizar preço:', error.message);
    }
}

/**
 * Atualizar elemento HTML com o preço
 * @param {Object} candle - Dados do candle
 */
function updatePriceElement(candle) {
    const priceElement = document.getElementById('current-price');
    const changeElement = document.getElementById('price-change');
    const timeElement = document.getElementById('last-update');
    
    if (priceElement) {
        priceElement.textContent = `$${candle.close.toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
        priceElement.className = `price ${candle.is_positive ? 'positive' : 'negative'}`;
    }
    
    if (changeElement) {
        const changeSign = candle.price_change >= 0 ? '+' : '';
        changeElement.textContent = `${changeSign}${candle.price_change_percent.toFixed(2)}%`;
        changeElement.className = `change ${candle.is_positive ? 'positive' : 'negative'}`;
    }
    
    if (timeElement) {
        timeElement.textContent = new Date(candle.datetime).toLocaleString('pt-BR');
    }
}

/**
 * Comparar múltiplos símbolos
 * @param {Array} symbols - Array de símbolos
 * @param {string} timeframe - Timeframe
 */
async function compareSymbols(symbols, timeframe = DEFAULT_TIMEFRAME) {
    console.log(`🔍 Comparando ${symbols.length} símbolos (${timeframe})`);
    console.log('='.repeat(50));
    
    const promises = symbols.map(symbol => 
        getCurrentCandle(symbol, timeframe).catch(error => ({
            symbol,
            error: error.message
        }))
    );
    
    const results = await Promise.all(promises);
    
    results.forEach((result, index) => {
        if (result.error) {
            console.log(`${index + 1}. ❌ ${result.symbol}: ${result.error}`);
        } else {
            const changeIcon = result.is_positive ? '🟢' : '🔴';
            const changeSign = result.price_change >= 0 ? '+' : '';
            console.log(`${index + 1}. ${changeIcon} ${result.symbol}: $${result.close.toFixed(2)} (${changeSign}${result.price_change_percent.toFixed(2)}%)`);
        }
    });
}

/**
 * Exemplo de uso básico
 */
async function exemploBasico() {
    console.log('🚀 Exemplo Básico - Current Candle API');
    console.log('='.repeat(50));
    
    try {
        // Obter candle do Bitcoin
        const btcCandle = await getCurrentCandle('BINANCE:BTCUSDT', '1m');
        displayCandle(btcCandle);
        
        // Obter candle do Ethereum
        const ethCandle = await getCurrentCandle('BINANCE:ETHUSDT', '5m');
        displayCandle(ethCandle);
        
    } catch (error) {
        console.error('❌ Erro no exemplo básico:', error);
    }
}

/**
 * Exemplo de dashboard em tempo real
 */
function exemploDashboard() {
    console.log('📊 Exemplo Dashboard - Atualizações em Tempo Real');
    console.log('='.repeat(50));
    
    // Iniciar atualizações para Bitcoin
    startRealTimeUpdates('BINANCE:BTCUSDT', '1m', 5000);
    
    // Iniciar atualizações para Ethereum
    setTimeout(() => {
        startRealTimeUpdates('BINANCE:ETHUSDT', '5m', 10000);
    }, 2000);
}

/**
 * Exemplo de comparação de símbolos
 */
async function exemploComparacao() {
    console.log('🔍 Exemplo Comparação - Múltiplos Símbolos');
    console.log('='.repeat(50));
    
    const symbols = [
        'BINANCE:BTCUSDT',
        'BINANCE:ETHUSDT',
        'BINANCE:ADAUSDT',
        'BINANCE:DOTUSDT',
        'BINANCE:LINKUSDT'
    ];
    
    await compareSymbols(symbols, '1h');
}

// Exemplos de uso
console.log('🎯 Current Candle API - Exemplos de Uso');
console.log('='.repeat(50));
console.log('1. exemploBasico() - Exemplo básico');
console.log('2. exemploDashboard() - Dashboard em tempo real');
console.log('3. exemploComparacao() - Comparar múltiplos símbolos');
console.log('4. getCurrentCandle(symbol, timeframe) - Obter candle específico');
console.log('5. startRealTimeUpdates(symbol, timeframe, interval) - Atualizações automáticas');
console.log('='.repeat(50));

// Executar exemplo básico automaticamente
exemploBasico();

