# 🚀 API Current Candle - Guia Completo

## 🎯 Nova Rota Criada!

**`GET /api/current-candle`** - Obter apenas o candle atual de forma simplificada

---

## ⚡ Teste Imediato

### 1. **Inicie o Servidor**
```bash
cd tradingview-scraper/webapp
python app.py
```

### 2. **Teste Básico com cURL**
```bash
# Bitcoin 1 minuto
curl "http://localhost:5000/api/current-candle?symbol=BINANCE:BTCUSDT&timeframe=1m"

# Ethereum 5 minutos
curl "http://localhost:5000/api/current-candle?symbol=BINANCE:ETHUSDT&timeframe=5m"

# Bitcoin 1 hora
curl "http://localhost:5000/api/current-candle?symbol=BINANCE:BTCUSDT&timeframe=1h"
```

### 3. **Teste no Navegador**
```
http://localhost:5000/api/current-candle?symbol=BINANCE:BTCUSDT&timeframe=1m
```

---

## 📊 Exemplo de Resposta

```json
{
  "symbol": "BINANCE:BTCUSDT",
  "timeframe": "1m",
  "timestamp": 1705312800,
  "datetime": "2024-01-15T10:00:00",
  "open": 42500.0,
  "high": 42800.0,
  "low": 42300.0,
  "close": 42650.0,
  "volume": 1234.5678,
  "price_change": 150.0,
  "price_change_percent": 0.3529,
  "is_positive": true,
  "generated_at": "2024-01-15T10:30:00.123456",
  "timezone": "UTC"
}
```

---

## 🧪 Teste Automatizado

### **Execute o script de teste:**
```bash
cd tradingview-scraper/webapp
python test_current_candle.py
```

**Resultado esperado:**
```
🚀 Testando API de Current Candle
==================================================
✅ Servidor está rodando

📊 Testando Current Candle...

🧪 Teste 1: Bitcoin 1 minuto
⏱️  Tempo: 2.34s
📊 Status: 200
✅ Sucesso!
   📈 Símbolo: BINANCE:BTCUSDT
   ⏰ Timeframe: 1m
   💰 Preço: $42,650.00
   📊 Abertura: $42,500.00
   🔺 Máxima: $42,800.00
   🔻 Mínima: $42,300.00
   📦 Volume: 1,234.57
   💹 Mudança: +$150.00 (+0.35%)
   🎯 Status: 🟢 Positivo
   🕐 Timestamp: 2024-01-15T10:00:00

🎉 Testes concluídos!
```

---

## 🔧 Parâmetros da API

| Parâmetro | Obrigatório | Padrão | Descrição |
|-----------|-------------|--------|-----------|
| `symbol` | ✅ | - | EXCHANGE:SYMBOL (ex: BINANCE:BTCUSDT) |
| `timeframe` | ❌ | 1m | 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1M |

---

## 📈 Exemplos de Uso

### **Python:**
```python
import requests

# Obter candle atual do Bitcoin
response = requests.get('http://localhost:5000/api/current-candle', params={
    'symbol': 'BINANCE:BTCUSDT',
    'timeframe': '1m'
})

data = response.json()
print(f"Preço atual: ${data['close']}")
print(f"Mudança: {data['price_change_percent']:+.2f}%")
```

### **JavaScript:**
```javascript
// Função para obter candle atual
async function getCurrentCandle(symbol, timeframe) {
    const response = await fetch(`http://localhost:5000/api/current-candle?symbol=${symbol}&timeframe=${timeframe}`);
    return await response.json();
}

// Uso
getCurrentCandle('BINANCE:BTCUSDT', '1m')
    .then(candle => {
        console.log(`Preço: $${candle.close}`);
        console.log(`Mudança: ${candle.price_change_percent}%`);
    });
```

### **PHP:**
```php
$response = file_get_contents('http://localhost:5000/api/current-candle?symbol=BINANCE:BTCUSDT&timeframe=1m');
$data = json_decode($response, true);
echo "Preço atual: $" . $data['close'];
echo "Mudança: " . $data['price_change_percent'] . "%";
```

---

## 🎯 Casos de Uso Práticos

### **1. Dashboard de Preços**
```javascript
// Atualizar preço a cada 5 segundos
setInterval(async () => {
    try {
        const candle = await getCurrentCandle('BINANCE:BTCUSDT', '1m');
        document.getElementById('price').textContent = `$${candle.close}`;
        document.getElementById('change').textContent = `${candle.price_change_percent}%`;
        document.getElementById('change').className = candle.is_positive ? 'positive' : 'negative';
    } catch (error) {
        console.error('Erro ao atualizar preço:', error);
    }
}, 5000);
```

### **2. Alertas de Preço**
```python
import time

def monitor_price(symbol, target_price, timeframe='1m'):
    while True:
        try:
            response = requests.get('http://localhost:5000/api/current-candle', params={
                'symbol': symbol,
                'timeframe': timeframe
            })
            data = response.json()
            
            current_price = data['close']
            if current_price >= target_price:
                print(f"🚨 ALERTA: {symbol} atingiu ${current_price}!")
                break
                
            print(f"💰 {symbol}: ${current_price} (objetivo: ${target_price})")
            time.sleep(30)  # Verificar a cada 30 segundos
            
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(10)

# Monitorar Bitcoin
monitor_price('BINANCE:BTCUSDT', 50000)
```

### **3. Comparação de Símbolos**
```javascript
async function compareSymbols() {
    const symbols = ['BINANCE:BTCUSDT', 'BINANCE:ETHUSDT', 'BINANCE:ADAUSDT'];
    const results = [];
    
    for (const symbol of symbols) {
        try {
            const candle = await getCurrentCandle(symbol, '1h');
            results.push({
                symbol: symbol,
                price: candle.close,
                change: candle.price_change_percent,
                isPositive: candle.is_positive
            });
        } catch (error) {
            console.error(`Erro ao obter ${symbol}:`, error);
        }
    }
    
    // Ordenar por mudança percentual
    results.sort((a, b) => b.change - a.change);
    
    console.log('📊 Ranking de Performance:');
    results.forEach((item, index) => {
        const icon = item.isPositive ? '🟢' : '🔴';
        console.log(`${index + 1}. ${icon} ${item.symbol}: ${item.change.toFixed(2)}%`);
    });
}
```

### **4. Trading Bot Simples**
```python
def simple_trading_bot(symbol, timeframe='1m'):
    while True:
        try:
            response = requests.get('http://localhost:5000/api/current-candle', params={
                'symbol': symbol,
                'timeframe': timeframe
            })
            data = response.json()
            
            price = data['close']
            change_percent = data['price_change_percent']
            
            # Estratégia simples: comprar se subiu mais de 1%
            if change_percent > 1.0:
                print(f"🟢 SINAL DE COMPRA: {symbol} subiu {change_percent:.2f}%")
            # Vender se desceu mais de 1%
            elif change_percent < -1.0:
                print(f"🔴 SINAL DE VENDA: {symbol} desceu {change_percent:.2f}%")
            else:
                print(f"⚪ AGUARDAR: {symbol} mudança {change_percent:+.2f}%")
                
            time.sleep(60)  # Verificar a cada minuto
            
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(10)

# Executar bot
simple_trading_bot('BINANCE:BTCUSDT')
```

---

## 🚨 Casos de Erro

### **Sem símbolo:**
```bash
curl "http://localhost:5000/api/current-candle"
# Retorna: {"error": "Parâmetro 'symbol' é obrigatório"}
```

### **Símbolo inválido:**
```bash
curl "http://localhost:5000/api/current-candle?symbol=BTCUSDT"
# Retorna: {"error": "Formato de símbolo inválido"}
```

### **Timeframe inválido:**
```bash
curl "http://localhost:5000/api/current-candle?symbol=BINANCE:BTCUSDT&timeframe=2h"
# Retorna: {"error": "Timeframe inválido"}
```

### **Símbolo não encontrado:**
```bash
curl "http://localhost:5000/api/current-candle?symbol=BINANCE:INVALID"
# Retorna: {"error": "Não foi possível obter o candle atual"}
```

---

## 🔄 Diferenças entre as APIs

| Recurso | `/api/candles` | `/api/current-candle` |
|---------|----------------|----------------------|
| **Dados históricos** | ✅ Sim | ❌ Não |
| **Candle atual** | ✅ Sim | ✅ Sim |
| **Performance** | 🐌 Mais lento | ⚡ Mais rápido |
| **Uso** | Análise completa | Preço atual |
| **Tamanho resposta** | 📦 Grande | 📦 Pequeno |

---

## 📚 Arquivos Relacionados

- ✅ `app.py` - Endpoint `/api/current-candle` adicionado
- ✅ `test_current_candle.py` - Script de teste automatizado
- ✅ `current_candle_example.js` - Exemplos de uso em JavaScript
- ✅ `CURRENT_CANDLE_GUIDE.md` - Este guia

---

## ✅ Status

- ✅ **Endpoint criado:** `/api/current-candle`
- ✅ **Validação de parâmetros**
- ✅ **Tratamento de erros**
- ✅ **Timeout de 10 segundos**
- ✅ **Cálculo de mudança de preço**
- ✅ **Formato JSON otimizado**
- ✅ **Documentação completa**
- ✅ **Scripts de teste**

**API Current Candle pronta para uso!** 🚀📊

---

## 🎯 Próximos Passos

1. **Teste a API** com os exemplos acima
2. **Integre em sua aplicação** usando os códigos de exemplo
3. **Monitore performance** com diferentes timeframes
4. **Implemente alertas** baseados nos dados
5. **Crie dashboards** em tempo real

**A API está otimizada para obter o candle atual de forma rápida e eficiente!** ⚡🎉

