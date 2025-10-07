@echo off
setlocal enabledelayedexpansion

echo.
echo ==========================================
echo 🚀 Commit - Final Docker Solution
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

REM Verificar docker-compose.yml
if exist "docker-compose.yml" (
    echo ✅ docker-compose.yml - ENCONTRADO
) else (
    echo ❌ docker-compose.yml - NÃO ENCONTRADO
)

REM Verificar .dockerignore
if exist ".dockerignore" (
    echo ✅ .dockerignore - ENCONTRADO
) else (
    echo ❌ .dockerignore - NÃO ENCONTRADO
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

REM Verificar se arquivos Nixpacks foram removidos
if not exist "Procfile" (
    echo ✅ Procfile - REMOVIDO (correto)
) else (
    echo ⚠️  Procfile - AINDA EXISTE (deve ser removido)
)

if not exist "runtime.txt" (
    echo ✅ runtime.txt - REMOVIDO (correto)
) else (
    echo ⚠️  runtime.txt - AINDA EXISTE (deve ser removido)
)

if not exist "nixpacks.toml" (
    echo ✅ nixpacks.toml - REMOVIDO (correto)
) else (
    echo ⚠️  nixpacks.toml - AINDA EXISTE (deve ser removido)
)

if not exist "easypanel.yml" (
    echo ✅ easypanel.yml - REMOVIDO (correto)
) else (
    echo ⚠️  easypanel.yml - AINDA EXISTE (deve ser removido)
)

if not exist "Dockerfile.easypanel" (
    echo ✅ Dockerfile.easypanel - REMOVIDO (correto)
) else (
    echo ⚠️  Dockerfile.easypanel - AINDA EXISTE (deve ser removido)
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
git commit -m "Final Docker Solution - Força Dockerfile

- Dockerfile simplificado e direto
- Removido easypanel.yml (causava confusão)
- Removido Dockerfile.easypanel (desnecessário)
- Criado docker-compose.yml para referência
- .dockerignore atualizado para excluir Nixpacks
- Configuração mínima e limpa

Configuração no Easypanel:
- Service Type: Docker
- Dockerfile Path: Dockerfile
- Port: 5000

Solução para erros:
- .nixpacks/nixpkgs-*.nix not found
- Nixpacks Dockerfile automático
- Força uso do Dockerfile customizado

Vantagens:
- Dockerfile simples e direto
- Sem configurações desnecessárias
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
echo 🎉 COMMIT CONCLUÍDO - FINAL DOCKER!
echo ==========================================
echo.
echo 📋 Configuração no Easypanel:
echo 1. Service Type: Docker
echo 2. Dockerfile Path: Dockerfile
echo 3. Port: 5000
echo.
echo 🔧 Solução implementada:
echo - Dockerfile simplificado
echo - easypanel.yml removido
echo - Dockerfile.easypanel removido
echo - docker-compose.yml criado
echo - .dockerignore atualizado
echo.
echo 🎯 Vantagens:
echo - Dockerfile simples e direto
echo - Sem configurações desnecessárias
echo - Build mais rápido
echo - Fácil de debugar
echo.
echo 🧪 Teste após deploy:
echo curl https://seu-dominio.com/api/health
echo.
echo 🚀 Problemas resolvidos:
echo - .nixpacks/nixpkgs-*.nix not found
echo - Nixpacks Dockerfile automático
echo - Força uso do Dockerfile customizado
echo.
echo ✅ Solução final - Dockerfile simples!
echo.
pause
