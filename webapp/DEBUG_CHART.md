# 🔧 Debug do Gráfico - Guia Detalhado

## 🎯 Problema Atual
Os logs mostram que a comunicação está funcionando, mas o gráfico não exibe dados.

## 🔍 Teste Passo a Passo

### 1. **Reinicie o Servidor**
```bash
cd tradingview-scraper/webapp
python app.py
```

### 2. **Abra o Console do Navegador**
```
1. Pressione F12
2. Vá para a aba "Console"
3. Limpe o console (Ctrl+L)
```

### 3. **Teste Básico**
```
1. Acesse: http://localhost:5000
2. Aguarde 2 segundos
3. Verifique se aparece: "🧪 Testando gráfico..."
```

### 4. **Se o Teste do Gráfico Funcionar**
Você deve ver:
```javascript
🧪 Testando gráfico...
✅ Gráfico e série encontrados
📊 Adicionando dados de teste...
✅ Dados de teste adicionados com sucesso!
```

**Se isso funcionar**, o problema está na comunicação de dados.

### 5. **Se o Teste do Gráfico NÃO Funcionar**
Você verá:
```javascript
🧪 Testando gráfico...
❌ Gráfico não encontrado
```
ou
```javascript
❌ Série de candlesticks não encontrada
```

**Se isso não funcionar**, o problema está na inicialização do gráfico.

## 🚨 Diagnóstico por Logs

### Cenário 1: Gráfico OK, Dados Não Chegam
**Logs esperados:**
```javascript
🧪 Testando gráfico...
✅ Gráfico e série encontrados
✅ Dados de teste adicionados com sucesso!
🔄 Mudando timeframe de 1m para 5m
🔌 Parando stream atual...
✅ Stream started: {symbol: 'BINANCE:BTCUSDT', timeframe: '5m'}
📈 Ready to receive data for BINANCE:BTCUSDT (5m)
// MAS NÃO APARECE: 📊 Price update #1
```

**Solução:** Problema no backend - não está enviando dados.

### Cenário 2: Gráfico Quebrado
**Logs esperados:**
```javascript
🧪 Testando gráfico...
❌ Gráfico não encontrado
```

**Solução:** Problema na inicialização do gráfico.

### Cenário 3: Dados Chegam, Gráfico Não Atualiza
**Logs esperados:**
```javascript
📊 Price update #1: {...}
🕯️ Processing candle: {...}
📦 Added to batch, total: 1
// MAS NÃO APARECE: ✅ Loaded 1000 historical candles
```

**Solução:** Problema na lógica de exibição.

## 🔧 Soluções por Problema

### Problema 1: Backend Não Envia Dados
**Verificar no terminal do servidor:**
```bash
# Deve aparecer:
Starting stream for BINANCE:BTCUSDT (5m) - SID: ...
Sending 1000 historical candles for BINANCE:BTCUSDT (5m)
Sent 1/1000 candles
Sent 101/1000 candles
...
```

**Se não aparecer:**
1. Verifique se o símbolo está correto
2. Tente outro símbolo: BINANCE:ETHUSDT
3. Verifique se há erros no terminal

### Problema 2: Gráfico Não Inicializa
**Solução:**
1. Recarregue a página (Ctrl+F5)
2. Verifique se há erros no console
3. Verifique se o Lightweight Charts carregou

### Problema 3: Dados Chegam Mas Não Exibem
**Solução:**
1. Verifique se `candlestickSeries` existe
2. Verifique se `chart` existe
3. Verifique se há erros ao chamar `setData()`

## 🧪 Teste Manual no Console

### Teste 1: Verificar Gráfico
```javascript
// No console do navegador:
console.log('Chart:', chart);
console.log('CandlestickSeries:', candlestickSeries);
```

### Teste 2: Adicionar Dados Manualmente
```javascript
// No console do navegador:
const testData = [
    { time: 1640995200, open: 47000, high: 48000, low: 46000, close: 47500 },
    { time: 1640995260, open: 47500, high: 48500, low: 47000, close: 48000 }
];
candlestickSeries.setData(testData);
```

### Teste 3: Verificar Dados Recebidos
```javascript
// No console do navegador:
console.log('CandleData length:', candleData.length);
console.log('PriceUpdateCount:', priceUpdateCount);
console.log('IsHistoricalDataLoaded:', isHistoricalDataLoaded);
```

## 📊 Logs Esperados do Backend

No terminal do servidor Python, você deve ver:
```bash
Starting stream for BINANCE:BTCUSDT (5m) - SID: abc123
Sending 1000 historical candles for BINANCE:BTCUSDT (5m)
Sent 1/1000 candles
Sent 101/1000 candles
Sent 201/1000 candles
...
Sent 1001/1000 candles
```

## 🎯 Próximos Passos

**Me informe:**

1. **O teste do gráfico funcionou?**
   ```
   [Sim/Não] - Cole os logs do teste
   ```

2. **O backend está enviando dados?**
   ```
   [Sim/Não] - Cole os logs do terminal do servidor
   ```

3. **Os dados chegam no frontend?**
   ```
   [Sim/Não] - Cole os logs do console do navegador
   ```

4. **Há erros no console?**
   ```
   [Sim/Não] - Cole os erros em vermelho
   ```

## 🔄 Teste Rápido

1. **Reinicie tudo:**
   ```bash
   # Terminal 1: Servidor
   cd tradingview-scraper/webapp
   python app.py
   
   # Terminal 2: Navegador
   # Abra http://localhost:5000
   # Pressione F12
   ```

2. **Aguarde 2 segundos e verifique:**
   - Aparece "🧪 Testando gráfico..."?
   - O teste passou ou falhou?

3. **Inicie o stream:**
   - Digite: BINANCE:BTCUSDT
   - Clique: "Iniciar Stream"
   - Aguarde: "Streaming em Tempo Real"

4. **Mude o timeframe:**
   - Clique: "5m"
   - Observe os logs

**Cole aqui todos os logs que aparecerem!** 📝

