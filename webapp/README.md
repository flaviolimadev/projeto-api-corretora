# Trading View - Aplicação Web de Preços em Tempo Real

Esta é uma aplicação web moderna para visualizar gráficos e preços de ativos em tempo real usando a biblioteca `tradingview-scraper`.

## 🚀 Características

- **Gráfico em Tempo Real**: Visualize candlesticks atualizados em tempo real usando TradingView Lightweight Charts
- **Preço ao Vivo**: Display do preço atual com mudanças em tempo real
- **Informações Detalhadas**: Veja abertura, máxima, mínima e volume
- **Interface Moderna**: Design dark mode inspirado no TradingView
- **WebSocket**: Comunicação em tempo real entre servidor e cliente

## 📋 Pré-requisitos

- Python 3.8+
- pip

## 🔧 Instalação

1. **Navegue até o diretório da aplicação web:**
   ```bash
   cd tradingview-scraper/webapp
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Como Usar

1. **Inicie o servidor:**
   ```bash
   python app.py
   ```

2. **Abra o navegador e acesse:**
   ```
   http://localhost:5000
   ```

3. **Use a aplicação:**
   - Digite o símbolo do ativo no formato `EXCHANGE:SYMBOL` (ex: `BINANCE:BTCUSDT`)
   - Clique em "Iniciar Stream"
   - Observe o gráfico e os preços sendo atualizados em tempo real
   - Clique em "Parar Stream" para interromper

## 📊 Exemplos de Símbolos

- **Criptomoedas:**
  - `BINANCE:BTCUSDT` - Bitcoin
  - `BINANCE:ETHUSDT` - Ethereum
  - `BINANCE:BNBUSDT` - Binance Coin

- **Forex:**
  - `FXOPEN:EURUSD` - Euro/Dólar
  - `FXOPEN:GBPUSD` - Libra/Dólar

- **Commodities:**
  - `FXOPEN:XAUUSD` - Ouro

## 🏗️ Estrutura do Projeto

```
webapp/
├── app.py                 # Backend Flask com Socket.IO
├── requirements.txt       # Dependências Python
├── README.md             # Esta documentação
├── templates/
│   └── index.html        # Template HTML principal
└── static/
    ├── style.css         # Estilos CSS
    └── app.js            # JavaScript do cliente
```

## 🛠️ Tecnologias Utilizadas

- **Backend:**
  - Flask - Framework web
  - Flask-SocketIO - WebSocket para comunicação em tempo real
  - tradingview-scraper - Biblioteca para obter dados do TradingView

- **Frontend:**
  - HTML5/CSS3
  - JavaScript (ES6+)
  - Socket.IO Client - Cliente WebSocket
  - TradingView Lightweight Charts - Gráficos profissionais

## 🔍 Como Funciona

1. O usuário insere um símbolo de ativo
2. O frontend envia uma requisição via WebSocket para o backend
3. O backend cria uma conexão com o TradingView via `tradingview-scraper`
4. Os dados OHLCV são recebidos em tempo real
5. O backend emite os dados para o frontend via WebSocket
6. O frontend atualiza o gráfico e os displays de preço

## ⚠️ Notas Importantes

- Certifique-se de que o símbolo está no formato correto: `EXCHANGE:SYMBOL`
- A conexão é mantida em tempo real, consumindo recursos enquanto ativa
- Para múltiplos símbolos, abra múltiplas janelas/abas do navegador

## 🐛 Troubleshooting

**Erro de conexão:**
- Verifique se o servidor Flask está rodando
- Verifique se a porta 5000 não está bloqueada

**Símbolo inválido:**
- Confirme que o formato está correto: `EXCHANGE:SYMBOL`
- Verifique se o símbolo existe no TradingView

**Gráfico não atualiza:**
- Verifique o console do navegador para erros
- Tente parar e reiniciar o stream

## 📝 Licença

Este projeto usa a biblioteca `tradingview-scraper` sob licença MIT.

## 🤝 Contribuindo

Sinta-se livre para abrir issues ou pull requests para melhorias!

