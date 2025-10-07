"""
Entry point para o Easypanel
Este arquivo redireciona para o app principal na pasta webapp
"""

import sys
import os

# Adicionar o diretório webapp ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'webapp'))

# Importar o app principal
from webapp.app import app

if __name__ == '__main__':
    # Para desenvolvimento local
    app.run(host='0.0.0.0', port=5000, debug=False)
else:
    # Para produção com gunicorn
    pass
