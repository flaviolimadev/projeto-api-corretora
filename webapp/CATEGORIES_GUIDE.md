# 📊 API de Categorias - Guia Completo

## 🎯 **Novas Rotas Criadas!**

### ✅ **Rotas Implementadas:**
- **`GET /api/categories`** - Listar todas as categorias disponíveis
- **`GET /api/categories/<category_name>`** - Detalhes de uma categoria específica

---

## 🚀 **Categorias Disponíveis**

### **1. 💱 Forex (Moedas)**
- **Exchanges:** FX_IDC, FXCM, OANDA
- **Símbolos populares:** EURUSD, GBPUSD, USDJPY, USDCHF, AUDUSD, USDCAD, NZDUSD, EURGBP, EURJPY, GBPJPY
- **Descrição:** Pares de câmbio e moedas internacionais

### **2. ₿ Crypto (Criptomoedas)**
- **Exchanges:** BINANCE, COINBASE, KRAKEN, BITFINEX, HUOBI, KUCOIN
- **Símbolos populares:** BTCUSDT, ETHUSDT, ADAUSDT, DOTUSDT, LINKUSDT, UNIUSDT, LTCUSDT, BCHUSDT, XRPUSDT, BNBUSDT
- **Descrição:** Criptomoedas e tokens digitais

### **3. 📈 Stocks (Ações)**
- **Exchanges:** NASDAQ, NYSE, AMEX, LSE, TSE, HKEX, SSE
- **Símbolos populares:** AAPL, GOOGL, MSFT, AMZN, TSLA, META, NVDA, JPM, JNJ, V
- **Descrição:** Ações de empresas listadas em bolsas

### **4. 📊 Indices (Índices)**
- **Exchanges:** NASDAQ, NYSE, CBOE, CME
- **Símbolos populares:** NDX, COMP, SPX, DJI, RUT, VIX, ES1!, NQ1!, YM1!, RTY1!
- **Descrição:** Índices de mercado e indicadores

### **5. 🥇 Commodities (Commodities)**
- **Exchanges:** COMEX, NYMEX, CBOT, LME
- **Símbolos populares:** GC1!, SI1!, CL1!, NG1!, ZC1!, ZS1!, ZW1!, CAD1!, ALI1!, ZNI1!
- **Descrição:** Mercadorias e matérias-primas

### **6. 🏛️ Bonds (Títulos)**
- **Exchanges:** CBOT, EUREX, TSE
- **Símbolos populares:** TY1!, US1!, UB1!, FGBL1!, FGBM1!, FGBS1!, JGB1!, JGB2!, JGB3!, JGB4!
- **Descrição:** Títulos e obrigações governamentais

### **7. 📦 ETFs (Fundos)**
- **Exchanges:** NYSE, NASDAQ, AMEX
- **Símbolos populares:** SPY, QQQ, IWM, VTI, VEA, VWO, GLD, SLV, TLT, HYG
- **Descrição:** Fundos negociados em bolsa

### **8. ⏰ Futures (Futuros)**
- **Exchanges:** CME, CBOT, NYMEX, COMEX, EUREX
- **Símbolos populares:** ES1!, NQ1!, YM1!, RTY1!, ZC1!, ZS1!, CL1!, NG1!, GC1!, SI1!
- **Descrição:** Contratos futuros de commodities e índices

---

## 🧪 **Teste Imediato**

### **1. Inicie o Servidor:**
```bash
cd tradingview-scraper/webapp
python app.py
```

### **2. Teste com cURL:**
```bash
# Listar todas as categorias
curl "http://localhost:5000/api/categories"

# Detalhes da categoria Crypto
curl "http://localhost:5000/api/categories/crypto"

# Detalhes da categoria Forex
curl "http://localhost:5000/api/categories/forex"

# Detalhes da categoria Stocks
curl "http://localhost:5000/api/categories/stocks"
```

### **3. Teste no Navegador:**
```
http://localhost:5000/api/categories
http://localhost:5000/api/categories/crypto
http://localhost:5000/api/categories/forex
```

### **4. Execute o Teste Automatizado:**
```bash
python test_categories.py
```

---

## 📊 **Exemplo de Resposta - Todas as Categorias**

```json
{
  "categories": {
    "forex": {
      "name": "Forex",
      "description": "Moedas e pares de câmbio",
      "icon": "💱",
      "exchanges": ["FX_IDC", "FXCM", "OANDA"],
      "popular_symbols": ["FX_IDC:EURUSD", "FX_IDC:GBPUSD", "FX_IDC:USDJPY", ...],
      "timeframes": ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"]
    },
    "crypto": {
      "name": "Crypto",
      "description": "Criptomoedas e tokens digitais",
      "icon": "₿",
      "exchanges": ["BINANCE", "COINBASE", "KRAKEN", "BITFINEX", "HUOBI", "KUCOIN"],
      "popular_symbols": ["BINANCE:BTCUSDT", "BINANCE:ETHUSDT", "BINANCE:ADAUSDT", ...],
      "timeframes": ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"]
    }
  },
  "statistics": {
    "total_categories": 8,
    "total_exchanges": 25,
    "total_popular_symbols": 80,
    "supported_timeframes": ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"]
  },
  "generated_at": "2024-01-15T10:30:00.123456",
  "timezone": "UTC"
}
```

---

## 📈 **Exemplos de Uso Práticos**

### **Python:**
```python
import requests

# Obter todas as categorias
response = requests.get('http://localhost:5000/api/categories')
categories = response.json()

print(f"Total de categorias: {categories['statistics']['total_categories']}")

# Obter detalhes da categoria Crypto
crypto_response = requests.get('http://localhost:5000/api/categories/crypto')
crypto_data = crypto_response.json()

print(f"Crypto: {crypto_data['total_symbols']} símbolos populares")
print(f"Exchanges: {', '.join(crypto_data['exchanges'])}")
```

### **JavaScript:**
```javascript
// Obter todas as categorias
fetch('http://localhost:5000/api/categories')
  .then(response => response.json())
  .then(data => {
    console.log(`Total de categorias: ${data.statistics.total_categories}`);
    
    // Exibir categorias
    Object.entries(data.categories).forEach(([id, category]) => {
      console.log(`${category.icon} ${category.name}: ${category.popular_symbols.length} símbolos`);
    });
  });

// Obter detalhes de uma categoria específica
fetch('http://localhost:5000/api/categories/crypto')
  .then(response => response.json())
  .then(data => {
    console.log(`Crypto: ${data.total_symbols} símbolos`);
    console.log(`Exchanges: ${data.exchanges.join(', ')}`);
  });
```

### **Dashboard HTML:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Categories Dashboard</title>
    <style>
        .categories-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            padding: 20px;
        }
        .category-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .category-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .category-icon {
            font-size: 2em;
            margin-bottom: 10px;
        }
        .category-name {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .category-description {
            color: #666;
            margin-bottom: 15px;
        }
        .category-stats {
            display: flex;
            justify-content: space-around;
            margin-bottom: 15px;
        }
        .stat {
            background: #f0f0f0;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.9em;
        }
        .symbol-tag {
            display: inline-block;
            background: #e3f2fd;
            padding: 2px 8px;
            margin: 2px;
            border-radius: 12px;
            font-size: 0.8em;
        }
    </style>
</head>
<body>
    <h1>📊 TradingView Categories</h1>
    <div id="categories-container"></div>

    <script>
        async function loadCategories() {
            try {
                const response = await fetch('/api/categories');
                const data = await response.json();
                
                const container = document.getElementById('categories-container');
                container.innerHTML = createCategoryCards(data);
                
                // Adicionar event listeners
                document.querySelectorAll('.category-card').forEach(card => {
                    card.addEventListener('click', () => {
                        const categoryId = card.dataset.category;
                        loadCategoryDetails(categoryId);
                    });
                });
                
            } catch (error) {
                console.error('Erro ao carregar categorias:', error);
            }
        }
        
        async function loadCategoryDetails(categoryId) {
            try {
                const response = await fetch(`/api/categories/${categoryId}`);
                const data = await response.json();
                
                alert(`${data.name}\n\n${data.description}\n\nExchanges: ${data.exchanges.join(', ')}\nSímbolos: ${data.total_symbols}`);
                
            } catch (error) {
                console.error('Erro ao carregar detalhes:', error);
            }
        }
        
        function createCategoryCards(categoriesData) {
            const { categories } = categoriesData;
            
            let html = '<div class="categories-grid">';
            
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
                            `<span class="symbol-tag">+${category.popular_symbols.length - 3} mais</span>` : 
                            ''
                        }
                    </div>
                </div>`;
            });
            
            html += '</div>';
            return html;
        }
        
        // Carregar categorias quando a página carregar
        loadCategories();
    </script>
</body>
</html>
```

---

## 🔍 **Casos de Uso Avançados**

### **1. Filtro por Exchange:**
```javascript
async function getCategoriesByExchange(exchangeName) {
    const response = await fetch('/api/categories');
    const data = await response.json();
    
    const filteredCategories = Object.entries(data.categories)
        .filter(([_, category]) => category.exchanges.includes(exchangeName))
        .map(([id, category]) => ({ id, ...category }));
    
    return filteredCategories;
}

// Exemplo: Categorias que usam BINANCE
getCategoriesByExchange('BINANCE').then(categories => {
    console.log('Categorias com BINANCE:', categories);
});
```

### **2. Busca por Símbolo:**
```javascript
async function findSymbolInCategories(symbol) {
    const response = await fetch('/api/categories');
    const data = await response.json();
    
    const results = [];
    
    Object.entries(data.categories).forEach(([categoryId, category]) => {
        const foundSymbols = category.popular_symbols.filter(s => 
            s.toLowerCase().includes(symbol.toLowerCase())
        );
        
        if (foundSymbols.length > 0) {
            results.push({
                category: categoryId,
                name: category.name,
                symbols: foundSymbols
            });
        }
    });
    
    return results;
}

// Exemplo: Buscar símbolos que contenham "BTC"
findSymbolInCategories('BTC').then(results => {
    console.log('Símbolos com BTC:', results);
});
```

### **3. Estatísticas de Categorias:**
```javascript
async function getCategoryStatistics() {
    const response = await fetch('/api/categories');
    const data = await response.json();
    
    const stats = {
        totalCategories: data.statistics.total_categories,
        totalExchanges: data.statistics.total_exchanges,
        totalSymbols: data.statistics.total_popular_symbols,
        averageSymbolsPerCategory: Math.round(data.statistics.total_popular_symbols / data.statistics.total_categories),
        categoriesByExchange: {}
    };
    
    // Contar categorias por exchange
    Object.values(data.categories).forEach(category => {
        category.exchanges.forEach(exchange => {
            if (!stats.categoriesByExchange[exchange]) {
                stats.categoriesByExchange[exchange] = 0;
            }
            stats.categoriesByExchange[exchange]++;
        });
    });
    
    return stats;
}
```

---

## 🚨 **Casos de Erro**

### **Categoria não encontrada:**
```bash
curl "http://localhost:5000/api/categories/invalid"
# Retorna: {"error": "Categoria não encontrada", "available_categories": [...], "received": "invalid"}
```

### **Servidor não disponível:**
```bash
curl "http://localhost:5000/api/categories"
# Retorna: Connection refused ou timeout
```

---

## 📚 **Arquivos Criados**

### ✅ **Backend:**
- `app.py` - Rotas `/api/categories` e `/api/categories/<category>` adicionadas

### ✅ **Testes:**
- `test_categories.py` - Script de teste automatizado

### ✅ **Exemplos:**
- `categories_example.js` - Exemplos de uso em JavaScript

### ✅ **Documentação:**
- `CATEGORIES_GUIDE.md` - Este guia completo

---

## ✅ **Status da Implementação**

- ✅ **8 categorias** implementadas (Forex, Crypto, Stocks, Indices, Commodities, Bonds, ETFs, Futures)
- ✅ **25 exchanges** suportados
- ✅ **80 símbolos populares** incluídos
- ✅ **2 rotas** funcionais
- ✅ **Validação de erros** completa
- ✅ **Documentação** detalhada
- ✅ **Exemplos de uso** em Python e JavaScript
- ✅ **Testes automatizados** criados

**API de Categorias pronta para uso!** 🚀📊

---

## 🎯 **Próximos Passos Sugeridos**

1. **✅ Testar as rotas** com os exemplos fornecidos
2. **✅ Integrar em aplicações** usando os códigos de exemplo
3. **✅ Criar dashboard** web com as categorias
4. **✅ Implementar busca** por símbolos
5. **✅ Adicionar filtros** por exchange ou timeframe

**A API de Categorias está completa e funcionando!** 🎉📈
