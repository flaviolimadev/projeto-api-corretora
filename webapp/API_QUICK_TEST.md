# 🚀 Teste Rápido da API de Candles

## 🎯 API Criada com Sucesso!

Nova rota: **`GET /api/candles`** para obter dados de candles em formato JSON.

---

## ⚡ Teste Imediato

### 1. **Inicie o Servidor**
```bash
cd tradingview-scraper/webapp
python app.py
```

### 2. **Teste Básico com cURL**
```bash
# Bitcoin 1 hora - 10 candles
curl "http://localhost:5000/api/candles?symbol=BINANCE:BTCUSDT&timeframe=1h&limit=10"

# Ethereum 15 minutos - 50 candles  
curl "http://localhost:5000/api/candles?symbol=BINANCE:ETHUSDT&timeframe=15m&limit=50"

# Apenas o último candle
curl "http://localhost:5000/api/candles?symbol=BINANCE:BTCUSDT&timeframe=1m&limit=1"
```

### 3. **Teste no Navegador**
```
http://localhost:5000/api/candles?symbol=BINANCE:BTCUSDT&timeframe=1h&limit=10
```

---

## 📊 Exemplo de Resposta

```json
{
  "symbol": "BINANCE:BTCUSDT",
  "timeframe": "1h",
  "total_candles": 10,
  "current_candle": {
    "timestamp": 1705312800,
    "datetime": "2024-01-15T10:00:00",
    "open": 42500.0,
    "high": 42800.0,
    "low": 42300.0,
    "close": 42650.0,
    "volume": 1234.5678,
    "is_current": true
  },
  "historical_candles": [
    {
      "timestamp": 1705309200,
      "datetime": "2024-01-15T09:00:00",
      "open": 42000.0,
      "high": 42500.0,
      "low": 41800.0,
      "close": 42500.0,
      "volume": 987.6543
    }
  ],
  "generated_at": "2024-01-15T10:30:00.123456",
  "timezone": "UTC"
}
```

---

## 🧪 Teste Automatizado

### **Execute o script de teste:**
```bash
cd tradingview-scraper/webapp
python test_api.py
```

**Resultado esperado:**
```
🚀 Iniciando testes da API de Candles
==================================================
✅ Servidor está rodando

📊 Testes básicos...
🧪 Testando: BINANCE:BTCUSDT (1m) - 10 candles
⏱️  Tempo: 3.45s
📊 Status: 200
✅ Sucesso!
   - Total candles: 10
   - Current candle: Sim
   - Generated at: 2024-01-15T10:30:00.123456

🎉 Todos os testes passaram! API funcionando perfeitamente!
```

---

## 🔧 Parâmetros da API

| Parâmetro | Obrigatório | Padrão | Descrição |
|-----------|-------------|--------|-----------|
| `symbol` | ✅ | - | EXCHANGE:SYMBOL (ex: BINANCE:BTCUSDT) |
| `timeframe` | ❌ | 1m | 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1M |
| `limit` | ❌ | 1000 | Número de candles (máx: 1000) |

---

## 📈 Exemplos de Uso

### **Python:**
```python
import requests

response = requests.get('http://localhost:5000/api/candles', params={
    'symbol': 'BINANCE:BTCUSDT',
    'timeframe': '1h',
    'limit': 100
})

data = response.json()
print(f"Preço atual: ${data['current_candle']['close']}")
```

### **JavaScript:**
```javascript
fetch('http://localhost:5000/api/candles?symbol=BINANCE:BTCUSDT&timeframe=1h&limit=100')
  .then(response => response.json())
  .then(data => {
    console.log(`Preço atual: $${data.current_candle.close}`);
  });
```

### **PHP:**
```php
$response = file_get_contents('http://localhost:5000/api/candles?symbol=BINANCE:BTCUSDT&timeframe=1h&limit=100');
$data = json_decode($response, true);
echo "Preço atual: $" . $data['current_candle']['close'];
```

---

## 🚨 Casos de Erro

### **Sem símbolo:**
```bash
curl "http://localhost:5000/api/candles"
# Retorna: {"error": "Parâmetro 'symbol' é obrigatório"}
```

### **Símbolo inválido:**
```bash
curl "http://localhost:5000/api/candles?symbol=BTCUSDT"
# Retorna: {"error": "Formato de símbolo inválido"}
```

### **Timeframe inválido:**
```bash
curl "http://localhost:5000/api/candles?symbol=BINANCE:BTCUSDT&timeframe=2h"
# Retorna: {"error": "Timeframe inválido"}
```

---

## 🎯 Casos de Uso

### **1. Trading Bot:**
```python
# Obter dados para análise
data = requests.get('http://localhost:5000/api/candles', params={
    'symbol': 'BINANCE:BTCUSDT',
    'timeframe': '5m',
    'limit': 100
}).json()

# Calcular indicadores
prices = [c['close'] for c in data['historical_candles']]
sma_20 = sum(prices[-20:]) / 20
current_price = data['current_candle']['close']

# Lógica de trading
if current_price > sma_20:
    print("Sinal de COMPRA")
```

### **2. Dashboard:**
```javascript
// Atualizar preço a cada minuto
setInterval(async () => {
    const data = await fetch('/api/candles?symbol=BINANCE:BTCUSDT&timeframe=1m&limit=1').then(r => r.json());
    document.getElementById('price').textContent = `$${data.current_candle.close}`;
}, 60000);
```

### **3. Análise Técnica:**
```python
# Calcular RSI
def calculate_rsi(prices, period=14):
    gains = [max(0, prices[i] - prices[i-1]) for i in range(1, len(prices))]
    losses = [max(0, prices[i-1] - prices[i]) for i in range(1, len(prices))]
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Usar com dados da API
data = requests.get('http://localhost:5000/api/candles', params={
    'symbol': 'BINANCE:BTCUSDT',
    'timeframe': '1h',
    'limit': 50
}).json()

prices = [c['close'] for c in data['historical_candles']]
rsi = calculate_rsi(prices)
print(f"RSI: {rsi:.2f}")
```

---

## 📚 Documentação Completa

Para documentação detalhada, veja: `API_DOCUMENTATION.md`

---

## ✅ Status

- ✅ **Endpoint criado:** `/api/candles`
- ✅ **Validação de parâmetros**
- ✅ **Tratamento de erros**
- ✅ **Dados históricos + atuais**
- ✅ **Múltiplos timeframes**
- ✅ **Formato JSON padronizado**
- ✅ **Documentação completa**
- ✅ **Scripts de teste**

**API pronta para uso em qualquer aplicação!** 🚀📊

