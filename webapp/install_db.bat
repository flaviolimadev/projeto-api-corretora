@echo off
echo ========================================
echo TradingView Scraper - Database Setup
echo ========================================
echo.

echo [1/4] Instalando dependencias Python...
pip install prisma python-dotenv aiohttp APScheduler python-dateutil

echo.
echo [2/4] Gerando Prisma Client...
prisma generate

echo.
echo [3/4] Criando banco de dados...
prisma db push

echo.
echo [4/4] Verificando instalacao...
python -c "from prisma import Prisma; print('OK - Prisma instalado com sucesso!')"

echo.
echo ========================================
echo Instalacao concluida!
echo ========================================
echo.
echo Proximos passos:
echo 1. python workers/sync_categories.py
echo 2. python app_db.py
echo.
pause
