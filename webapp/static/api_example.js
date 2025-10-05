/**
 * Exemplo de uso da API de Candles
 * Este arquivo demonstra como consumir a API em JavaScript
 */

class CandlesAPI {
    constructor(baseUrl = 'http://localhost:5000/api') {
        this.baseUrl = baseUrl;
    }

    /**
     * Obter candles de um ativo
     * @param {string} symbol - Símbolo (ex: BINANCE:BTCUSDT)
     * @param {string} timeframe - Timeframe (ex: 1h, 1d)
     * @param {number} limit - Número de candles (máx: 1000)
     * @returns {Promise<Object>} Dados dos candles
     */
    async getCandles(symbol, timeframe = '1h', limit = 100) {
        try {
            const url = `${this.baseUrl}/candles`;
            const params = new URLSearchParams({
                symbol: symbol,
                timeframe: timeframe,
                limit: limit.toString()
            });

            console.log(`🔍 Buscando: ${symbol} (${timeframe}) - ${limit} candles`);
            
            const response = await fetch(`${url}?${params}`);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`HTTP ${response.status}: ${errorData.error || 'Erro desconhecido'}`);
            }

            const data = await response.json();
            console.log(`✅ Dados recebidos: ${data.total_candles} candles`);
            
            return data;
        } catch (error) {
            console.error(`❌ Erro ao buscar candles:`, error);
            throw error;
        }
    }

    /**
     * Obter apenas o preço atual
     * @param {string} symbol - Símbolo
     * @param {string} timeframe - Timeframe
     * @returns {Promise<number>} Preço atual
     */
    async getCurrentPrice(symbol, timeframe = '1m') {
        const data = await this.getCandles(symbol, timeframe, 1);
        return data.current_candle?.close || data.historical_candles[0]?.close;
    }

    /**
     * Calcular média móvel simples
     * @param {Array} candles - Array de candles
     * @param {number} period - Período da média
     * @returns {Array} Array com as médias móveis
     */
    calculateSMA(candles, period = 20) {
        const sma = [];
        
        for (let i = period - 1; i < candles.length; i++) {
            let sum = 0;
            for (let j = 0; j < period; j++) {
                sum += candles[i - j].close;
            }
            sma.push({
                timestamp: candles[i].timestamp,
                datetime: candles[i].datetime,
                value: sum / period
            });
        }
        
        return sma;
    }

    /**
     * Calcular RSI (Relative Strength Index)
     * @param {Array} candles - Array de candles
     * @param {number} period - Período do RSI
     * @returns {Array} Array com os valores de RSI
     */
    calculateRSI(candles, period = 14) {
        const rsi = [];
        const gains = [];
        const losses = [];

        // Calcular ganhos e perdas
        for (let i = 1; i < candles.length; i++) {
            const change = candles[i].close - candles[i - 1].close;
            gains.push(change > 0 ? change : 0);
            losses.push(change < 0 ? Math.abs(change) : 0);
        }

        // Calcular RSI
        for (let i = period - 1; i < gains.length; i++) {
            let avgGain = 0;
            let avgLoss = 0;

            for (let j = 0; j < period; j++) {
                avgGain += gains[i - j];
                avgLoss += losses[i - j];
            }

            avgGain /= period;
            avgLoss /= period;

            const rs = avgGain / avgLoss;
            const rsiValue = 100 - (100 / (1 + rs));

            rsi.push({
                timestamp: candles[i + 1].timestamp,
                datetime: candles[i + 1].datetime,
                value: rsiValue
            });
        }

        return rsi;
    }

    /**
     * Plotar gráfico simples (usando console)
     * @param {Array} candles - Array de candles
     */
    plotChart(candles) {
        console.log('\n📊 Gráfico de Preços:');
        console.log('=' * 50);
        
        candles.slice(-20).forEach(candle => {
            const price = candle.close;
            const bar = '█'.repeat(Math.floor(price / 1000));
            console.log(`${candle.datetime}: $${price.toFixed(2)} ${bar}`);
        });
    }
}

// Exemplos de uso
async function examples() {
    const api = new CandlesAPI();

    try {
        // Exemplo 1: Obter dados do Bitcoin
        console.log('🚀 Exemplo 1: Bitcoin 1 hora');
        const btcData = await api.getCandles('BINANCE:BTCUSDT', '1h', 50);
        console.log(`Preço atual: $${btcData.current_candle?.close || 'N/A'}`);
        console.log(`Total de candles: ${btcData.total_candles}`);

        // Exemplo 2: Calcular média móvel
        console.log('\n📈 Exemplo 2: Média Móvel Simples');
        const sma = api.calculateSMA(btcData.historical_candles, 20);
        console.log(`SMA 20: ${sma[sma.length - 1]?.value.toFixed(2)}`);

        // Exemplo 3: Calcular RSI
        console.log('\n📊 Exemplo 3: RSI');
        const rsi = api.calculateRSI(btcData.historical_candles, 14);
        console.log(`RSI 14: ${rsi[rsi.length - 1]?.value.toFixed(2)}`);

        // Exemplo 4: Preço atual
        console.log('\n💰 Exemplo 4: Preço Atual');
        const currentPrice = await api.getCurrentPrice('BINANCE:BTCUSDT', '1m');
        console.log(`Preço atual BTC: $${currentPrice}`);

        // Exemplo 5: Gráfico simples
        console.log('\n📊 Exemplo 5: Gráfico');
        api.plotChart(btcData.historical_candles);

    } catch (error) {
        console.error('Erro nos exemplos:', error);
    }
}

// Executar exemplos quando a página carregar
if (typeof window !== 'undefined') {
    // Se estiver no navegador
    window.CandlesAPI = CandlesAPI;
    window.runCandlesExamples = examples;
    
    console.log('🔧 API de Candles carregada!');
    console.log('Execute: runCandlesExamples() para ver os exemplos');
} else {
    // Se estiver no Node.js
    examples();
}

// Exportar para uso em módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CandlesAPI;
}
