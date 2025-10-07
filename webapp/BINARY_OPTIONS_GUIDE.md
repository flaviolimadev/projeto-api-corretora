# 📈 Guia de Opções Binárias - Simulador

## 🎯 O que foi implementado

Sistema completo de simulação de opções binárias estilo IQ Option com:

### ✨ Funcionalidades

1. **Painel de Trading Completo**
   - Saldo inicial: $10,000 (virtual)
   - Seleção de valor de investimento ($10, $50, $100, $500 ou customizado)
   - Tempo de expiração (1 min, 3 min, 5 min, 15 min)
   - Botões CALL (Compra) e PUT (Venda)

2. **Operações em Tempo Real**
   - ✅ CALL: Aposta que o preço vai SUBIR
   - ✅ PUT: Aposta que o preço vai DESCER
   - ✅ Retorno de 85% em caso de vitória

3. **Animações e Interações**
   - 🎨 Notificações animadas ao abrir operação
   - ⏱️ Timer com contagem regressiva em tempo real
   - 📊 P&L (Lucro/Perda) atualizado ao vivo
   - 🎉 Notificação de resultado (Ganhou/Perdeu) com animação

4. **Painel de Operações Ativas**
   - Mostra todas as operações em andamento
   - Timer de expiração
   - Preço de entrada vs Preço atual
   - P&L em percentual
   - Cores verde/vermelho para lucro/prejuízo

5. **Histórico de Operações**
   - Últimas 20 operações realizadas
   - Resultado de cada operação
   - Horário de fechamento
   - Lucro/Prejuízo total

## 🚀 Como Usar

### 1. Inicie a Aplicação
```bash
cd tradingview-scraper/webapp
python app.py
```

### 2. Abra o Navegador
Acesse: `http://localhost:5000`

### 3. Inicie o Stream
1. Digite um símbolo (ex: `BINANCE:BTCUSDT`)
2. Selecione o timeframe
3. Clique em "Iniciar Stream"

### 4. Configure sua Operação
1. **Escolha o valor:** Clique em $10, $50, $100, $500 ou digite um valor customizado
2. **Escolha o tempo:** 1 min, 3 min, 5 min ou 15 min

### 5. Execute a Operação
- **CALL (📈):** Clique se acha que o preço vai SUBIR
- **PUT (📉):** Clique se acha que o preço vai DESCER

### 6. Acompanhe
- Veja sua operação no painel "Operações Ativas"
- Acompanhe o timer e o P&L em tempo real
- Aguarde a expiração

### 7. Resultado
- ✅ **GANHOU:** Recebe o valor investido + 85% de lucro
- ❌ **PERDEU:** Perde o valor investido

## 📊 Exemplo Prático

### Cenário 1: CALL Vencedor ✅
```
1. Preço atual: $100,000
2. Você clica em CALL apostando $50
3. Expira em 1 minuto
4. Preço após 1 min: $100,500
5. GANHOU! Lucro: $42.50 (85% de $50)
6. Novo saldo: $10,042.50
```

### Cenário 2: PUT Perdedor ❌
```
1. Preço atual: $100,000
2. Você clica em PUT apostando $100
3. Expira em 1 minuto
4. Preço após 1 min: $100,300 (subiu)
5. PERDEU! Perda: $100
6. Novo saldo: $9,900
```

## 🎮 Estratégias

### Para Iniciantes:
- Comece com valores pequenos ($10-$50)
- Use expirações curtas (1-3 min) para aprender
- Observe as tendências do gráfico

### Para Avançados:
- Combine com análise técnica
- Use timeframes maiores para tendências mais claras
- Gerencie seu risco (não invista mais de 5% do saldo por operação)

## ⚡ Recursos Visuais

### Cores e Indicadores:
- **Verde (📈):** CALL / Lucro / Vitória
- **Vermelho (📉):** PUT / Perda / Derrota
- **Azul:** Timer / Informações
- **Amarelo:** Alertas

### Notificações:
- 🎯 Abertura de operação (2 segundos)
- 🎉 Vitória (3 segundos com emoji feliz)
- 😢 Derrota (3 segundos com emoji triste)

## 📈 Estatísticas

O sistema rastreia automaticamente:
- Saldo atual
- Número de operações ativas
- Histórico de operações
- Win rate (taxa de vitória)
- P&L total

## ⚠️ Importante

- Este é um **SIMULADOR** com dinheiro virtual
- Os preços são reais do TradingView
- Perfeito para praticar estratégias sem risco
- Não use dinheiro real sem entender os riscos

## 🔧 Personalização

Você pode ajustar no código:
- Taxa de retorno (padrão: 85%)
- Saldo inicial (padrão: $10,000)
- Valores de investimento
- Tempos de expiração

## 🎯 Próximas Melhorias Possíveis

- [ ] Marcadores visuais no gráfico mostrando entrada
- [ ] Linha horizontal no preço de entrada
- [ ] Som ao abrir/fechar operação
- [ ] Gráfico de performance
- [ ] Ranking de melhores operações
- [ ] Replay de operações
- [ ] Indicadores técnicos integrados

---

**Divirta-se e bons trades! 📊🚀**


