# 🔧 Debug do Timeframe - Guia de Teste

## 🎯 Problema Atual
O timeframe muda no display mas o gráfico não atualiza com novos dados.

## 🔍 Como Testar

### 1. **Abra o Console do Navegador**
```
1. Pressione F12
2. Vá para a aba "Console"
3. Mantenha aberto durante o teste
```

### 2. **Teste Básico**
```
1. Acesse: http://localhost:5000
2. Digite: BINANCE:BTCUSDT
3. Clique: "Iniciar Stream"
4. Aguarde: Status "Streaming em Tempo Real"
5. Clique: Botão "15m" na toolbar do gráfico
```

### 3. **Verifique os Logs no Console**
Você deve ver esta sequência:

```javascript
// Ao clicar em 15m:
🔄 Mudando timeframe de 1m para 15m
🔌 Parando stream atual...
✅ Stream started: {symbol: "BINANCE:BTCUSDT", timeframe: "15m"}
📈 Ready to receive data for BINANCE:BTCUSDT (15m)
📊 Price update #1: {timestamp: ..., open: ..., close: ...}
📊 Price update #2: {timestamp: ..., open: ..., close: ...}
...
✅ Loaded 1000 historical candles for 15m
```

## 🚨 Se NÃO Funcionar

### Problema 1: Não aparece logs
**Causa:** JavaScript não está carregando
**Solução:** 
1. Recarregue a página (Ctrl+F5)
2. Verifique se não há erros no console

### Problema 2: Logs aparecem mas gráfico não muda
**Causa:** Dados não estão chegando do backend
**Solução:**
1. Verifique se o servidor está rodando
2. Pare e reinicie o servidor:
   ```bash
   cd tradingview-scraper/webapp
   python app.py
   ```

### Problema 3: "Stream started" mas sem "Price update"
**Causa:** Backend não está enviando dados
**Solução:**
1. Verifique se o símbolo está correto
2. Tente outro símbolo: BINANCE:ETHUSDT
3. Verifique logs do servidor Python

### Problema 4: Dados chegam mas gráfico não atualiza
**Causa:** Problema na renderização do gráfico
**Solução:**
1. Verifique se há erros no console
2. Tente recarregar a página
3. Teste com o arquivo de teste: `TEST_TIMEFRAME.html`

## 🧪 Teste Alternativo

### Use o arquivo de teste simples:
```
1. Acesse: http://localhost:5000/TEST_TIMEFRAME.html
2. Clique: "Iniciar Stream"
3. Clique: Botões de timeframe
4. Veja os logs em tempo real
```

Este arquivo testa apenas a comunicação sem o gráfico complexo.

## 📊 O Que Deve Acontecer

### Sequência Correta:
1. ✅ **Clique em timeframe** → Log: "Mudando timeframe..."
2. ✅ **Stream para** → Log: "Parando stream atual..."
3. ✅ **Stream inicia** → Log: "Stream started: {timeframe: '15m'}"
4. ✅ **Dados chegam** → Log: "Price update #1, #2, #3..."
5. ✅ **Gráfico atualiza** → Log: "Loaded 1000 historical candles"
6. ✅ **Status muda** → "Streaming em Tempo Real"

### Sinais de Sucesso:
- ✅ Botão do timeframe fica **azul brilhante**
- ✅ Status muda para **"Reconectando..."** depois **"Streaming em Tempo Real"**
- ✅ Gráfico mostra candles do novo timeframe
- ✅ Console mostra logs de dados chegando

## 🔧 Se Ainda Não Funcionar

### Debug Avançado:

1. **Verifique o Network Tab:**
   ```
   F12 → Network → WS (WebSocket)
   Deve mostrar conexão ativa
   ```

2. **Verifique o Backend:**
   ```bash
   # No terminal do servidor, deve aparecer:
   Starting stream for BINANCE:BTCUSDT (15m) - SID: ...
   Sending 1000 historical candles
   ```

3. **Teste Manual:**
   ```javascript
   // No console do navegador:
   socket.emit('start_stream', {symbol: 'BINANCE:BTCUSDT', timeframe: '15m'});
   ```

## 📝 Relatório de Teste

Por favor, me informe:

1. **Logs que aparecem no console:**
   ```
   [Cole aqui os logs que aparecem]
   ```

2. **O que acontece visualmente:**
   ```
   [Descreva o que vê na tela]
   ```

3. **Erros no console:**
   ```
   [Cole aqui qualquer erro em vermelho]
   ```

4. **Status do servidor:**
   ```
   [Descreva se o servidor está rodando sem erros]
   ```

## 🎯 Resultado Esperado

Após a correção, ao clicar em um novo timeframe:

1. ✅ **Imediatamente:** Botão fica azul, status "Reconectando..."
2. ✅ **1-2 segundos:** Status "Carregando dados históricos..."
3. ✅ **5-10 segundos:** Status "Streaming em Tempo Real"
4. ✅ **Gráfico:** Mostra candles do novo timeframe
5. ✅ **Console:** Logs de dados chegando

**Teste agora e me diga o que acontece!** 🚀

