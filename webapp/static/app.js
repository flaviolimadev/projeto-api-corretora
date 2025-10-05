// Socket.IO connection
const socket = io();

// DOM elements
const symbolInput = document.getElementById('symbol-input');
const timeframeSelect = document.getElementById('timeframe-select');
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const currentPriceEl = document.getElementById('current-price');
const priceChangeEl = document.getElementById('price-change');
const openPriceEl = document.getElementById('open-price');
const highPriceEl = document.getElementById('high-price');
const lowPriceEl = document.getElementById('low-price');
const volumeEl = document.getElementById('volume');
const statusEl = document.getElementById('status');
const statusTextEl = document.getElementById('status-text');
const symbolDisplayEl = document.getElementById('symbol-display');
const autocompleteResults = document.getElementById('autocomplete-results');

// State
let chart = null;
let candlestickSeries = null;
let previousPrice = null;
let isStreaming = false;
let candleData = [];
let isHistoricalDataLoaded = false;
let autocompleteTimeout = null;
let selectedIndex = -1;
let priceLines = [];
let markers = [];

// Indicators state
let indicators = {
    ema: { active: false, series: [], lines: [] },
    sma: { active: false, series: [], lines: [] },
    bb: { active: false, series: [], lines: [] },
    volume: { active: false, series: null }
};
let currentTimeframe = '1m';
let priceUpdateCount = 0;

// Technical Indicators Calculation Functions
function calculateEMA(data, period) {
    const k = 2 / (period + 1);
    const emaData = [];
    let ema = data[0].close;
    
    emaData.push({ time: data[0].time, value: ema });
    
    for (let i = 1; i < data.length; i++) {
        ema = (data[i].close * k) + (ema * (1 - k));
        emaData.push({ time: data[i].time, value: ema });
    }
    
    return emaData;
}

function calculateSMA(data, period) {
    const smaData = [];
    
    for (let i = period - 1; i < data.length; i++) {
        let sum = 0;
        for (let j = 0; j < period; j++) {
            sum += data[i - j].close;
        }
        smaData.push({ time: data[i].time, value: sum / period });
    }
    
    return smaData;
}

function calculateBollingerBands(data, period = 20, stdDev = 2) {
    const sma = calculateSMA(data, period);
    const upper = [];
    const lower = [];
    
    for (let i = period - 1; i < data.length; i++) {
        let sum = 0;
        const smaValue = sma[i - period + 1].value;
        
        for (let j = 0; j < period; j++) {
            sum += Math.pow(data[i - j].close - smaValue, 2);
        }
        
        const variance = sum / period;
        const standardDeviation = Math.sqrt(variance);
        
        upper.push({ time: data[i].time, value: smaValue + (standardDeviation * stdDev) });
        lower.push({ time: data[i].time, value: smaValue - (standardDeviation * stdDev) });
    }
    
    return { upper, middle: sma, lower };
}

// Add/Remove Indicators
function toggleIndicator(indicatorName) {
    const indicator = indicators[indicatorName];
    
    if (indicator.active) {
        removeIndicator(indicatorName);
    } else {
        addIndicator(indicatorName);
    }
    
    indicator.active = !indicator.active;
}

function addIndicator(indicatorName) {
    if (candleData.length < 50) {
        console.warn('Not enough data to calculate indicators');
        return;
    }
    
    switch (indicatorName) {
        case 'ema':
            const ema9 = calculateEMA(candleData, 9);
            const ema21 = calculateEMA(candleData, 21);
            
            const ema9Line = chart.addLineSeries({
                color: '#2962FF',
                lineWidth: 2,
                title: 'EMA 9',
                priceLineVisible: false,
                lastValueVisible: true,
            });
            ema9Line.setData(ema9);
            
            const ema21Line = chart.addLineSeries({
                color: '#FF6D00',
                lineWidth: 2,
                title: 'EMA 21',
                priceLineVisible: false,
                lastValueVisible: true,
            });
            ema21Line.setData(ema21);
            
            indicators.ema.series = [ema9, ema21];
            indicators.ema.lines = [ema9Line, ema21Line];
            break;
            
        case 'sma':
            const sma20 = calculateSMA(candleData, 20);
            const sma50 = calculateSMA(candleData, 50);
            
            const sma20Line = chart.addLineSeries({
                color: '#26a69a',
                lineWidth: 2,
                title: 'SMA 20',
                priceLineVisible: false,
                lastValueVisible: true,
            });
            sma20Line.setData(sma20);
            
            const sma50Line = chart.addLineSeries({
                color: '#ef5350',
                lineWidth: 2,
                title: 'SMA 50',
                priceLineVisible: false,
                lastValueVisible: true,
            });
            sma50Line.setData(sma50);
            
            indicators.sma.series = [sma20, sma50];
            indicators.sma.lines = [sma20Line, sma50Line];
            break;
            
        case 'bb':
            const bb = calculateBollingerBands(candleData, 20, 2);
            
            const upperLine = chart.addLineSeries({
                color: 'rgba(41, 98, 255, 0.5)',
                lineWidth: 1,
                title: 'BB Upper',
                priceLineVisible: false,
                lastValueVisible: false,
            });
            upperLine.setData(bb.upper);
            
            const middleLine = chart.addLineSeries({
                color: 'rgba(255, 255, 255, 0.5)',
                lineWidth: 1,
                lineStyle: 2,
                title: 'BB Middle',
                priceLineVisible: false,
                lastValueVisible: false,
            });
            middleLine.setData(bb.middle);
            
            const lowerLine = chart.addLineSeries({
                color: 'rgba(41, 98, 255, 0.5)',
                lineWidth: 1,
                title: 'BB Lower',
                priceLineVisible: false,
                lastValueVisible: false,
            });
            lowerLine.setData(bb.lower);
            
            indicators.bb.series = [bb.upper, bb.middle, bb.lower];
            indicators.bb.lines = [upperLine, middleLine, lowerLine];
            break;
            
        case 'volume':
            const volumeData = candleData.map(candle => ({
                time: candle.time,
                value: candle.volume || 0,
                color: candle.close >= candle.open ? 'rgba(38, 166, 154, 0.5)' : 'rgba(239, 83, 80, 0.5)'
            }));
            
            const volumeSeries = chart.addHistogramSeries({
                priceFormat: {
                    type: 'volume',
                },
                priceScaleId: 'volume',
                scaleMargins: {
                    top: 0.8,
                    bottom: 0,
                },
            });
            volumeSeries.setData(volumeData);
            
            indicators.volume.series = volumeSeries;
            break;
    }
}

function removeIndicator(indicatorName) {
    const indicator = indicators[indicatorName];
    
    if (indicatorName === 'volume' && indicator.series) {
        chart.removeSeries(indicator.series);
        indicator.series = null;
    } else if (indicator.lines && indicator.lines.length > 0) {
        indicator.lines.forEach(line => {
            try {
                chart.removeSeries(line);
            } catch (e) {
                console.error('Error removing indicator line:', e);
            }
        });
        indicator.lines = [];
        indicator.series = [];
    }
}

function updateIndicators() {
    Object.keys(indicators).forEach(indicatorName => {
        if (indicators[indicatorName].active) {
            removeIndicator(indicatorName);
            addIndicator(indicatorName);
        }
    });
}

// Initialize chart
function initChart() {
    const chartContainer = document.getElementById('chart');
    
    chart = LightweightCharts.createChart(chartContainer, {
        width: chartContainer.clientWidth,
        height: 550,
        layout: {
            background: { type: 'solid', color: 'transparent' },
            textColor: '#d1d4dc',
        },
        grid: {
            vertLines: { color: 'rgba(42, 46, 57, 0.5)' },
            horzLines: { color: 'rgba(42, 46, 57, 0.5)' },
        },
        crosshair: {
            mode: LightweightCharts.CrosshairMode.Normal,
        },
        rightPriceScale: {
            borderColor: '#2a2e39',
        },
        timeScale: {
            borderColor: '#2a2e39',
            timeVisible: true,
            secondsVisible: false,
        },
    });

    candlestickSeries = chart.addCandlestickSeries({
        upColor: '#26a69a',
        downColor: '#ef5350',
        borderVisible: false,
        wickUpColor: '#26a69a',
        wickDownColor: '#ef5350',
    });

    // Handle window resize
    window.addEventListener('resize', () => {
        chart.applyOptions({ width: chartContainer.clientWidth });
    });
}

// Format number with commas
function formatNumber(num, decimals = 2) {
    if (num === null || num === undefined) return '-';
    return parseFloat(num).toLocaleString('pt-BR', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    });
}

// Update price display
function updatePriceDisplay(data) {
    const { open, high, low, close, volume } = data;
    
    // Update current price
    currentPriceEl.textContent = `$${formatNumber(close)}`;
    
    // Update price change
    if (previousPrice !== null) {
        const change = close - previousPrice;
        const changePercent = ((change / previousPrice) * 100).toFixed(2);
        
        priceChangeEl.textContent = `${change >= 0 ? '+' : ''}${formatNumber(change)} (${changePercent}%)`;
        priceChangeEl.className = change >= 0 ? 'price-change positive' : 'price-change negative';
        
        // Animate price change
        currentPriceEl.style.transform = 'scale(1.05)';
        setTimeout(() => {
            currentPriceEl.style.transform = 'scale(1)';
        }, 200);
    }
    
    previousPrice = close;
    
    // Update other info
    openPriceEl.textContent = `$${formatNumber(open)}`;
    highPriceEl.textContent = `$${formatNumber(high)}`;
    lowPriceEl.textContent = `$${formatNumber(low)}`;
    volumeEl.textContent = formatNumber(volume, 4);
}

// Update chart
function updateChart(data) {
    const { timestamp, open, high, low, close } = data;
    
    const candle = {
        time: Math.floor(timestamp),
        open: parseFloat(open),
        high: parseFloat(high),
        low: parseFloat(low),
        close: parseFloat(close)
    };
    
    console.log(`🕯️ Processing candle:`, candle);
    
    // If we're still loading historical data, batch them
    if (!isHistoricalDataLoaded) {
        candleData.push(candle);
        console.log(`📦 Added to batch, total: ${candleData.length}`);
    } else {
        // For real-time updates, use update method
        console.log(`⚡ Real-time update`);
        candlestickSeries.update(candle);
    }
}

// Update status
function updateStatus(status, text) {
    statusEl.className = `status ${status}`;
    statusTextEl.textContent = text;
}

// Socket.IO event handlers
socket.on('connect', () => {
    console.log('Connected to server');
    updateStatus('connected', 'Conectado');
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
    updateStatus('', 'Desconectado');
    isStreaming = false;
    startBtn.disabled = false;
    stopBtn.disabled = true;
});

socket.on('stream_started', (data) => {
    console.log('✅ Stream started:', data);
    updateStatus('streaming', 'Carregando dados históricos...');
    symbolDisplayEl.textContent = `${data.symbol} (${data.timeframe})`;
    isStreaming = true;
    isHistoricalDataLoaded = false;
    candleData = [];
    priceUpdateCount = 0;
    
    // Update current timeframe
    currentTimeframe = data.timeframe;
    
    // Update toolbar buttons
    document.querySelectorAll('.tf-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tf === data.timeframe) {
            btn.classList.add('active');
        }
    });
    
    // Clear all indicators when starting new stream
    Object.keys(indicators).forEach(indicatorName => {
        if (indicators[indicatorName].active) {
            removeIndicator(indicatorName);
        }
    });
    
    // Reset indicator buttons
    document.querySelectorAll('.indicator-btn').forEach(btn => {
        btn.classList.remove('active');
        indicators[btn.dataset.indicator].active = false;
    });
    
    console.log(`📈 Ready to receive data for ${data.symbol} (${data.timeframe})`);
});

socket.on('stream_stopped', () => {
    console.log('Stream stopped');
    updateStatus('connected', 'Stream Parado');
    isStreaming = false;
    startBtn.disabled = false;
    stopBtn.disabled = true;
});

socket.on('price_update', (data) => {
    console.log(`📊 Price update #${priceUpdateCount + 1}:`, data);
    updatePriceDisplay(data);
    updateChart(data);
    
    priceUpdateCount++;
    
    // Debug: Show when we have enough data
    if (priceUpdateCount % 100 === 0) {
        console.log(`📈 Received ${priceUpdateCount} updates, candleData length: ${candleData.length}`);
    }
    
    // After receiving ~1000 updates (historical data), switch to real-time mode
    if (!isHistoricalDataLoaded && priceUpdateCount > 900) {
        isHistoricalDataLoaded = true;
        
        // Set all historical data at once
        if (candleData.length > 0) {
            // Sort by timestamp
            candleData.sort((a, b) => a.time - b.time);
            console.log(`📊 Setting ${candleData.length} candles to chart`);
            candlestickSeries.setData(candleData);
            console.log(`✅ Loaded ${candleData.length} historical candles for ${currentTimeframe}`);
            updateStatus('streaming', 'Streaming em Tempo Real');
            
            // Update indicators with historical data
            updateIndicators();
        } else {
            console.log(`⚠️ No candle data to display!`);
        }
    }
});

socket.on('error', (error) => {
    console.error('Error:', error);
    alert(`Erro: ${error.message}`);
    updateStatus('connected', 'Erro');
    isStreaming = false;
    startBtn.disabled = false;
    stopBtn.disabled = true;
});

// Button handlers
startBtn.addEventListener('click', () => {
    const symbol = symbolInput.value.trim();
    const timeframe = timeframeSelect.value;
    
    if (!symbol) {
        alert('Por favor, insira um símbolo válido');
        return;
    }
    
    // Validate format
    if (!symbol.includes(':')) {
        alert('Formato inválido. Use EXCHANGE:SYMBOL (ex: BINANCE:BTCUSDT)');
        return;
    }
    
    // Reset chart and state
    if (candlestickSeries) {
        candlestickSeries.setData([]);
    }
    previousPrice = null;
    priceUpdateCount = 0;
    candleData = [];
    isHistoricalDataLoaded = false;
    
    // Update current timeframe
    currentTimeframe = timeframe;
    
    // Update toolbar buttons to match
    document.querySelectorAll('.tf-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tf === timeframe) {
            btn.classList.add('active');
        }
    });
    
    // Start stream with timeframe
    socket.emit('start_stream', { symbol, timeframe });
    startBtn.disabled = true;
    stopBtn.disabled = false;
});

stopBtn.addEventListener('click', () => {
    socket.emit('stop_stream');
    stopBtn.disabled = true;
});

// Popular symbols
const popularSymbols = [
    { symbol: 'BINANCE:BTCUSDT', description: 'Bitcoin / Tether', type: 'crypto', exchange: 'BINANCE' },
    { symbol: 'BINANCE:ETHUSDT', description: 'Ethereum / Tether', type: 'crypto', exchange: 'BINANCE' },
    { symbol: 'BINANCE:BNBUSDT', description: 'Binance Coin / Tether', type: 'crypto', exchange: 'BINANCE' },
    { symbol: 'BINANCE:ADAUSDT', description: 'Cardano / Tether', type: 'crypto', exchange: 'BINANCE' },
    { symbol: 'BINANCE:DOGEUSDT', description: 'Dogecoin / Tether', type: 'crypto', exchange: 'BINANCE' },
    { symbol: 'BINANCE:SOLUSDT', description: 'Solana / Tether', type: 'crypto', exchange: 'BINANCE' },
    { symbol: 'FXOPEN:EURUSD', description: 'Euro / US Dollar', type: 'forex', exchange: 'FXOPEN' },
    { symbol: 'FXOPEN:GBPUSD', description: 'British Pound / US Dollar', type: 'forex', exchange: 'FXOPEN' },
    { symbol: 'FXOPEN:USDJPY', description: 'US Dollar / Japanese Yen', type: 'forex', exchange: 'FXOPEN' },
    { symbol: 'FXOPEN:AUDUSD', description: 'Australian Dollar / US Dollar', type: 'forex', exchange: 'FXOPEN' },
    { symbol: 'FXOPEN:XAUUSD', description: 'Gold / US Dollar', type: 'commodity', exchange: 'FXOPEN' },
    { symbol: 'NASDAQ:AAPL', description: 'Apple Inc.', type: 'stock', exchange: 'NASDAQ' },
    { symbol: 'NASDAQ:TSLA', description: 'Tesla Inc.', type: 'stock', exchange: 'NASDAQ' },
    { symbol: 'NASDAQ:MSFT', description: 'Microsoft Corporation', type: 'stock', exchange: 'NASDAQ' },
    { symbol: 'NASDAQ:GOOGL', description: 'Alphabet Inc.', type: 'stock', exchange: 'NASDAQ' },
    { symbol: 'NYSE:NVDA', description: 'NVIDIA Corporation', type: 'stock', exchange: 'NYSE' },
];

// Autocomplete functionality
async function searchSymbols(query) {
    try {
        // First, search in popular symbols
        const queryLower = query.toLowerCase();
        const popularMatches = popularSymbols.filter(s => 
            s.symbol.toLowerCase().includes(queryLower) ||
            s.description.toLowerCase().includes(queryLower)
        );
        
        // Then search API
        const response = await fetch(`/api/search-symbols?q=${encodeURIComponent(query)}`);
        const apiResults = await response.json();
        
        // Combine results, prioritizing popular symbols
        const combined = [...popularMatches];
        apiResults.forEach(result => {
            if (!combined.find(s => s.symbol === result.symbol)) {
                combined.push(result);
            }
        });
        
        return combined.slice(0, 15);
    } catch (error) {
        console.error('Error searching symbols:', error);
        
        // Fallback to popular symbols only
        const queryLower = query.toLowerCase();
        return popularSymbols.filter(s => 
            s.symbol.toLowerCase().includes(queryLower) ||
            s.description.toLowerCase().includes(queryLower)
        ).slice(0, 15);
    }
}

function showAutocomplete(results) {
    autocompleteResults.innerHTML = '';
    selectedIndex = -1;
    
    if (results.length === 0) {
        autocompleteResults.innerHTML = '<div class="autocomplete-no-results">Nenhum símbolo encontrado</div>';
        autocompleteResults.classList.add('show');
        return;
    }
    
    results.forEach((result, index) => {
        const div = document.createElement('div');
        div.className = 'autocomplete-item';
        div.dataset.index = index;
        div.dataset.symbol = result.symbol;
        
        div.innerHTML = `
            <div class="autocomplete-symbol">
                ${result.symbol}
                <span class="autocomplete-badge">${result.type}</span>
            </div>
            <div class="autocomplete-description">${result.description}</div>
        `;
        
        div.addEventListener('click', () => {
            symbolInput.value = result.symbol;
            hideAutocomplete();
        });
        
        autocompleteResults.appendChild(div);
    });
    
    autocompleteResults.classList.add('show');
}

function hideAutocomplete() {
    autocompleteResults.classList.remove('show');
    selectedIndex = -1;
}

function navigateAutocomplete(direction) {
    const items = autocompleteResults.querySelectorAll('.autocomplete-item');
    if (items.length === 0) return;
    
    // Remove active class from current
    if (selectedIndex >= 0 && selectedIndex < items.length) {
        items[selectedIndex].classList.remove('active');
    }
    
    // Update index
    if (direction === 'down') {
        selectedIndex = (selectedIndex + 1) % items.length;
    } else if (direction === 'up') {
        selectedIndex = selectedIndex <= 0 ? items.length - 1 : selectedIndex - 1;
    }
    
    // Add active class to new
    items[selectedIndex].classList.add('active');
    
    // Update input value
    symbolInput.value = items[selectedIndex].dataset.symbol;
    
    // Scroll into view
    items[selectedIndex].scrollIntoView({ block: 'nearest' });
}

// Symbol input events
symbolInput.addEventListener('input', (e) => {
    const query = e.target.value.trim();
    
    // Clear previous timeout
    if (autocompleteTimeout) {
        clearTimeout(autocompleteTimeout);
    }
    
    // Hide if empty
    if (query.length < 2) {
        hideAutocomplete();
        return;
    }
    
    // Show loading
    autocompleteResults.innerHTML = '<div class="autocomplete-loading">Buscando...</div>';
    autocompleteResults.classList.add('show');
    
    // Debounce search
    autocompleteTimeout = setTimeout(async () => {
        const results = await searchSymbols(query);
        showAutocomplete(results);
    }, 300);
});

symbolInput.addEventListener('keydown', (e) => {
    const isOpen = autocompleteResults.classList.contains('show');
    
    if (e.key === 'ArrowDown' && isOpen) {
        e.preventDefault();
        navigateAutocomplete('down');
    } else if (e.key === 'ArrowUp' && isOpen) {
        e.preventDefault();
        navigateAutocomplete('up');
    } else if (e.key === 'Escape') {
        hideAutocomplete();
    } else if (e.key === 'Enter') {
        if (isOpen && selectedIndex >= 0) {
            e.preventDefault();
            hideAutocomplete();
        } else if (!startBtn.disabled) {
            e.preventDefault();
            startBtn.click();
        }
    }
});

// Close autocomplete when clicking outside
document.addEventListener('click', (e) => {
    if (!symbolInput.contains(e.target) && !autocompleteResults.contains(e.target)) {
        hideAutocomplete();
    }
});

// Binary Options Trading System
let balance = 10000;
let activeTrades = [];
let tradeHistory = [];
let selectedAmount = 50;
let selectedExpiry = 60;
let currentPrice = null;
let tradeIdCounter = 0;

const balanceEl = document.getElementById('balance');
const callBtn = document.getElementById('call-btn');
const putBtn = document.getElementById('put-btn');
const activeTradesEl = document.getElementById('active-trades');
const historyListEl = document.getElementById('history-list');
const customAmountInput = document.getElementById('custom-amount');

// Amount selector
document.querySelectorAll('.amount-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.amount-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        selectedAmount = parseFloat(btn.dataset.amount);
        customAmountInput.value = selectedAmount;
    });
});

customAmountInput.addEventListener('input', (e) => {
    selectedAmount = parseFloat(e.target.value) || 50;
    document.querySelectorAll('.amount-btn').forEach(b => b.classList.remove('active'));
});

// Expiry selector
document.querySelectorAll('.expiry-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.expiry-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        selectedExpiry = parseInt(btn.dataset.expiry);
    });
});

// Update balance display
function updateBalance() {
    balanceEl.textContent = `$${formatNumber(balance)}`;
    balanceEl.style.transform = 'scale(1.1)';
    setTimeout(() => {
        balanceEl.style.transform = 'scale(1)';
    }, 200);
}

// Enable/disable trade buttons
function updateTradeButtons() {
    const canTrade = isStreaming && currentPrice && balance >= selectedAmount;
    callBtn.disabled = !canTrade;
    putBtn.disabled = !canTrade;
}

// Place a trade
function placeTrade(type) {
    if (!currentPrice || balance < selectedAmount) {
        alert('Saldo insuficiente ou preço não disponível!');
        return;
    }
    
    const trade = {
        id: `trade_${tradeIdCounter++}`,
        type: type,
        amount: selectedAmount,
        entryPrice: currentPrice,
        entryTime: Date.now(),
        expiryTime: Date.now() + (selectedExpiry * 1000),
        expirySeconds: selectedExpiry,
        payout: 0.85
    };
    
    balance -= selectedAmount;
    updateBalance();
    
    activeTrades.push(trade);
    renderActiveTrades();
    updateTradeButtons();
    
    // Show notification
    showTradeNotification(trade);
    
    // Create price line marker on chart
    createPriceMarker(trade);
}

// Show trade notification
function showTradeNotification(trade) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${trade.type === 'call' ? '#26a69a' : '#ef5350'};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        font-weight: 600;
        z-index: 10000;
        animation: slideIn 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    `;
    notification.textContent = `${trade.type === 'call' ? '📈 CALL' : '📉 PUT'} de $${trade.amount} aberto!`;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 2000);
}

// Create price marker on chart  
function createPriceMarker(trade) {
    if (!candlestickSeries) return;
    
    const color = trade.type === 'call' ? '#26a69a' : '#ef5350';
    
    // Create horizontal price line at entry price
    const priceLine = candlestickSeries.createPriceLine({
        price: trade.entryPrice,
        color: color,
        lineWidth: 2,
        lineStyle: 2, // Dashed
        axisLabelVisible: true,
        title: '',
    });
    
    // Store the price line reference
    priceLines.push({
        id: trade.id,
        line: priceLine,
        trade: trade
    });
    
    // Add entry marker
    const entryTime = Math.floor(trade.entryTime / 1000);
    const entryMarker = {
        time: entryTime,
        position: trade.type === 'call' ? 'belowBar' : 'aboveBar',
        color: color,
        shape: trade.type === 'call' ? 'arrowUp' : 'arrowDown',
        text: `${trade.type.toUpperCase()}`,
        size: 1
    };
    
    // Add expiry marker
    const expiryTime = Math.floor(trade.expiryTime / 1000);
    const expiryMarker = {
        time: expiryTime,
        position: 'inBar',
        color: '#ef5350',
        shape: 'circle',
        text: '⏰',
        size: 2
    };
    
    markers.push({
        id: trade.id,
        marker: entryMarker,
        trade: trade
    });
    
    markers.push({
        id: `${trade.id}_expiry`,
        marker: expiryMarker,
        trade: trade
    });
    
    updateChartMarkers();
    
    // Create HTML overlay for percentage badge and countdown
    createHTMLOverlay(trade);
}

// Create HTML overlay for badges and countdown
function createHTMLOverlay(trade) {
    const overlaysContainer = document.getElementById('chart-overlays');
    if (!overlaysContainer) return;
    
    const overlay = document.createElement('div');
    overlay.id = `overlay-${trade.id}`;
    overlay.className = 'trade-overlay';
    overlay.dataset.tradeId = trade.id;
    overlay.dataset.entryPrice = trade.entryPrice;
    overlay.dataset.expiryTime = trade.expiryTime;
    
    overlaysContainer.appendChild(overlay);
}

// Update HTML overlays (badges and countdown only)
function updateTradeOverlays() {
    if (!chart || !candlestickSeries) return;
    
    const chartContainer = document.getElementById('chart');
    if (!chartContainer) return;
    
    activeTrades.forEach(trade => {
        const overlay = document.getElementById(`overlay-${trade.id}`);
        if (!overlay) return;
        
        const entryPrice = parseFloat(overlay.dataset.entryPrice);
        const expiryTime = parseInt(overlay.dataset.expiryTime);
        const now = Date.now();
        const timeRemaining = Math.max(0, expiryTime - now);
        const seconds = Math.ceil(timeRemaining / 1000);
        
        const profit = currentPrice ? 
            (trade.type === 'call' ? currentPrice - entryPrice : entryPrice - currentPrice) : 0;
        const profitPercent = ((profit / entryPrice) * 100).toFixed(2);
        const isWinning = profit > 0;
        
        try {
            const priceY = candlestickSeries.priceToCoordinate(entryPrice);
            const expiryTimestamp = Math.floor(expiryTime / 1000);
            const expiryX = chart.timeScale().timeToCoordinate(expiryTimestamp);
            
            if (priceY === null || expiryX === null) return;
            
            overlay.innerHTML = '';
            
            // Create price badge (on the right)
            const badge = document.createElement('div');
            badge.className = `price-badge ${isWinning ? 'winning' : 'losing'}`;
            badge.style.top = `${priceY}px`;
            badge.style.left = `${chartContainer.offsetWidth - 90}px`;
            badge.textContent = `${profit >= 0 ? '+' : ''}${profitPercent}%`;
            overlay.appendChild(badge);
            
            // Create countdown clock above expiry marker
            if (expiryX > 0) {
                const clock = document.createElement('div');
                clock.className = `countdown-clock ${seconds < 10 ? 'urgent' : ''}`;
                clock.style.left = `${expiryX}px`;
                clock.style.top = `10px`;
                clock.textContent = seconds;
                overlay.appendChild(clock);
            }
        } catch (e) {
            console.error('Error updating overlay:', e);
        }
    });
    
    // Update price line colors
    updatePriceLineColors();
}

// Update price line colors based on profit/loss
function updatePriceLineColors() {
    if (!currentPrice) return;
    
    priceLines.forEach(({ id, line, trade }) => {
        const profit = trade.type === 'call' ? 
            currentPrice - trade.entryPrice : 
            trade.entryPrice - currentPrice;
        
        const isWinning = profit > 0;
        const newColor = isWinning ? '#26a69a' : '#ef5350';
        
        // Remove old line
        try {
            candlestickSeries.removePriceLine(line);
        } catch (e) {
            // Line already removed
        }
        
        // Create new line with updated color
        const newLine = candlestickSeries.createPriceLine({
            price: trade.entryPrice,
            color: newColor,
            lineWidth: 2,
            lineStyle: 2,
            axisLabelVisible: true,
            title: `${isWinning ? '✓' : '✗'} ${Math.abs(profit).toFixed(2)}`,
        });
        
        // Update stored reference
        const lineIndex = priceLines.findIndex(pl => pl.id === id);
        if (lineIndex !== -1) {
            priceLines[lineIndex].line = newLine;
        }
    });
}

// Update chart markers
function updateChartMarkers() {
    if (candlestickSeries && markers.length > 0) {
        candlestickSeries.setMarkers(markers.map(m => m.marker));
    }
}

// Update visual overlays - called every second
function updateVisualOverlays() {
    updateTradeOverlays();
}

// Render active trades
function renderActiveTrades() {
    if (activeTrades.length === 0) {
        activeTradesEl.innerHTML = '';
        return;
    }
    
    // Update visual overlays
    updateVisualOverlays();
    
    activeTradesEl.innerHTML = activeTrades.map(trade => {
        const remaining = Math.max(0, Math.ceil((trade.expiryTime - Date.now()) / 1000));
        const minutes = Math.floor(remaining / 60);
        const seconds = remaining % 60;
        
        const profit = currentPrice ? 
            (trade.type === 'call' ? currentPrice - trade.entryPrice : trade.entryPrice - currentPrice) : 0;
        const profitPercent = ((profit / trade.entryPrice) * 100).toFixed(2);
        const isWinning = profit > 0;
        
        return `
            <div class="active-trade-card ${isWinning ? 'winning' : 'losing'}" data-trade-id="${trade.id}">
                <div class="trade-card-header">
                    <span class="trade-type ${trade.type}">${trade.type === 'call' ? '📈 CALL' : '📉 PUT'}</span>
                    <span class="trade-timer ${remaining < 10 ? 'urgent' : ''}">${minutes}:${seconds.toString().padStart(2, '0')}</span>
                </div>
                <div class="trade-info">
                    <div class="trade-info-item">
                        <span class="trade-info-label">Entrada</span>
                        <span class="trade-info-value">$${formatNumber(trade.entryPrice)}</span>
                    </div>
                    <div class="trade-info-item">
                        <span class="trade-info-label">Atual</span>
                        <span class="trade-info-value" style="color: ${profit >= 0 ? 'var(--success)' : 'var(--error)'}">
                            $${currentPrice ? formatNumber(currentPrice) : '-'}
                        </span>
                    </div>
                    <div class="trade-info-item">
                        <span class="trade-info-label">Valor</span>
                        <span class="trade-info-value">$${formatNumber(trade.amount)}</span>
                    </div>
                    <div class="trade-info-item">
                        <span class="trade-info-label">P&L</span>
                        <span class="trade-info-value status-${isWinning ? 'winning' : 'losing'}">
                            ${isWinning ? '✓' : '✗'} ${profit >= 0 ? '+' : ''}${profitPercent}%
                        </span>
                    </div>
                </div>
                <div class="trade-status-bar ${isWinning ? 'winning' : 'losing'}">
                    ${isWinning ? '🚀 EM LUCRO' : '⚠️ EM PERDA'}
                </div>
            </div>
        `;
    }).join('');
}

// Check trade expirations
function checkTradeExpirations() {
    const now = Date.now();
    const expiredTrades = activeTrades.filter(trade => now >= trade.expiryTime);
    
    expiredTrades.forEach(trade => {
        closeTrade(trade);
    });
    
    activeTrades = activeTrades.filter(trade => now < trade.expiryTime);
    renderActiveTrades();
}

// Close a trade
function closeTrade(trade) {
    if (!currentPrice) return;
    
    const isWin = (trade.type === 'call' && currentPrice > trade.entryPrice) ||
                  (trade.type === 'put' && currentPrice < trade.entryPrice);
    
    const profit = isWin ? trade.amount * trade.payout : -trade.amount;
    const finalBalance = balance + trade.amount + profit;
    
    balance = finalBalance;
    updateBalance();
    
    // Remove price line from chart
    removePriceLine(trade.id);
    
    // Add close marker to chart
    addCloseMarker(trade, isWin);
    
    // Add to history
    const historyItem = {
        ...trade,
        closePrice: currentPrice,
        closeTime: Date.now(),
        profit: profit,
        isWin: isWin
    };
    
    tradeHistory.unshift(historyItem);
    renderHistory();
    updateTradeButtons();
    
    // Show result notification
    showResultNotification(historyItem);
}

// Remove price line from chart
function removePriceLine(tradeId) {
    // Remove price line
    const lineIndex = priceLines.findIndex(pl => pl.id === tradeId);
    if (lineIndex !== -1) {
        try {
            candlestickSeries.removePriceLine(priceLines[lineIndex].line);
        } catch (e) {
            // Already removed
        }
        priceLines.splice(lineIndex, 1);
    }
    
    // Remove markers
    markers = markers.filter(m => !m.id.toString().startsWith(tradeId.toString()));
    updateChartMarkers();
    
    // Remove HTML overlay
    const overlay = document.getElementById(`overlay-${tradeId}`);
    if (overlay) {
        overlay.remove();
    }
}

// Add close marker
function addCloseMarker(trade, isWin) {
    // Visual feedback only - marker removed with overlay
    console.log(`Trade closed: ${isWin ? 'WIN' : 'LOSS'}`);
}

// Show result notification
function showResultNotification(trade) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${trade.isWin ? '#26a69a' : '#ef5350'};
        color: white;
        padding: 20px 25px;
        border-radius: 8px;
        font-weight: 700;
        z-index: 10000;
        animation: slideIn 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        font-size: 1.1rem;
    `;
    notification.innerHTML = `
        <div style="font-size: 2rem; margin-bottom: 10px;">${trade.isWin ? '🎉' : '😢'}</div>
        <div>${trade.isWin ? 'GANHOU!' : 'PERDEU'}</div>
        <div style="font-size: 1.3rem; margin-top: 5px;">
            ${trade.profit >= 0 ? '+' : ''}$${formatNumber(Math.abs(trade.profit))}
        </div>
    `;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Render history
function renderHistory() {
    if (tradeHistory.length === 0) {
        historyListEl.innerHTML = '<p class="no-history">Nenhuma operação realizada ainda</p>';
        return;
    }
    
    historyListEl.innerHTML = tradeHistory.slice(0, 20).map(trade => {
        const time = new Date(trade.closeTime).toLocaleTimeString('pt-BR');
        return `
            <div class="history-item ${trade.isWin ? 'win' : 'loss'}">
                <div class="history-item-left">
                    <span class="history-item-type">
                        ${trade.type === 'call' ? '📈 CALL' : '📉 PUT'} - $${formatNumber(trade.amount)}
                    </span>
                    <span class="history-item-time">${time}</span>
                </div>
                <div class="history-item-right">
                    <div class="history-item-result ${trade.profit >= 0 ? 'profit' : 'loss'}">
                        ${trade.profit >= 0 ? '+' : ''}$${formatNumber(Math.abs(trade.profit))}
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// Trade button handlers
callBtn.addEventListener('click', () => placeTrade('call'));
putBtn.addEventListener('click', () => placeTrade('put'));

// Update active trades every second
setInterval(() => {
    if (activeTrades.length > 0) {
        renderActiveTrades();
        checkTradeExpirations();
    }
}, 1000);

// Update current price when price updates
const originalUpdatePriceDisplay = updatePriceDisplay;
updatePriceDisplay = function(data) {
    originalUpdatePriceDisplay(data);
    currentPrice = data.close;
    updateTradeButtons();
};

// Visual Effects - Confetti for wins
function createConfetti(isWin) {
    const colors = isWin ? 
        ['#26a69a', '#00bfa5', '#4caf50', '#8bc34a'] : 
        ['#ef5350', '#f44336', '#e91e63', '#ff5722'];
    
    const confettiCount = isWin ? 50 : 20;
    
    for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement('div');
        confetti.style.position = 'fixed';
        confetti.style.width = '10px';
        confetti.style.height = '10px';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.left = Math.random() * window.innerWidth + 'px';
        confetti.style.top = '-10px';
        confetti.style.opacity = '1';
        confetti.style.zIndex = '9999';
        confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
        confetti.style.pointerEvents = 'none';
        
        document.body.appendChild(confetti);
        
        const duration = 2000 + Math.random() * 1000;
        const rotation = Math.random() * 360;
        const xMovement = (Math.random() - 0.5) * 200;
        
        confetti.animate([
            { transform: 'translateY(0) translateX(0) rotate(0deg)', opacity: 1 },
            { transform: `translateY(${window.innerHeight}px) translateX(${xMovement}px) rotate(${rotation}deg)`, opacity: 0 }
        ], {
            duration: duration,
            easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
        });
        
        setTimeout(() => {
            confetti.remove();
        }, duration);
    }
}

// Screen shake effect
function shakeScreen(intensity = 5, duration = 500) {
    const body = document.body;
    const originalTransform = body.style.transform;
    let startTime = null;
    
    function shake(timestamp) {
        if (!startTime) startTime = timestamp;
        const elapsed = timestamp - startTime;
        
        if (elapsed < duration) {
            const x = (Math.random() - 0.5) * intensity;
            const y = (Math.random() - 0.5) * intensity;
            body.style.transform = `translate(${x}px, ${y}px)`;
            requestAnimationFrame(shake);
        } else {
            body.style.transform = originalTransform;
        }
    }
    
    requestAnimationFrame(shake);
}

// Flash screen effect
function flashScreen(color, opacity = 0.3, duration = 300) {
    const flash = document.createElement('div');
    flash.style.position = 'fixed';
    flash.style.top = '0';
    flash.style.left = '0';
    flash.style.width = '100%';
    flash.style.height = '100%';
    flash.style.backgroundColor = color;
    flash.style.opacity = '0';
    flash.style.zIndex = '9998';
    flash.style.pointerEvents = 'none';
    
    document.body.appendChild(flash);
    
    flash.animate([
        { opacity: 0 },
        { opacity: opacity },
        { opacity: 0 }
    ], {
        duration: duration,
        easing: 'ease-in-out'
    });
    
    setTimeout(() => {
        flash.remove();
    }, duration);
}

// Enhance result notification with visual effects
const originalShowResultNotification = showResultNotification;
showResultNotification = function(historyItem) {
    originalShowResultNotification(historyItem);
    
    if (historyItem.result === 'win') {
        createConfetti(true);
        flashScreen('#26a69a', 0.2, 400);
        // Play success sound (optional)
        // new Audio('/static/sounds/win.mp3').play();
    } else {
        shakeScreen(8, 400);
        flashScreen('#ef5350', 0.2, 400);
        // Play loss sound (optional)
        // new Audio('/static/sounds/loss.mp3').play();
    }
};

// Add pulse effect to balance on change
const originalUpdateBalance = updateBalance;
updateBalance = function() {
    const previousBalance = balance;
    originalUpdateBalance();
    
    if (balanceEl && previousBalance !== balance) {
        balanceEl.style.animation = 'none';
        setTimeout(() => {
            balanceEl.style.animation = 'balance-pulse 3s ease-in-out infinite';
        }, 10);
        
        // Add extra glow on win
        if (balance > previousBalance) {
            balanceEl.style.filter = 'drop-shadow(0 0 30px rgba(38, 166, 154, 1))';
            setTimeout(() => {
                balanceEl.style.filter = '';
            }, 1000);
        }
    }
};

// Chart Toolbar Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Timeframe buttons
    const tfButtons = document.querySelectorAll('.tf-btn');
    tfButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const newTimeframe = btn.dataset.tf;
            
            if (newTimeframe === currentTimeframe) {
                console.log(`⚠️ Timeframe ${newTimeframe} já está ativo`);
                return;
            }
            
            if (!isStreaming) {
                alert('Por favor, inicie o streaming primeiro antes de mudar o timeframe.');
                return;
            }
            
            console.log(`🔄 Mudando timeframe de ${currentTimeframe} para ${newTimeframe}`);
            
            // Update active state
            tfButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Update timeframe
            currentTimeframe = newTimeframe;
            
            // Update the timeframe select dropdown too
            if (timeframeSelect) {
                timeframeSelect.value = newTimeframe;
            }
            
            // Clear everything
            isHistoricalDataLoaded = false;
            candleData = [];
            priceUpdateCount = 0;
            
            // Clear indicators
            Object.keys(indicators).forEach(indicatorName => {
                if (indicators[indicatorName].active) {
                    removeIndicator(indicatorName);
                }
            });
            
            // Reset indicator buttons
            document.querySelectorAll('.indicator-btn').forEach(btn => {
                btn.classList.remove('active');
                indicators[btn.dataset.indicator].active = false;
            });
            
            // Clear price lines and markers
            priceLines.forEach(({ line }) => {
                try {
                    candlestickSeries.removePriceLine(line);
                } catch (e) {
                    console.log('Price line already removed');
                }
            });
            priceLines = [];
            markers = [];
            
            // Clear chart data
            if (candlestickSeries) {
                candlestickSeries.setData([]);
            }
            
            // Restart stream
            const currentSymbol = symbolInput.value;
            updateStatus('connecting', 'Reconectando...');
            
            console.log(`🔌 Parando stream atual...`);
            socket.emit('stop_stream');
            
            // Wait a bit longer to ensure clean stop
            setTimeout(() => {
                console.log(`🚀 Iniciando novo stream: ${currentSymbol} (${currentTimeframe})`);
                socket.emit('start_stream', {
                    symbol: currentSymbol,
                    timeframe: currentTimeframe
                });
            }, 1000);
        });
        
        // Set initial active state
        if (btn.dataset.tf === '1m') {
            btn.classList.add('active');
        }
    });
    
    // Indicator buttons
    const indicatorButtons = document.querySelectorAll('.indicator-btn');
    indicatorButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const indicatorName = btn.dataset.indicator;
            
            if (candleData.length < 50) {
                alert('Aguarde carregar mais dados históricos para adicionar indicadores.');
                return;
            }
            
            toggleIndicator(indicatorName);
            
            // Update button state
            btn.classList.toggle('active');
        });
    });
});

// Initialize on page load
window.addEventListener('load', () => {
    initChart();
    updateStatus('', 'Desconectado');
    updateBalance();
    renderHistory();
});

