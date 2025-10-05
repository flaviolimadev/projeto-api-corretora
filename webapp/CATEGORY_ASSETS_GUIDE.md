# 📊 API de Category Assets - Guia Completo

## 🎯 **Nova Rota Criada!**

**`GET /api/category-assets`** - Obter todos os ativos de uma categoria específica baseada na exchange

---

## 🚀 **Funcionalidades**

### ✅ **Parâmetros:**
- `category` (obrigatório): Nome da categoria (crypto, stocks, forex, etc.)
- `exchange` (obrigatório): Nome da exchange (BINANCE, NASDAQ, NYSE, etc.)
- `limit` (opcional): Número máximo de ativos (padrão: 50, máximo: 200)
- `search` (opcional): Termo de busca para filtrar ativos

### ✅ **Recursos:**
- **Busca inteligente** baseada na categoria e exchange
- **Filtros automáticos** para validar ativos por categoria
- **Fallback para símbolos populares** se não encontrar ativos
- **Ordenação por relevância** (símbolos populares primeiro)
- **Validação completa** de parâmetros e exchanges
- **Integração com TradingView** para busca em tempo real

---

## 🧪 **Teste Imediato**

### **1. Inicie o Servidor:**
```bash
cd tradingview-scraper/webapp
python app.py
```

### **2. Teste com cURL:**
```bash
# Criptomoedas da BINANCE
curl "http://localhost:5000/api/category-assets?category=crypto&exchange=BINANCE&limit=10"

# Ações da NASDAQ
curl "http://localhost:5000/api/category-assets?category=stocks&exchange=NASDAQ&limit=15"

# Forex da FX_IDC
curl "http://localhost:5000/api/category-assets?category=forex&exchange=FX_IDC&limit=8"

# Busca por termo específico
curl "http://localhost:5000/api/category-assets?category=crypto&exchange=BINANCE&search=BTC&limit=5"
```

### **3. Teste no Navegador:**
```
http://localhost:5000/api/category-assets?category=crypto&exchange=BINANCE&limit=10
http://localhost:5000/api/category-assets?category=stocks&exchange=NASDAQ&limit=15
```

### **4. Execute o Teste Automatizado:**
```bash
python test_category_assets.py
```

---

## 📊 **Exemplo de Resposta**

```json
{
  "category": "crypto",
  "exchange": "BINANCE",
  "total_assets": 10,
  "limit": 10,
  "search_term": "",
  "assets": [
    {
      "symbol": "BINANCE:BTCUSDT",
      "exchange": "BINANCE",
      "description": "Bitcoin / Tether USD",
      "type": "crypto",
      "category": "crypto",
      "search_query": "BTC"
    },
    {
      "symbol": "BINANCE:ETHUSDT",
      "exchange": "BINANCE",
      "description": "Ethereum / Tether USD",
      "type": "crypto",
      "category": "crypto",
      "search_query": "ETH"
    }
  ],
  "category_info": {
    "name": "Crypto",
    "description": "Criptomoedas e tokens digitais",
    "supported_exchanges": ["BINANCE", "COINBASE", "KRAKEN", "BITFINEX", "HUOBI", "KUCOIN"]
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

# Obter criptomoedas da BINANCE
response = requests.get('http://localhost:5000/api/category-assets', params={
    'category': 'crypto',
    'exchange': 'BINANCE',
    'limit': 20
})

data = response.json()
print(f"Encontrados {data['total_assets']} ativos de {data['category']} na {data['exchange']}")

for asset in data['assets']:
    print(f"- {asset['symbol']}: {asset['description']}")

# Buscar por termo específico
btc_response = requests.get('http://localhost:5000/api/category-assets', params={
    'category': 'crypto',
    'exchange': 'BINANCE',
    'search': 'BTC',
    'limit': 5
})

btc_data = btc_response.json()
print(f"Ativos com BTC: {len(btc_data['assets'])}")
```

### **JavaScript:**
```javascript
// Obter ativos de uma categoria
async function getCategoryAssets(category, exchange, limit = 50, search = '') {
    const params = new URLSearchParams({
        category: category,
        exchange: exchange,
        limit: limit.toString()
    });
    
    if (search) {
        params.append('search', search);
    }
    
    const response = await fetch(`http://localhost:5000/api/category-assets?${params}`);
    return await response.json();
}

// Uso
getCategoryAssets('crypto', 'BINANCE', 10)
    .then(data => {
        console.log(`Encontrados ${data.total_assets} ativos`);
        data.assets.forEach(asset => {
            console.log(`${asset.symbol}: ${asset.description}`);
        });
    });

// Busca por termo específico
getCategoryAssets('stocks', 'NASDAQ', 15, 'AAPL')
    .then(data => {
        console.log(`Ações da Apple: ${data.assets.length} encontradas`);
    });
```

### **Dashboard HTML:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Category Assets Dashboard</title>
    <style>
        .selector-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
            padding: 20px;
            background: #f5f5f5;
            border-radius: 8px;
        }
        .form-select, .form-input {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }
        .btn-primary {
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        .btn-primary:hover {
            background: #0056b3;
        }
        .assets-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        .assets-table th,
        .assets-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        .assets-table th {
            background: #f8f9fa;
            font-weight: bold;
        }
        .type-badge {
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }
        .type-badge.crypto { background: #e3f2fd; color: #1976d2; }
        .type-badge.stocks { background: #e8f5e8; color: #2e7d32; }
        .type-badge.forex { background: #fff3e0; color: #f57c00; }
        .type-badge.popular { background: #f3e5f5; color: #7b1fa2; }
        .btn-price, .btn-chart {
            padding: 4px 8px;
            margin: 2px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
        }
        .btn-price { background: #28a745; color: white; }
        .btn-chart { background: #17a2b8; color: white; }
    </style>
</head>
<body>
    <h1>📊 Category Assets Dashboard</h1>
    
    <div class="selector-container">
        <div>
            <label for="category-select">Categoria:</label>
            <select id="category-select" class="form-select">
                <option value="">Selecione...</option>
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
        
        <div>
            <label for="exchange-select">Exchange:</label>
            <select id="exchange-select" class="form-select">
                <option value="">Selecione...</option>
                <option value="BINANCE">BINANCE</option>
                <option value="COINBASE">COINBASE</option>
                <option value="NASDAQ">NASDAQ</option>
                <option value="NYSE">NYSE</option>
                <option value="FX_IDC">FX_IDC</option>
                <option value="COMEX">COMEX</option>
                <option value="NYMEX">NYMEX</option>
            </select>
        </div>
        
        <div>
            <label for="limit-input">Limite:</label>
            <input type="number" id="limit-input" class="form-input" value="20" min="1" max="200">
        </div>
        
        <div>
            <label for="search-input">Busca:</label>
            <input type="text" id="search-input" class="form-input" placeholder="Ex: BTC, AAPL">
        </div>
        
        <div>
            <button onclick="loadAssets()" class="btn-primary">🔍 Buscar Ativos</button>
        </div>
    </div>
    
    <div id="assets-container">
        <p>Selecione uma categoria e exchange para começar</p>
    </div>

    <script>
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
                const response = await fetch(`/api/category-assets?category=${category}&exchange=${exchange}&limit=${limit}&search=${search}`);
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || `HTTP ${response.status}`);
                }
                
                displayAssets(data);
            } catch (error) {
                console.error('Erro ao carregar ativos:', error);
                alert('Erro ao carregar ativos: ' + error.message);
            }
        }
        
        function displayAssets(assetsData) {
            const container = document.getElementById('assets-container');
            
            let html = `
                <h2>📊 ${assetsData.category.toUpperCase()} - ${assetsData.exchange}</h2>
                <div style="margin-bottom: 20px;">
                    <span style="background: #e3f2fd; padding: 4px 8px; border-radius: 4px; margin-right: 10px;">
                        Total: ${assetsData.total_assets}
                    </span>
                    <span style="background: #e8f5e8; padding: 4px 8px; border-radius: 4px; margin-right: 10px;">
                        Limite: ${assetsData.limit}
                    </span>
                    ${assetsData.search_term ? `<span style="background: #fff3e0; padding: 4px 8px; border-radius: 4px;">Busca: ${assetsData.search_term}</span>` : ''}
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
                </table>`;
            
            container.innerHTML = html;
        }
        
        async function getCurrentPrice(symbol) {
            try {
                const response = await fetch(`/api/current-candle?symbol=${symbol}&timeframe=1m`);
                const data = await response.json();
                alert(`${symbol}: $${data.close} (${data.price_change_percent}%)`);
            } catch (error) {
                console.error('Erro ao obter preço:', error);
                alert('Erro ao obter preço: ' + error.message);
            }
        }
        
        function getChart(symbol) {
            window.open(`/?symbol=${symbol}`, '_blank');
        }
    </script>
</body>
</html>
```

---

## 🔍 **Casos de Uso Avançados**

### **1. Busca Inteligente por Categoria:**
```javascript
// Buscar ativos de crypto em diferentes exchanges
const exchanges = ['BINANCE', 'COINBASE', 'KRAKEN'];

async function compareCryptoExchanges() {
    const results = {};
    
    for (const exchange of exchanges) {
        try {
            const data = await getCategoryAssets('crypto', exchange, 10);
            results[exchange] = {
                total: data.total_assets,
                symbols: data.assets.map(a => a.symbol)
            };
        } catch (error) {
            results[exchange] = { error: error.message };
        }
    }
    
    console.log('Comparação de exchanges crypto:', results);
}
```

### **2. Filtro por Tipo de Ativo:**
```javascript
async function getAssetsByType(category, exchange, type) {
    const data = await getCategoryAssets(category, exchange, 100);
    
    const filteredAssets = data.assets.filter(asset => 
        asset.type.toLowerCase().includes(type.toLowerCase())
    );
    
    return {
        ...data,
        assets: filteredAssets,
        total_assets: filteredAssets.length
    };
}

// Exemplo: Buscar apenas ações de tecnologia
getAssetsByType('stocks', 'NASDAQ', 'tech').then(data => {
    console.log(`Ações de tecnologia: ${data.total_assets} encontradas`);
});
```

### **3. Monitoramento de Novos Ativos:**
```javascript
class AssetMonitor {
    constructor(category, exchange, interval = 30000) {
        this.category = category;
        this.exchange = exchange;
        this.interval = interval;
        this.lastAssets = new Set();
        this.isRunning = false;
    }
    
    async start() {
        this.isRunning = true;
        console.log(`Iniciando monitoramento: ${this.category} - ${this.exchange}`);
        
        while (this.isRunning) {
            try {
                const data = await getCategoryAssets(this.category, this.exchange, 50);
                const currentAssets = new Set(data.assets.map(a => a.symbol));
                
                // Detectar novos ativos
                const newAssets = [...currentAssets].filter(symbol => 
                    !this.lastAssets.has(symbol)
                );
                
                if (newAssets.length > 0) {
                    console.log(`🆕 Novos ativos encontrados: ${newAssets.join(', ')}`);
                }
                
                this.lastAssets = currentAssets;
                
            } catch (error) {
                console.error('Erro no monitoramento:', error);
            }
            
            await new Promise(resolve => setTimeout(resolve, this.interval));
        }
    }
    
    stop() {
        this.isRunning = false;
        console.log('Monitoramento parado');
    }
}

// Usar o monitor
const monitor = new AssetMonitor('crypto', 'BINANCE', 60000); // Verificar a cada minuto
monitor.start();
```

---

## 🚨 **Casos de Erro**

### **Categoria inválida:**
```bash
curl "http://localhost:5000/api/category-assets?category=invalid&exchange=BINANCE"
# Retorna: {"error": "Categoria inválida", "valid_categories": [...], "received": "invalid"}
```

### **Exchange não suportada:**
```bash
curl "http://localhost:5000/api/category-assets?category=crypto&exchange=INVALID"
# Retorna: {"error": "Exchange não suportada para esta categoria", "supported_exchanges": [...], "received": "INVALID"}
```

### **Parâmetros obrigatórios ausentes:**
```bash
curl "http://localhost:5000/api/category-assets"
# Retorna: {"error": "Parâmetro 'category' é obrigatório", "example": "..."}
```

---

## 📚 **Arquivos Criados**

### ✅ **Backend:**
- `app.py` - Rota `/api/category-assets` e funções auxiliares adicionadas

### ✅ **Testes:**
- `test_category_assets.py` - Script de teste automatizado

### ✅ **Exemplos:**
- `category_assets_example.js` - Exemplos de uso em JavaScript

### ✅ **Documentação:**
- `CATEGORY_ASSETS_GUIDE.md` - Este guia completo

---

## ✅ **Status da Implementação**

- ✅ **Rota `/api/category-assets`** implementada
- ✅ **Validação completa** de parâmetros
- ✅ **Integração com TradingView** para busca em tempo real
- ✅ **Filtros inteligentes** por categoria
- ✅ **Fallback para símbolos populares**
- ✅ **Ordenação por relevância**
- ✅ **Suporte a busca por termo**
- ✅ **Documentação completa**
- ✅ **Exemplos de uso** em Python e JavaScript
- ✅ **Testes automatizados** criados

**API de Category Assets pronta para uso!** 🚀📊

---

## 🎯 **Próximos Passos Sugeridos**

1. **✅ Testar a API** com diferentes categorias e exchanges
2. **✅ Integrar em aplicações** usando os exemplos fornecidos
3. **✅ Criar dashboard** web interativo
4. **✅ Implementar cache** para melhorar performance
5. **✅ Adicionar filtros** por tipo de ativo
6. **✅ Implementar monitoramento** de novos ativos

**A API de Category Assets está completa e funcionando!** 🎉📈
