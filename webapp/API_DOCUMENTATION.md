# 📊 API de Candles - Documentação

## 🎯 Visão Geral

API REST para obter dados de candles históricos e atuais de ativos financeiros em formato JSON.

**Base URL:** `http://localhost:5000/api`

---

## 🔗 Endpoints

### 1. **GET /api/candles** - Obter Candles

Obtém dados de candles históricos e o candle atual de um ativo.

#### **Parâmetros da Query:**

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `symbol` | string | ✅ | - | Símbolo no formato `EXCHANGE:SYMBOL` |
| `timeframe` | string | ❌ | `1m` | Timeframe dos candles |
| `limit` | integer | ❌ | `1000` | Número de candles (máx: 1000) |

#### **Timeframes Suportados:**
- `1m` - 1 minuto
- `5m` - 5 minutos  
- `15m` - 15 minutos
- `30m` - 30 minutos
- `1h` - 1 hora
- `2h` - 2 horas
- `4h` - 4 horas
- `1d` - 1 dia
- `1w` - 1 semana
- `1M` - 1 mês

#### **Exemplos de Uso:**

```bash
# Bitcoin 1 hora - últimos 500 candles
GET /api/candles?symbol=BINANCE:BTCUSDT&timeframe=1h&limit=500

# Ethereum 15 minutos - últimos 100 candles
GET /api/candles?symbol=BINANCE:ETHUSDT&timeframe=15m&limit=100

# Apple 1 dia - últimos 1000 candles
GET /api/candles?symbol=NASDAQ:AAPL&timeframe=1d&limit=1000
```

---

## 📋 Formato da Resposta

### **Estrutura da Resposta:**

```json
{
  "symbol": "BINANCE:BTCUSDT",
  "timeframe": "1h",
  "total_candles": 500,
  "current_candle": {
    "timestamp": 1640995200,
    "datetime": "2022-01-01T00:00:00",
    "open": 47000.0,
    "high": 48000.0,
    "low": 46000.0,
    "close": 47500.0,
    "volume": 1234.56,
    "is_current": true
  },
  "historical_candles": [
    {
      "timestamp": 1640991600,
      "datetime": "2021-12-31T23:00:00",
      "open": 46500.0,
      "high": 47500.0,
      "low": 46000.0,
      "close": 47000.0,
      "volume": 987.65
    }
  ],
  "generated_at": "2024-01-15T10:30:00.123456",
  "timezone": "UTC"
}
```

### **Campos da Resposta:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `symbol` | string | Símbolo solicitado |
| `timeframe` | string | Timeframe solicitado |
| `total_candles` | integer | Número de candles históricos |
| `current_candle` | object | Candle atual (pode ser null) |
| `historical_candles` | array | Array de candles históricos |
| `generated_at` | string | Timestamp de geração da resposta |
| `timezone` | string | Timezone dos dados (sempre UTC) |

### **Campos do Candle:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `timestamp` | integer | Timestamp Unix |
| `datetime` | string | Data/hora em formato ISO |
| `open` | float | Preço de abertura |
| `high` | float | Preço máximo |
| `low` | float | Preço mínimo |
| `close` | float | Preço de fechamento |
| `volume` | float | Volume negociado |
| `is_current` | boolean | Se é o candle atual (apenas no current_candle) |

---

## 🚨 Códigos de Erro

### **400 Bad Request**
```json
{
  "error": "Parâmetro 'symbol' é obrigatório",
  "example": "/api/candles?symbol=BINANCE:BTCUSDT&timeframe=1h"
}
```

### **400 Bad Request - Símbolo Inválido**
```json
{
  "error": "Formato de símbolo inválido",
  "expected": "EXCHANGE:SYMBOL (ex: BINANCE:BTCUSDT)",
  "received": "BTCUSDT"
}
```

### **400 Bad Request - Timeframe Inválido**
```json
{
  "error": "Timeframe inválido",
  "valid_timeframes": ["1m", "5m", "15m", "30m", "1h", "2h", "4h", "1d", "1w", "1M"],
  "received": "2h"
}
```

### **500 Internal Server Error**
```json
{
  "error": "Erro interno do servidor",
  "details": "Mensagem de erro específica"
}
```

---

## 🧪 Exemplos de Uso

### **1. Python - requests**

```python
import requests
import json

# Obter dados do Bitcoin
response = requests.get('http://localhost:5000/api/candles', params={
    'symbol': 'BINANCE:BTCUSDT',
    'timeframe': '1h',
    'limit': 100
})

if response.status_code == 200:
    data = response.json()
    print(f"Total candles: {data['total_candles']}")
    print(f"Último preço: {data['current_candle']['close']}")
    
    # Processar candles históricos
    for candle in data['historical_candles']:
        print(f"{candle['datetime']}: {candle['close']}")
else:
    print(f"Erro: {response.json()}")
```

### **2. JavaScript - fetch**

```javascript
async function getCandles(symbol, timeframe, limit = 100) {
    try {
        const response = await fetch(
            `http://localhost:5000/api/candles?symbol=${symbol}&timeframe=${timeframe}&limit=${limit}`
        );
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        
        console.log(`Total candles: ${data.total_candles}`);
        console.log(`Current price: ${data.current_candle?.close}`);
        
        return data;
    } catch (error) {
        console.error('Erro:', error);
    }
}

// Uso
getCandles('BINANCE:BTCUSDT', '1h', 50);
```

### **3. cURL**

```bash
# Bitcoin 1 hora
curl "http://localhost:5000/api/candles?symbol=BINANCE:BTCUSDT&timeframe=1h&limit=100"

# Ethereum 15 minutos
curl "http://localhost:5000/api/candles?symbol=BINANCE:ETHUSDT&timeframe=15m&limit=50"

# Apenas o último candle
curl "http://localhost:5000/api/candles?symbol=BINANCE:BTCUSDT&timeframe=1m&limit=1"
```

### **4. Postman**

```
Method: GET
URL: http://localhost:5000/api/candles
Query Params:
- symbol: BINANCE:BTCUSDT
- timeframe: 1h
- limit: 100
```

---

## 📊 Exemplos de Resposta

### **Resposta Completa (Bitcoin 1h):**

```json
{
  "symbol": "BINANCE:BTCUSDT",
  "timeframe": "1h",
  "total_candles": 100,
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
    },
    {
      "timestamp": 1705305600,
      "datetime": "2024-01-15T08:00:00",
      "open": 41800.0,
      "high": 42200.0,
      "low": 41500.0,
      "close": 42000.0,
      "volume": 876.5432
    }
  ],
  "generated_at": "2024-01-15T10:30:00.123456",
  "timezone": "UTC"
}
```

### **Resposta de Erro:**

```json
{
  "error": "Parâmetro 'symbol' é obrigatório",
  "example": "/api/candles?symbol=BINANCE:BTCUSDT&timeframe=1h"
}
```

---

## 🔧 Configuração

### **Iniciar o Servidor:**

```bash
cd tradingview-scraper/webapp
python app.py
```

### **Testar a API:**

```bash
# Teste básico
curl "http://localhost:5000/api/candles?symbol=BINANCE:BTCUSDT&timeframe=1h&limit=10"

# Teste de erro
curl "http://localhost:5000/api/candles"
```

---

## 📈 Casos de Uso

### **1. Análise Técnica**
- Obter dados históricos para calcular indicadores
- Backtesting de estratégias
- Análise de padrões de preço

### **2. Dashboards**
- Visualização de preços em tempo real
- Gráficos interativos
- Monitoramento de portfólio

### **3. Trading Bots**
- Alimentar algoritmos de trading
- Análise de sinais
- Execução automática

### **4. Pesquisa**
- Análise de mercado
- Estudos acadêmicos
- Desenvolvimento de modelos

---

## ⚡ Performance

- **Latência:** ~2-5 segundos por requisição
- **Throughput:** ~10-20 requisições por minuto
- **Limite:** Máximo 1000 candles por requisição
- **Cache:** Não implementado (dados sempre frescos)

---

## 🛡️ Limitações

1. **Rate Limiting:** Sem limite implementado (use com moderação)
2. **Símbolos:** Apenas símbolos suportados pelo TradingView
3. **Timeframes:** Apenas timeframes pré-definidos
4. **Histórico:** Máximo 1000 candles por requisição
5. **Tempo Real:** Dados podem ter delay de 1-2 minutos

---

## 🔄 Changelog

### **v1.0.0** (2024-01-15)
- ✅ Endpoint `/api/candles` implementado
- ✅ Suporte a múltiplos timeframes
- ✅ Dados históricos e atuais
- ✅ Validação de parâmetros
- ✅ Tratamento de erros
- ✅ Documentação completa

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs do servidor
2. Teste com cURL primeiro
3. Verifique se o símbolo existe no TradingView
4. Confirme se o servidor está rodando

**API pronta para uso!** 🚀📊

