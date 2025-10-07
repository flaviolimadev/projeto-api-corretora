# 🎯 Marcadores Visuais Estilo IQ Option

## ✨ O que foi implementado

Sistema completo de overlays visuais sobre o gráfico, exatamente como no IQ Option!

### 📊 Elementos Visuais:

#### 1. **Linha Horizontal Tracejada**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
- Cor: Verde (ganhando) ou Vermelho (perdendo)
- Posição: Preço de entrada da operação
- Estilo: Linha tracejada (dashed)
- Animação: Muda de cor em tempo real

#### 2. **Badge de Porcentagem**
```
┌──────────┐
│ +2.45%  │  (Verde - Lucro)
└──────────┘

┌──────────┐
│ -1.83%  │  (Vermelho - Perda)
└──────────┘
```
- Posição: Na ponta direita da linha horizontal
- Animação: Pulsa suavemente
- Cores dinâmicas baseadas em lucro/perda

#### 3. **Marcador de Entrada (Círculo)**
```
  ⬤  (Verde para CALL)
  ⬤  (Vermelho para PUT)
```
- Posição: No ponto de entrada no gráfico
- Borda branca
- Animação: Pulso contínuo
- Sombra brilhante

#### 4. **Linha Vertical Vermelha**
```
│
│  (Linha sólida vermelha)
│
│
```
- Posição: Onde a operação vai expirar
- Gradiente: Mais transparente nas bordas
- Animação: Pulsa suavemente

#### 5. **Relógio Circular de Countdown**
```
    ┌──────┐
    │  37  │  (Segundos restantes)
    └──────┘
```
- Posição: Em cima da linha vertical
- Borda vermelha pulsante
- Fundo escuro semi-transparente
- Animação urgente quando < 10 segundos

## 🎬 Funcionamento em Tempo Real

### Ao Abrir Operação:
```
1. ⬤ Círculo verde/vermelho aparece (entrada)
2. ━━━ Linha horizontal tracejada
3. 📊 Badge com 0.00%
4. │ Linha vertical no ponto de expiração
5. ⏰ Relógio circular mostrando tempo
```

### Durante a Operação:
```
Se GANHANDO:
  ━━━ Linha VERDE
  📊 Badge VERDE com +X.XX%
  ⬤ Círculo pulsante verde
  
Se PERDENDO:
  ━━━ Linha VERMELHA
  📊 Badge VERMELHO com -X.XX%
  ⬤ Círculo pulsante vermelho
```

### Últimos 10 Segundos:
```
⏰ Relógio:
  - Aumenta de tamanho
  - Pulsa mais rápido
  - Background pisca vermelho
  - Borda mais brilhante
```

### Ao Expirar:
```
1. Todos os elementos desaparecem
2. Notificação de resultado aparece
3. Vai para o histórico
```

## 🎨 Cores e Estados

### Verde (#26a69a):
- ✅ Operação em lucro
- ✅ CALL em alta
- ✅ Badge positivo

### Vermelho (#ef5350):
- ❌ Operação em perda  
- ❌ PUT em baixa
- ❌ Badge negativo
- ❌ Linha de expiração

### Animações:

**Badge:**
```css
0% → 100% → 105% → 100%  (pulso)
```

**Relógio Normal:**
```css
0% → 100% → 108% → 100%  (pulso suave)
```

**Relógio Urgente (<10s):**
```css
0% → 100% → 115% → 100%  (pulso rápido)
Background: rgba vermelho piscando
```

**Círculo de Entrada:**
```css
0% → 100% → 120% → 100%  (pulso forte)
Sombra: 15px → 25px → 15px
```

**Linha Vertical:**
```css
Opacity: 60% → 100% → 60%  (fade)
```

## 📐 Posicionamento

### Linha Horizontal:
- Y: Calculado baseado no preço de entrada
- X: 0 até borda direita (menos 80px para o badge)

### Badge:
- Fixa na direita da linha horizontal
- Centralizado verticalmente na linha

### Círculo de Entrada:
- X: ~20px da esquerda (ponto inicial)
- Y: Mesma altura da linha horizontal

### Linha Vertical:
- X: Calculado baseado no tempo (progresso até expiração)
- Y: 0 até altura total do gráfico

### Relógio:
- X: Centro da linha vertical
- Y: -40px acima do topo do gráfico

## 🚀 Como Funciona

```javascript
Intervalo 1 segundo:
  1. Calcula tempo restante
  2. Calcula lucro/perda atual
  3. Atualiza posição da linha vertical
  4. Atualiza badge de porcentagem
  5. Atualiza número do relógio
  6. Muda cores se necessário
```

## 📱 Exemplo Visual Completo

```
       ⏰ 37                    ← Relógio circular vermelho
        │
        │                       ← Linha vertical vermelha
  ⬤━━━━━━━━━━━━━━━━━━┃+2.45%┃  ← Linha horizontal verde + badge
   ↑                   ↑
   Entrada             Porcentagem
   (círculo            (badge pulsante)
    pulsante)
        │
        │
        │
```

### CALL em Lucro:
```
Status: GANHANDO
├─ Linha horizontal: Verde tracejada
├─ Badge: Verde "+2.45%"
├─ Círculo: Verde pulsante
├─ Linha vertical: Vermelha (expiração)
└─ Relógio: "37" (segundos)
```

### PUT em Perda:
```
Status: PERDENDO
├─ Linha horizontal: Vermelha tracejada
├─ Badge: Vermelho "-1.83%"
├─ Círculo: Vermelho pulsante
├─ Linha vertical: Vermelha (expiração)
└─ Relógio: "22" (segundos)
```

## 🔧 Tecnologia

- **HTML Overlays:** Divs posicionados sobre o gráfico
- **CSS Animations:** Keyframes para pulsos
- **JavaScript:** Cálculo de posições em tempo real
- **Update Rate:** 1 segundo (60 FPS para animações)

## ⚡ Performance

- Overlays são reusados (não recriados)
- Animações CSS (GPU accelerated)
- Cálculos otimizados
- Elementos removidos ao expirar

---

**Resultado: Visual IDÊNTICO ao IQ Option! 🎯**


