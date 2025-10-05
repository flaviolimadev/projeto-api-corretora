/**
 * Exemplo de uso da API de Categorias
 * Demonstra como consumir as rotas /api/categories e /api/categories/<category>
 */

// Configuração
const API_BASE_URL = 'http://localhost:5000';

/**
 * Obter todas as categorias disponíveis
 * @returns {Promise<Object>} Dados de todas as categorias
 */
async function getAllCategories() {
    try {
        console.log('🔍 Buscando todas as categorias...');
        
        const response = await fetch(`${API_BASE_URL}/api/categories`);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || `HTTP ${response.status}`);
        }
        
        return data;
    } catch (error) {
        console.error('❌ Erro ao obter categorias:', error);
        throw error;
    }
}

/**
 * Obter detalhes de uma categoria específica
 * @param {string} categoryName - Nome da categoria (ex: crypto, forex, stocks)
 * @returns {Promise<Object>} Dados da categoria
 */
async function getCategoryDetails(categoryName) {
    try {
        console.log(`🔍 Buscando detalhes da categoria: ${categoryName}`);
        
        const response = await fetch(`${API_BASE_URL}/api/categories/${categoryName}`);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || `HTTP ${response.status}`);
        }
        
        return data;
    } catch (error) {
        console.error(`❌ Erro ao obter categoria ${categoryName}:`, error);
        throw error;
    }
}

/**
 * Exibir todas as categorias de forma formatada
 * @param {Object} categoriesData - Dados das categorias
 */
function displayAllCategories(categoriesData) {
    console.log('\n📊 TODAS AS CATEGORIAS DISPONÍVEIS');
    console.log('='.repeat(50));
    
    const { categories, statistics } = categoriesData;
    
    console.log(`📈 Estatísticas:`);
    console.log(`   Total de categorias: ${statistics.total_categories}`);
    console.log(`   Total de exchanges: ${statistics.total_exchanges}`);
    console.log(`   Total de símbolos populares: ${statistics.total_popular_symbols}`);
    console.log(`   Timeframes suportados: ${statistics.supported_timeframes.join(', ')}`);
    
    console.log('\n📋 Categorias:');
    Object.entries(categories).forEach(([categoryId, category]) => {
        console.log(`\n${category.icon} ${category.name}`);
        console.log(`   Descrição: ${category.description}`);
        console.log(`   Exchanges: ${category.exchanges.join(', ')}`);
        console.log(`   Símbolos populares: ${category.popular_symbols.length}`);
        console.log(`   Timeframes: ${category.timeframes.join(', ')}`);
    });
}

/**
 * Exibir detalhes de uma categoria específica
 * @param {Object} categoryData - Dados da categoria
 */
function displayCategoryDetails(categoryData) {
    console.log(`\n📊 DETALHES DA CATEGORIA: ${categoryData.name}`);
    console.log('='.repeat(50));
    
    console.log(`📝 Descrição: ${categoryData.description}`);
    console.log(`🎯 Ícone: ${categoryData.icon}`);
    console.log(`🏢 Total de exchanges: ${categoryData.total_exchanges}`);
    console.log(`📈 Total de símbolos: ${categoryData.total_symbols}`);
    
    console.log(`\n🏢 Exchanges:`);
    categoryData.exchanges.forEach(exchange => {
        console.log(`   - ${exchange}`);
    });
    
    console.log(`\n📈 Símbolos populares:`);
    categoryData.popular_symbols.forEach((symbol, index) => {
        console.log(`   ${index + 1}. ${symbol}`);
    });
    
    console.log(`\n⏰ Timeframes suportados:`);
    console.log(`   ${categoryData.timeframes.join(', ')}`);
}

/**
 * Criar seletor de categorias para HTML
 * @param {Object} categoriesData - Dados das categorias
 * @returns {string} HTML do seletor
 */
function createCategorySelector(categoriesData) {
    const { categories } = categoriesData;
    
    let html = '<select id="category-selector" class="category-selector">\n';
    html += '  <option value="">Selecione uma categoria...</option>\n';
    
    Object.entries(categories).forEach(([categoryId, category]) => {
        html += `  <option value="${categoryId}">${category.icon} ${category.name}</option>\n`;
    });
    
    html += '</select>';
    return html;
}

/**
 * Criar cards de categorias para HTML
 * @param {Object} categoriesData - Dados das categorias
 * @returns {string} HTML dos cards
 */
function createCategoryCards(categoriesData) {
    const { categories } = categoriesData;
    
    let html = '<div class="categories-grid">\n';
    
    Object.entries(categories).forEach(([categoryId, category]) => {
        html += `
  <div class="category-card" data-category="${categoryId}">
    <div class="category-icon">${category.icon}</div>
    <div class="category-name">${category.name}</div>
    <div class="category-description">${category.description}</div>
    <div class="category-stats">
      <span class="stat">${category.exchanges.length} exchanges</span>
      <span class="stat">${category.popular_symbols.length} símbolos</span>
    </div>
    <div class="category-symbols">
      ${category.popular_symbols.slice(0, 3).map(symbol => 
        `<span class="symbol-tag">${symbol}</span>`
      ).join('')}
      ${category.popular_symbols.length > 3 ? 
        `<span class="symbol-more">+${category.popular_symbols.length - 3} mais</span>` : 
        ''
      }
    </div>
  </div>`;
    });
    
    html += '\n</div>';
    return html;
}

/**
 * Exemplo de uso básico
 */
async function exemploBasico() {
    console.log('🚀 Exemplo Básico - API de Categorias');
    console.log('='.repeat(50));
    
    try {
        // Obter todas as categorias
        const allCategories = await getAllCategories();
        displayAllCategories(allCategories);
        
        // Obter detalhes da categoria Crypto
        const cryptoDetails = await getCategoryDetails('crypto');
        displayCategoryDetails(cryptoDetails);
        
    } catch (error) {
        console.error('❌ Erro no exemplo básico:', error);
    }
}

/**
 * Exemplo de dashboard de categorias
 */
async function exemploDashboard() {
    console.log('📊 Exemplo Dashboard - Categorias');
    console.log('='.repeat(50));
    
    try {
        const categoriesData = await getAllCategories();
        
        // Criar seletor de categorias
        const selectorHTML = createCategorySelector(categoriesData);
        console.log('Seletor HTML criado:');
        console.log(selectorHTML);
        
        // Criar cards de categorias
        const cardsHTML = createCategoryCards(categoriesData);
        console.log('\nCards HTML criados:');
        console.log(cardsHTML);
        
        // Adicionar event listener para o seletor
        console.log('\nJavaScript para o seletor:');
        console.log(`
document.getElementById('category-selector').addEventListener('change', async (e) => {
    const categoryId = e.target.value;
    if (categoryId) {
        try {
            const categoryDetails = await getCategoryDetails(categoryId);
            displayCategoryDetails(categoryDetails);
        } catch (error) {
            console.error('Erro ao carregar categoria:', error);
        }
    }
});
        `);
        
    } catch (error) {
        console.error('❌ Erro no dashboard:', error);
    }
}

/**
 * Exemplo de comparação de categorias
 */
async function exemploComparacao() {
    console.log('🔍 Exemplo Comparação - Categorias');
    console.log('='.repeat(50));
    
    try {
        const categoriesData = await getAllCategories();
        const { categories } = categoriesData;
        
        console.log('📊 Comparação de Categorias:');
        console.log('='.repeat(40));
        
        Object.entries(categories).forEach(([categoryId, category]) => {
            console.log(`${category.icon} ${category.name}:`);
            console.log(`   Exchanges: ${category.exchanges.length}`);
            console.log(`   Símbolos: ${category.popular_symbols.length}`);
            console.log(`   Timeframes: ${category.timeframes.length}`);
            console.log('');
        });
        
    } catch (error) {
        console.error('❌ Erro na comparação:', error);
    }
}

/**
 * Exemplo de filtro por exchange
 */
async function exemploFiltroExchange() {
    console.log('🔍 Exemplo Filtro por Exchange');
    console.log('='.repeat(50));
    
    try {
        const categoriesData = await getAllCategories();
        const { categories } = categoriesData;
        
        // Filtrar categorias que usam BINANCE
        const binanceCategories = Object.entries(categories)
            .filter(([_, category]) => category.exchanges.includes('BINANCE'))
            .map(([id, category]) => ({ id, ...category }));
        
        console.log('📊 Categorias que usam BINANCE:');
        binanceCategories.forEach(category => {
            console.log(`   ${category.icon} ${category.name}: ${category.popular_symbols.length} símbolos`);
        });
        
        // Filtrar categorias que usam NASDAQ
        const nasdaqCategories = Object.entries(categories)
            .filter(([_, category]) => category.exchanges.includes('NASDAQ'))
            .map(([id, category]) => ({ id, ...category }));
        
        console.log('\n📊 Categorias que usam NASDAQ:');
        nasdaqCategories.forEach(category => {
            console.log(`   ${category.icon} ${category.name}: ${category.popular_symbols.length} símbolos`);
        });
        
    } catch (error) {
        console.error('❌ Erro no filtro:', error);
    }
}

// Exemplos de uso
console.log('🎯 API de Categorias - Exemplos de Uso');
console.log('='.repeat(50));
console.log('1. exemploBasico() - Exemplo básico');
console.log('2. exemploDashboard() - Dashboard HTML');
console.log('3. exemploComparacao() - Comparar categorias');
console.log('4. exemploFiltroExchange() - Filtrar por exchange');
console.log('5. getAllCategories() - Obter todas as categorias');
console.log('6. getCategoryDetails(category) - Obter categoria específica');
console.log('='.repeat(50));

// Executar exemplo básico automaticamente
exemploBasico();
