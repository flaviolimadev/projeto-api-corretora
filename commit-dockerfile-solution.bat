@echo off
setlocal enabledelayedexpansion

echo.
echo ==========================================
echo 🚀 Commit - Solução Dockerfile Simples
echo ==========================================
echo.

echo 📁 Diretório atual: %CD%
echo.

echo 🔍 Verificando arquivos...
echo.

REM Verificar Dockerfile
if exist "Dockerfile" (
    echo ✅ Dockerfile - ENCONTRADO
) else (
    echo ❌ Dockerfile - NÃO ENCONTRADO
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

REM Verificar Procfile
if exist "Procfile" (
    echo ✅ Procfile - ENCONTRADO
) else (
    echo ❌ Procfile - NÃO ENCONTRADO
)

REM Verificar se nixpacks.toml foi removido
if not exist "nixpacks.toml" (
    echo ✅ nixpacks.toml - REMOVIDO (correto)
) else (
    echo ⚠️  nixpacks.toml - AINDA EXISTE (deve ser removido)
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
git commit -m "Solução Dockerfile Simples - Easypanel

- Criado Dockerfile simples na raiz
- Removido nixpacks.toml (causava conflitos)
- Atualizado app.py como entry point
- Simplificado Procfile para python app.py
- Configurado PYTHONPATH corretamente
- Usa imagem Python oficial

Configuração no Easypanel:
- Service Type: Docker
- Dockerfile Path: Dockerfile
- Port: 5000

Solução para erros:
- NIXPACKS_PATH undefined
- nix-env installation failed
- pip command not found

Vantagens:
- Dockerfile simples e confiável
- Sem dependências do Nixpacks
- Build mais rápido
- Fácil de debugar"
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
echo 🎉 COMMIT CONCLUÍDO - DOCKERFILE SIMPLES!
echo ==========================================
echo.
echo 📋 Configuração no Easypanel:
echo 1. Service Type: Docker
echo 2. Dockerfile Path: Dockerfile
echo 3. Port: 5000
echo.
echo 🔧 Solução implementada:
echo - Dockerfile simples na raiz
echo - nixpacks.toml removido
echo - app.py como entry point
echo - PYTHONPATH configurado
echo - Imagem Python oficial
echo.
echo 🎯 Vantagens:
echo - Sem conflitos do Nixpacks
echo - Build mais rápido
echo - Fácil de debugar
echo - Configuração simples
echo.
echo 🧪 Teste após deploy:
echo curl https://seu-dominio.com/api/health
echo.
echo 🚀 Problemas resolvidos:
echo - NIXPACKS_PATH undefined
echo - nix-env installation failed
echo - pip command not found
echo.
pause
