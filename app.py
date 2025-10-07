"""
Entry point para o Easypanel/Nixpacks
Este arquivo redireciona para o app principal na pasta webapp
"""

import sys
import os

# Adicionar o diretório webapp ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'webapp'))

# Importar e executar o app principal
from webapp.app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
