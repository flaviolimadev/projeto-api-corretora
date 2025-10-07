# 🚀 Instalação Rápida

## Windows

1. **Abra o PowerShell ou CMD na pasta `webapp`**

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicie a aplicação:**
   ```bash
   start.bat
   ```
   
   OU
   
   ```bash
   python app.py
   ```

4. **Abra o navegador em:**
   ```
   http://localhost:5000
   ```

## Linux/Mac

1. **Abra o terminal na pasta `webapp`**

2. **Instale as dependências:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Dê permissão de execução ao script:**
   ```bash
   chmod +x start.sh
   ```

4. **Inicie a aplicação:**
   ```bash
   ./start.sh
   ```
   
   OU
   
   ```bash
   python3 app.py
   ```

5. **Abra o navegador em:**
   ```
   http://localhost:5000
   ```

## 🎯 Testando

1. No campo "Ativo", digite: `BINANCE:BTCUSDT`
2. Clique em "Iniciar Stream"
3. Observe o gráfico e os preços sendo atualizados em tempo real!

## ⚡ Outros Símbolos para Testar

- `BINANCE:ETHUSDT` (Ethereum)
- `BINANCE:BNBUSDT` (Binance Coin)
- `BINANCE:ADAUSDT` (Cardano)
- `BINANCE:DOGEUSDT` (Dogecoin)

## 🔧 Troubleshooting

### Erro: ModuleNotFoundError

```bash
pip install -r requirements.txt --upgrade
```

### Porta 5000 já está em uso

Edite `app.py` e altere a linha:
```python
socketio.run(app, debug=True, host='0.0.0.0', port=5001)  # Altere para 5001 ou outra porta
```

### Conexão WebSocket falha

- Verifique seu firewall
- Certifique-se de que não há proxy bloqueando WebSockets
- Tente desabilitar extensões do navegador

## 📞 Suporte

Se encontrar problemas, verifique:
1. A versão do Python (deve ser 3.8+)
2. Os logs no terminal/console
3. O console do navegador (F12)


