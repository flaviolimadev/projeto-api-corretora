# 🎨 Funcionalidades Visuais - Marcadores e Animações

## 📊 Marcadores no Gráfico

### 1. **Marcador de Entrada da Operação**
Quando você abre uma operação (CALL ou PUT), o sistema adiciona:

#### Seta de Entrada:
- **CALL (Compra):** ➡️ Seta VERDE para CIMA abaixo da vela
- **PUT (Venda):** ➡️ Seta VERMELHA para BAIXO acima da vela
- **Texto:** Mostra o tipo e preço de entrada

### 2. **Linha Horizontal de Preço**
Uma linha tracejada horizontal no preço de entrada:

#### Características:
- **Cor Inicial:** Verde (CALL) ou Vermelho (PUT)
- **Cor Dinâmica:** Muda conforme o resultado:
  - ✅ **Verde** = Está em LUCRO
  - ❌ **Vermelho** = Está em PERDA
- **Texto na Linha:** 
  - "CALL $50 ✓ GANHO" (quando ganhando)
  - "PUT $100 ✗ PERDA" (quando perdendo)

### 3. **Marcador de Expiração**
Um círculo dourado ⏰ mostrando onde a operação vai expirar:

#### Características:
- **Cor:** Dourado (#ffd700)
- **Posição:** Na vela de expiração
- **Texto:** "⏰ Expira"
- **Função:** Mostra visualmente quando a operação vai fechar

### 4. **Marcador de Fechamento**
Quando a operação expira, adiciona um marcador final:

#### Características:
- **Cor:** Verde (vitória) ou Vermelho (derrota)
- **Texto:** 
  - "✓ WIN $42.50" (vitória)
  - "✗ LOSS $100.00" (derrota)

## ✨ Animações e Efeitos

### 1. **Card de Operação Ativa**

#### Estados Visuais:
```
🟢 EM LUCRO:
- Borda esquerda verde (4px)
- Sombra verde pulsante
- Texto "🚀 EM LUCRO" em verde
- P&L com ✓ verde

🔴 EM PERDA:
- Borda esquerda vermelha (4px)
- Sombra vermelha pulsante
- Texto "⚠️ EM PERDA" em vermelho
- P&L com ✗ vermelho
```

### 2. **Timer com Pulsação**
Quando faltam menos de 10 segundos:
- Timer fica vermelho
- Pulsa e aumenta de tamanho
- Animação urgente chamando atenção

### 3. **Valores P&L Animados**
- Porcentagem de lucro/perda pulsa
- Cores dinâmicas (verde/vermelho)
- Símbolos ✓ ou ✗ indicam resultado

### 4. **Barra de Status**
No fundo de cada card ativo:
```css
🚀 EM LUCRO    (fundo verde com gradiente)
⚠️ EM PERDA    (fundo vermelho com gradiente)
```

## 🎬 Sequência Visual Completa

### Abertura de Operação:
```
1. Clica CALL/PUT
2. ✨ Notificação slide-in
3. 📍 Seta aparece no gráfico
4. ➖ Linha horizontal tracejada
5. ⏰ Marcador de expiração
6. 📋 Card aparece com animação
```

### Durante a Operação:
```
1. 🔄 Linha muda de cor (verde/vermelho)
2. 💫 Card pulsa (verde/vermelho)
3. ⏱️ Timer conta regressivo
4. 📊 P&L atualiza em tempo real
5. ✓/✗ Indicadores piscam
```

### Fechamento:
```
1. ⏰ Timer chega a 00:00
2. 🎯 Marca final no gráfico
3. ➖ Linha desaparece
4. 🎉/😢 Notificação de resultado
5. 📝 Vai para o histórico
6. 💰 Saldo atualiza com animação
```

## 🎨 Cores e Significados

### Verde (#26a69a):
- ✅ CALL (Compra)
- ✅ Operação em lucro
- ✅ Vitória
- ✅ Saldo positivo

### Vermelho (#ef5350):
- ❌ PUT (Venda)
- ❌ Operação em perda
- ❌ Derrota
- ❌ Saldo negativo

### Dourado (#ffd700):
- ⏰ Marcador de expiração
- ⏱️ Timer importante

### Azul (#2962ff):
- ℹ️ Informações
- 🔵 Timer normal

## 📱 Exemplos Visuais

### CALL em Lucro:
```
Gráfico:
  ➡️ Seta verde para cima ↑
  ━━━━━━ Linha verde tracejada ━━━━━━
  ⏰ Círculo dourado no final

Card:
  ┌──────────────────────────┐
  │ 📈 CALL      ⏱️ 0:45    │ (borda verde)
  │ Entrada: $100,000        │
  │ Atual: $100,250  🟢      │
  │ P&L: ✓ +0.25%           │
  │ ┌──────────────────────┐│
  │ │  🚀 EM LUCRO         ││ (fundo verde)
  │ └──────────────────────┘│
  └──────────────────────────┘
```

### PUT em Perda:
```
Gráfico:
  ➡️ Seta vermelha para baixo ↓
  ━━━━━━ Linha vermelha tracejada ━━━━━━
  ⏰ Círculo dourado no final

Card:
  ┌──────────────────────────┐
  │ 📉 PUT       ⏱️ 1:30    │ (borda vermelha)
  │ Entrada: $100,000        │
  │ Atual: $100,150  🔴      │
  │ P&L: ✗ -0.15%           │
  │ ┌──────────────────────┐│
  │ │  ⚠️ EM PERDA          ││ (fundo vermelho)
  │ └──────────────────────┘│
  └──────────────────────────┘
```

## 🔧 Configurações de Animação

### Velocidades:
- **Slide In:** 0.3s
- **Fade Out:** 0.3s
- **Pulse:** 2s (loop infinito)
- **Urgent Pulse:** 1s (loop infinito)
- **Text Pulse:** 1.5s (loop infinito)

### Efeitos:
- **Box Shadow:** Sombra pulsante ao redor do card
- **Transform Scale:** Timer urgente aumenta 10%
- **Opacity:** Textos pulsam entre 100% e 70%

## 📊 Linha do Tempo Visual

```
T=0s    → Abertura (seta + linha)
T=5s    → Primeira atualização P&L
T=10s   → Atualizações contínuas
T=50s   → Timer fica urgente (vermelho pulsante)
T=60s   → Expiração (marcador final)
T=60.1s → Resultado (notificação)
```

## 🎯 Dicas de UX

1. **Múltiplas Operações:** Cada uma tem sua própria cor e marcadores
2. **Limpeza Visual:** Linhas são removidas ao expirar
3. **Feedback Imediato:** Cores mudam em tempo real
4. **Atenção:** Animações urgentes nos últimos 10 segundos
5. **Histórico:** Marcadores de fechamento ficam visíveis no gráfico

---

**Tudo atualiza em TEMPO REAL conforme o preço se move! 🚀📈📉**


