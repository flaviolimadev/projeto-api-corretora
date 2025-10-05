@echo off
echo ========================================
echo Configurando SQLite (Desenvolvimento)
echo ========================================
echo.

echo [1/3] Copiando schema SQLite...
copy /Y prisma\schema_sqlite.prisma prisma\schema.prisma

echo.
echo [2/3] Gerando Prisma Client...
prisma generate

echo.
echo [3/3] Criando banco de dados SQLite...
prisma db push

echo.
echo ========================================
echo SQLite configurado com sucesso!
echo ========================================
echo.
echo Arquivo do banco: trading.db
echo.
echo Proximos passos:
echo 1. python workers/sync_categories.py
echo 2. prisma studio (para visualizar dados)
echo.
pause
