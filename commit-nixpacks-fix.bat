@echo off
setlocal enabledelayedexpansion

echo.
echo ==========================================
echo 🚀 Commit - Fix Nixpacks Easypanel
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

REM Verificar app.py na raiz
if exist "app.py" (
    echo ✅ app.py - ENCONTRADO
) else (
    echo ❌ app.py - NÃO ENCONTRADO
)

REM Verificar nixpacks.toml
if exist "nixpacks.toml" (
    echo ✅ nixpacks.toml - ENCONTRADO
) else (
    echo ❌ nixpacks.toml - NÃO ENCONTRADO
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
git commit -m "Fix Nixpacks Easypanel - pip command not found

- Adicionado app.py na raiz como entry point
- Configurado nixpacks.toml para Nixpacks
- Atualizado requirements.txt com setuptools e wheel
- Simplificado Procfile para usar app.py da raiz
- Configurado PYTHONPATH corretamente
- Entry point redireciona para webapp/app.py

Configuração no Easypanel:
- Service Type: Python (Nixpacks)
- Build Command: automático (nixpacks.toml)
- Start Command: automático (Procfile)
- Port: 5000

Fix para erro: pip: command not found"
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
echo 🎉 COMMIT CONCLUÍDO - NIXPACKS FIX!
echo ==========================================
echo.
echo 📋 Configuração no Easypanel:
echo 1. Service Type: Python (Nixpacks)
echo 2. Build Command: automático (nixpacks.toml)
echo 3. Start Command: automático (Procfile)
echo 4. Port: 5000
echo.
echo 🔧 Arquivos de configuração:
echo - app.py (entry point na raiz)
echo - nixpacks.toml (configuração Nixpacks)
echo - requirements.txt (dependências)
echo - Procfile (comando de start)
echo - runtime.txt (versão Python)
echo.
echo 🧪 Teste após deploy:
echo curl https://seu-dominio.com/api/health
echo.
echo 🎯 Fix implementado:
echo - Entry point na raiz redireciona para webapp
echo - Nixpacks configurado corretamente
echo - PYTHONPATH configurado
echo - Dependências atualizadas
echo.
pause
