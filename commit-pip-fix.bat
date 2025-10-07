@echo off
setlocal enabledelayedexpansion

echo.
echo ==========================================
echo 🚀 Commit - Fix pip command not found
echo ==========================================
echo.

echo 📁 Diretório atual: %CD%
echo.

echo 🔍 Verificando arquivos atualizados...
echo.

REM Verificar nixpacks.toml
if exist "nixpacks.toml" (
    echo ✅ nixpacks.toml - ENCONTRADO
) else (
    echo ❌ nixpacks.toml - NÃO ENCONTRADO
)

REM Verificar Procfile
if exist "Procfile" (
    echo ✅ Procfile - ENCONTRADO
) else (
    echo ❌ Procfile - NÃO ENCONTRADO
)

REM Verificar build.sh
if exist "build.sh" (
    echo ✅ build.sh - ENCONTRADO
) else (
    echo ❌ build.sh - NÃO ENCONTRADO
)

REM Verificar app.py na raiz
if exist "app.py" (
    echo ✅ app.py - ENCONTRADO
) else (
    echo ❌ app.py - NÃO ENCONTRADO
)

REM Verificar requirements.txt
if exist "requirements.txt" (
    echo ✅ requirements.txt - ENCONTRADO
) else (
    echo ❌ requirements.txt - NÃO ENCONTRADO
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
git commit -m "Fix pip command not found - Nixpacks

- Atualizado nixpacks.toml para usar python3 -m pip
- Adicionado python3Packages.pip aos nixPkgs
- Atualizado Procfile para usar python3 -m gunicorn
- Criado build.sh com comandos corretos
- Configurado PATH para /opt/venv/bin
- Fix para erro: /bin/bash: line 1: pip: command not found

Configuração no Easypanel:
- Service Type: Python (Nixpacks)
- Build Command: automático (nixpacks.toml)
- Start Command: automático (Procfile)
- Port: 5000

Comandos corrigidos:
- python3 -m pip install -r requirements.txt
- python3 -m gunicorn --bind 0.0.0.0:5000 app:app"
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
echo 🎉 COMMIT CONCLUÍDO - PIP FIX!
echo ==========================================
echo.
echo 📋 Configuração no Easypanel:
echo 1. Service Type: Python (Nixpacks)
echo 2. Build Command: automático (nixpacks.toml)
echo 3. Start Command: automático (Procfile)
echo 4. Port: 5000
echo.
echo 🔧 Correções implementadas:
echo - nixpacks.toml: python3 -m pip
echo - Procfile: python3 -m gunicorn
echo - build.sh: comandos corretos
echo - PATH configurado para /opt/venv/bin
echo.
echo 🧪 Teste após deploy:
echo curl https://seu-dominio.com/api/health
echo.
echo 🎯 Fix para erro:
echo /bin/bash: line 1: pip: command not found
echo.
echo ✅ Agora usa: python3 -m pip
echo.
pause
