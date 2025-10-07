@echo off
setlocal enabledelayedexpansion

echo.
echo ==========================================
echo 🚀 Commit - Easypanel sem Dockerfile
echo ==========================================
echo.

echo 📁 Diretório atual: %CD%
echo.

echo 🔍 Verificando arquivos criados...
echo.

REM Verificar requirements.txt
if exist "requirements.txt" (
    echo ✅ requirements.txt - ENCONTRADO
) else (
    echo ❌ requirements.txt - NÃO ENCONTRADO
)

REM Verificar Procfile
if exist "Procfile" (
    echo ✅ Procfile - ENCONTRADO
) else (
    echo ❌ Procfile - NÃO ENCONTRADO
)

REM Verificar runtime.txt
if exist "runtime.txt" (
    echo ✅ runtime.txt - ENCONTRADO
) else (
    echo ❌ runtime.txt - NÃO ENCONTRADO
)

REM Verificar webapp/app.py
if exist "webapp\app.py" (
    echo ✅ webapp\app.py - ENCONTRADO
) else (
    echo ❌ webapp\app.py - NÃO ENCONTRADO
)

echo.

REM Verificar status do git
echo 📋 Status do Git:
git status --short
echo.

REM Adicionar todos os arquivos
echo 📦 Adicionando arquivos ao Git...
git add .
if !errorlevel! neq 0 (
    echo ❌ Erro ao adicionar arquivos
    pause
    exit /b 1
)

echo ✅ Arquivos adicionados
echo.

REM Fazer commit
echo 💾 Fazendo commit...
git commit -m "Configuração Easypanel sem Dockerfile

- Adicionado requirements.txt na raiz
- Adicionado Procfile para comando de start
- Adicionado runtime.txt para versão Python
- Configuração Python nativa do Easypanel
- Sem necessidade de Dockerfile
- Build mais rápido e simples

Configuração no Easypanel:
- Service Type: Python
- Python Version: 3.11
- Build Command: pip install -r requirements.txt
- Start Command: cd webapp && gunicorn --bind 0.0.0.0:5000 --workers 4 --worker-class eventlet app:app
- Working Directory: /app/webapp
- Port: 5000"
if !errorlevel! neq 0 (
    echo ❌ Erro ao fazer commit
    pause
    exit /b 1
)

echo ✅ Commit realizado com sucesso
echo.

REM Push para o repositório
echo 🚀 Enviando para o repositório...
git push origin main
if !errorlevel! neq 0 (
    echo ❌ Erro ao enviar para o repositório
    pause
    exit /b 1
)

echo ✅ Push realizado com sucesso
echo.

echo ==========================================
echo 🎉 COMMIT CONCLUÍDO - SEM DOCKERFILE!
echo ==========================================
echo.
echo 📋 Configuração no Easypanel:
echo 1. Service Type: Python
echo 2. Python Version: 3.11
echo 3. Build Command: pip install -r requirements.txt
echo 4. Start Command: cd webapp && gunicorn --bind 0.0.0.0:5000 --workers 4 --worker-class eventlet app:app
echo 5. Working Directory: /app/webapp
echo 6. Port: 5000
echo.
echo 🧪 Teste após deploy:
echo curl https://seu-dominio.com/api/health
echo.
echo 📚 Documentação: webapp\easypanel-no-dockerfile.md
echo.
echo 🎯 Vantagens desta configuração:
echo - Sem necessidade de Dockerfile
echo - Usa imagem Python oficial
echo - Build mais rápido
echo - Configuração mais simples
echo - Fácil de debugar
echo.
pause
