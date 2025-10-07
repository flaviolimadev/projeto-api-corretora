@echo off
setlocal enabledelayedexpansion

echo.
echo ==========================================
echo 🚀 Commit - Docker Only (Sem Nixpacks)
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

REM Verificar .dockerignore
if exist ".dockerignore" (
    echo ✅ .dockerignore - ENCONTRADO
) else (
    echo ❌ .dockerignore - NÃO ENCONTRADO
)

REM Verificar se Procfile foi removido
if not exist "Procfile" (
    echo ✅ Procfile - REMOVIDO (correto)
) else (
    echo ⚠️  Procfile - AINDA EXISTE (deve ser removido)
)

REM Verificar se runtime.txt foi removido
if not exist "runtime.txt" (
    echo ✅ runtime.txt - REMOVIDO (correto)
) else (
    echo ⚠️  runtime.txt - AINDA EXISTE (deve ser removido)
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
git commit -m "Docker Only - Força uso do Dockerfile

- Dockerfile otimizado com python -m pip
- Removido Procfile (evita Nixpacks)
- Removido runtime.txt (evita Nixpacks)
- Removido nixpacks.toml (evita Nixpacks)
- Criado .dockerignore para build limpo
- Adicionado build-essential para compilação
- Comando: python -m pip install

Configuração no Easypanel:
- Service Type: Docker
- Dockerfile Path: Dockerfile
- Port: 5000

Solução para erros:
- pip: command not found
- NIXPACKS_PATH undefined
- nix-env installation failed

Vantagens:
- Força uso do Dockerfile
- Evita detecção automática do Nixpacks
- Build mais rápido e confiável
- Sem conflitos de ambiente"
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
echo 🎉 COMMIT CONCLUÍDO - DOCKER ONLY!
echo ==========================================
echo.
echo 📋 Configuração no Easypanel:
echo 1. Service Type: Docker
echo 2. Dockerfile Path: Dockerfile
echo 3. Port: 5000
echo.
echo 🔧 Solução implementada:
echo - Dockerfile otimizado
echo - Procfile removido
echo - runtime.txt removido
echo - nixpacks.toml removido
echo - .dockerignore criado
echo - python -m pip install
echo.
echo 🎯 Vantagens:
echo - Força uso do Dockerfile
echo - Evita Nixpacks automático
echo - Build mais rápido
echo - Sem conflitos de ambiente
echo.
echo 🧪 Teste após deploy:
echo curl https://seu-dominio.com/api/health
echo.
echo 🚀 Problemas resolvidos:
echo - pip: command not found
echo - NIXPACKS_PATH undefined
echo - nix-env installation failed
echo.
echo ✅ Agora usa apenas Dockerfile!
echo.
pause
