@echo off
echo ========================================
echo Configurando PostgreSQL (Producao)
echo ========================================
echo.
echo Banco: api-corretora
echo Host: easypainel.ctrlser.com:5434
echo.

echo [1/3] Restaurando schema PostgreSQL...
copy /Y prisma\schema.prisma.backup prisma\schema.prisma 2>nul
if not exist prisma\schema.prisma.backup (
    echo Backup nao encontrado, usando schema original...
)

echo.
echo [2/3] Gerando Prisma Client...
prisma generate

echo.
echo [3/3] Criando tabelas no banco PostgreSQL...
prisma db push

echo.
echo ========================================
echo PostgreSQL configurado com sucesso!
echo ========================================
echo.
echo Proximos passos:
echo 1. python workers/sync_categories.py
echo 2. python workers/sync_assets.py
echo 3. python workers/main_worker.py
echo.
pause
