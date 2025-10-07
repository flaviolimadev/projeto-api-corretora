@echo off
setlocal enabledelayedexpansion

echo.
echo ==========================================
echo 🚀 Commit Final + Instruções Easypanel
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

REM Verificar instruções
if exist "INSTRUCOES_EASYPANEL.md" (
    echo ✅ INSTRUCOES_EASYPANEL.md - ENCONTRADO
) else (
    echo ❌ INSTRUCOES_EASYPANEL.md - NÃO ENCONTRADO
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
git commit -m "Final Docker + Instruções Easypanel

- Dockerfile simplificado e funcional
- INSTRUCOES_EASYPANEL.md com passo a passo
- Problema identificado: Easypanel forçando Nixpacks

Configuração no Easypanel:
1. Builder Type: Docker (NÃO Nixpacks)
2. Dockerfile Path: Dockerfile
3. Build Context: .
4. Port: 5000

Instruções detalhadas em INSTRUCOES_EASYPANEL.md"
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
echo 🎉 COMMIT CONCLUÍDO!
echo ==========================================
echo.
echo 🚨 ATENÇÃO - LEIA COM ATENÇÃO:
echo.
echo O problema NÃO está no código!
echo O problema está na CONFIGURAÇÃO DO EASYPANEL!
echo.
echo 📋 PRÓXIMOS PASSOS:
echo.
echo 1. Abra o arquivo: INSTRUCOES_EASYPANEL.md
echo 2. Siga as instruções passo a passo
echo 3. Configure o Easypanel para usar Docker
echo 4. Faça o rebuild
echo.
echo 🔧 CONFIGURAÇÃO NECESSÁRIA:
echo - Builder Type: Docker (NÃO Nixpacks)
echo - Dockerfile Path: Dockerfile
echo - Build Context: .
echo - Port: 5000
echo.
echo ✅ Após configurar corretamente, o build funcionará!
echo.
pause
