/**
 * Exemplo de uso da API de Category Assets
 * Demonstra como consumir a rota /api/category-assets
 */

// Configuração
const API_BASE_URL = 'http://localhost:5000';

/**
 * Obter ativos de uma categoria específica de uma exchange
 * @param {string} category - Categoria (crypto, stocks, forex, etc.)
 * @param {string} exchange - Exchange (BINANCE, NASDAQ, NYSE, etc.)
 * @param {number} limit - Número máximo de ativos (padrão: 50)
 * @param {string} search - Termo de busca opcional
 * @returns {Promise<Object>} Dados dos ativos
 */
async function getCategoryAssets(category, exchange, limit = 50, search = '') {
    try {
        console.log(`🔍 Buscando ativos: ${category} da ${exchange} (limite: ${limit})`);
        
        const params = new URLSearchParams({
            category: category,
            exchange: exchange,
            limit: limit.toString()
        });
        
        if (search) {
            params.append('search', search);
        }
        
        const response = await fetch(`${API_BASE_URL}/api/category-assets?${params}`);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || `HTTP ${response.status}`);
        }
        
        return data;
    } catch (error) {
        console.error('❌ Erro ao obter ativos:', error);
        throw error;
    }
}

/**
 * Exibir ativos de forma formatada
 * @param {Object} assetsData - Dados dos ativos
 */
function displayAssets(assetsData) {
    console.log(`\n📊 ATIVOS DA CATEGORIA: ${assetsData.category.toUpperCase()}`);
    console.log('='.repeat(60));
    
    console.log(`🏢 Exchange: ${assetsData.exchange}`);
    console.log(`📈 Total de ativos: ${assetsData.total_assets}`);
    console.log(`🔢 Limite: ${assetsData.limit}`);
    if (assetsData.search_term) {
        console.log(`🔍 Termo de busca: ${assetsData.search_term}`);
    }
    
    console.log(`\n📋 Ativos encontrados:`);
    assetsData.assets.forEach((asset, index) => {
        console.log(`   ${index + 1}. ${asset.symbol}`);
        console.log(`      Descrição: ${asset.description}`);
        console.log(`      Tipo: ${asset.type}`);
        console.log(`      Query: ${asset.search_query}`);
        console.log('');
    });
    
    console.log(`\nℹ️  Informações da categoria:`);
    console.log(`   Nome: ${assetsData.category_info.name}`);
    console.log(`   Descrição: ${assetsData.category_info.description}`);
    console.log(`   Exchanges suportadas: ${assetsData.category_info.supported_exchanges.join(', ')}`);
}

/**
 * Criar tabela HTML de ativos
 * @param {Object} assetsData - Dados dos ativos
 * @returns {string} HTML da tabela
 */
function createAssetsTable(assetsData) {
    let html = `
    <div class="assets-container">
        <h2>📊 ${assetsData.category.toUpperCase()} - ${assetsData.exchange}</h2>
        <div class="assets-info">
            <span class="info-item">Total: ${assetsData.total_assets}</span>
            <span class="info-item">Limite: ${assetsData.limit}</span>
            ${assetsData.search_term ? `<span class="info-item">Busca: ${assetsData.search_term}</span>` : ''}
        </div>
        <table class="assets-table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Símbolo</th>
                    <th>Descrição</th>
                    <th>Tipo</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>`;
    
    assetsData.assets.forEach((asset, index) => {
        html += `
            <tr>
                <td>${index + 1}</td>
                <td><strong>${asset.symbol}</strong></td>
                <td>${asset.description}</td>
                <td><span class="type-badge ${asset.type}">${asset.type}</span></td>
                <td>
                    <button onclick="getCurrentPrice('${asset.symbol}')" class="btn-price">💰 Preço</button>
                    <button onclick="getChart('${asset.symbol}')" class="btn-chart">📈 Gráfico</button>
                </td>
            </tr>`;
    });
    
    html += `
            </tbody>
        </table>
    </div>`;
    
    return html;
}

/**
 * Criar seletor de categoria e exchange
 * @returns {string} HTML do seletor
 */
function createCategoryExchangeSelector() {
    return `
    <div class="selector-container">
        <div class="selector-group">
            <label for="category-select">Categoria:</label>
            <select id="category-select" class="form-select">
                <option value="">Selecione uma categoria...</option>
                <option value="crypto">₿ Crypto</option>
                <option value="stocks">📈 Stocks</option>
                <option value="forex">💱 Forex</option>
                <option value="indices">📊 Indices</option>
                <option value="commodities">🥇 Commodities</option>
                <option value="bonds">🏛️ Bonds</option>
                <option value="etfs">📦 ETFs</option>
                <option value="futures">⏰ Futures</option>
            </select>
        </div>
        
        <div class="selector-group">
            <label for="exchange-select">Exchange:</label>
            <select id="exchange-select" class="form-select">
                <option value="">Selecione uma exchange...</option>
                <option value="BINANCE">BINANCE</option>
                <option value="COINBASE">COINBASE</option>
                <option value="NASDAQ">NASDAQ</option>
                <option value="NYSE">NYSE</option>
                <option value="FX_IDC">FX_IDC</option>
                <option value="COMEX">COMEX</option>
                <option value="NYMEX">NYMEX</option>
            </select>
        </div>
        
        <div class="selector-group">
            <label for="limit-input">Limite:</label>
            <input type="number" id="limit-input" class="form-input" value="20" min="1" max="200">
        </div>
        
        <div class="selector-group">
            <label for="search-input">Busca (opcional):</label>
            <input type="text" id="search-input" class="form-input" placeholder="Ex: BTC, AAPL, EUR">
        </div>
        
        <button onclick="loadAssets()" class="btn-primary">🔍 Buscar Ativos</button>
    </div>`;
}

/**
 * Exemplo de uso básico
 */
async function exemploBasico() {
    console.log('🚀 Exemplo Básico - API de Category Assets');
    console.log('='.repeat(60));
    
    try {
        // Obter criptomoedas da BINANCE
        const cryptoAssets = await getCategoryAssets('crypto', 'BINANCE', 10);
        displayAssets(cryptoAssets);
        
        // Obter ações da NASDAQ
        const stockAssets = await getCategoryAssets('stocks', 'NASDAQ', 8);
        displayAssets(stockAssets);
        
    } catch (error) {
        console.error('❌ Erro no exemplo básico:', error);
    }
}

/**
 * Exemplo de dashboard interativo
 */
function exemploDashboard() {
    console.log('📊 Exemplo Dashboard - Category Assets');
    console.log('='.repeat(60));
    
    // Criar seletor
    const selectorHTML = createCategoryExchangeSelector();
    console.log('Seletor HTML criado:');
    console.log(selectorHTML);
    
    // Adicionar event listeners
    console.log('\nJavaScript para o dashboard:');
    console.log(`
// Função para carregar ativos
async function loadAssets() {
    const category = document.getElementById('category-select').value;
    const exchange = document.getElementById('exchange-select').value;
    const limit = parseInt(document.getElementById('limit-input').value);
    const search = document.getElementById('search-input').value;
    
    if (!category || !exchange) {
        alert('Por favor, selecione uma categoria e uma exchange');
        return;
    }
    
    try {
        const assetsData = await getCategoryAssets(category, exchange, limit, search);
        const tableHTML = createAssetsTable(assetsData);
        document.getElementById('assets-container').innerHTML = tableHTML;
    } catch (error) {
        console.error('Erro ao carregar ativos:', error);
        alert('Erro ao carregar ativos: ' + error.message);
    }
}

// Função para obter preço atual
async function getCurrentPrice(symbol) {
    try {
        const response = await fetch(\`/api/current-candle?symbol=\${symbol}&timeframe=1m\`);
        const data = await response.json();
        alert(\`\${symbol}: $\${data.close} (\${data.price_change_percent}%)\`);
    } catch (error) {
        console.error('Erro ao obter preço:', error);
    }
}

// Função para abrir gráfico
function getChart(symbol) {
    window.open(\`/?symbol=\${symbol}\`, '_blank');
}
    `);
}

/**
 * Exemplo de busca avançada
 */
async function exemploBuscaAvancada() {
    console.log('🔍 Exemplo Busca Avançada - Category Assets');
    console.log('='.repeat(60));
    
    try {
        // Buscar por termo específico
        const btcAssets = await getCategoryAssets('crypto', 'BINANCE', 10, 'BTC');
        console.log('🔍 Busca por "BTC":');
        displayAssets(btcAssets);
        
        // Buscar ações da Apple
        const appleAssets = await getCategoryAssets('stocks', 'NASDAQ', 5, 'AAPL');
        console.log('\n🔍 Busca por "AAPL":');
        displayAssets(appleAssets);
        
        // Buscar pares de EUR
        const eurAssets = await getCategoryAssets('forex', 'FX_IDC', 8, 'EUR');
        console.log('\n🔍 Busca por "EUR":');
        displayAssets(eurAssets);
        
    } catch (error) {
        console.error('❌ Erro na busca avançada:', error);
    }
}

/**
 * Exemplo de comparação de exchanges
 */
async function exemploComparacaoExchanges() {
    console.log('🔄 Exemplo Comparação de Exchanges');
    console.log('='.repeat(60));
    
    try {
        const exchanges = ['BINANCE', 'COINBASE', 'KRAKEN'];
        
        console.log('📊 Comparando exchanges de crypto:');
        for (const exchange of exchanges) {
            try {
                const assets = await getCategoryAssets('crypto', exchange, 5);
                console.log(`\n${exchange}:`);
                console.log(`   Total: ${assets.total_assets} ativos`);
                console.log(`   Primeiros 3: ${assets.assets.slice(0, 3).map(a => a.symbol).join(', ')}`);
            } catch (error) {
                console.log(`\n${exchange}: ERRO - ${error.message}`);
            }
        }
        
    } catch (error) {
        console.error('❌ Erro na comparação:', error);
    }
}

/**
 * Exemplo de filtro por tipo
 */
async function exemploFiltroPorTipo() {
    console.log('🔍 Exemplo Filtro por Tipo');
    console.log('='.repeat(60));
    
    try {
        const assets = await getCategoryAssets('stocks', 'NASDAQ', 20);
        
        // Agrupar por tipo
        const assetsByType = {};
        assets.assets.forEach(asset => {
            const type = asset.type || 'unknown';
            if (!assetsByType[type]) {
                assetsByType[type] = [];
            }
            assetsByType[type].push(asset);
        });
        
        console.log('📊 Ativos agrupados por tipo:');
        Object.entries(assetsByType).forEach(([type, typeAssets]) => {
            console.log(`\n${type.toUpperCase()}: ${typeAssets.length} ativos`);
            typeAssets.slice(0, 3).forEach(asset => {
                console.log(`   - ${asset.symbol}: ${asset.description}`);
            });
            if (typeAssets.length > 3) {
                console.log(`   ... e mais ${typeAssets.length - 3} ativos`);
            }
        });
        
    } catch (error) {
        console.error('❌ Erro no filtro por tipo:', error);
    }
}

// Exemplos de uso
console.log('🎯 API de Category Assets - Exemplos de Uso');
console.log('='.repeat(60));
console.log('1. exemploBasico() - Exemplo básico');
console.log('2. exemploDashboard() - Dashboard interativo');
console.log('3. exemploBuscaAvancada() - Busca com termos específicos');
console.log('4. exemploComparacaoExchanges() - Comparar exchanges');
console.log('5. exemploFiltroPorTipo() - Filtrar por tipo de ativo');
console.log('6. getCategoryAssets(category, exchange, limit, search) - Buscar ativos');
console.log('='.repeat(60));

// Executar exemplo básico automaticamente
exemploBasico();
