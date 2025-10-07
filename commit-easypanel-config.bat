@echo off
setlocal enabledelayedexpansion

echo.
echo ==========================================
echo 🚀 Commit - Easypanel Config
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

REM Verificar Dockerfile.easypanel
if exist "Dockerfile.easypanel" (
    echo ✅ Dockerfile.easypanel - ENCONTRADO
) else (
    echo ❌ Dockerfile.easypanel - NÃO ENCONTRADO
)

REM Verificar easypanel.yml
if exist "easypanel.yml" (
    echo ✅ easypanel.yml - ENCONTRADO
) else (
    echo ❌ easypanel.yml - NÃO ENCONTRADO
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
git commit -m "Easypanel Config - Força Dockerfile

- Criado easypanel.yml para configurar serviço
- Criado Dockerfile.easypanel como alternativa
- Atualizado .dockerignore para excluir .nixpacks
- Configuração específica para Easypanel
- Força uso do Dockerfile customizado

Configuração no Easypanel:
- Service Type: Docker
- Dockerfile Path: Dockerfile ou Dockerfile.easypanel
- Port: 5000
- Usar easypanel.yml se disponível

Solução para erros:
- .nixpacks/nixpkgs-*.nix not found
- Nixpacks Dockerfile automático
- Força uso do Dockerfile customizado

Vantagens:
- Configuração específica do Easypanel
- Força uso do Dockerfile
- Evita Nixpacks automático
- Build mais confiável"
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
echo 🎉 COMMIT CONCLUÍDO - EASYPANEL CONFIG!
echo ==========================================
echo.
echo 📋 Configuração no Easypanel:
echo 1. Service Type: Docker
echo 2. Dockerfile Path: Dockerfile ou Dockerfile.easypanel
echo 3. Port: 5000
echo 4. Usar easypanel.yml se disponível
echo.
echo 🔧 Solução implementada:
echo - easypanel.yml criado
echo - Dockerfile.easypanel criado
echo - .dockerignore atualizado
echo - Configuração específica
echo.
echo 🎯 Vantagens:
echo - Configuração específica do Easypanel
echo - Força uso do Dockerfile
echo - Evita Nixpacks automático
echo - Build mais confiável
echo.
echo 🧪 Teste após deploy:
echo curl https://seu-dominio.com/api/health
echo.
echo 🚀 Problemas resolvidos:
echo - .nixpacks/nixpkgs-*.nix not found
echo - Nixpacks Dockerfile automático
echo - Força uso do Dockerfile customizado
echo.
echo ✅ Agora com configuração específica do Easypanel!
echo.
pause
