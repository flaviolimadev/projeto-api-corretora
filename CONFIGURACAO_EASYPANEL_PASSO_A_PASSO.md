# 🚨 CONFIGURAÇÃO EASYPANEL - PASSO A PASSO

## ⚠️ PROBLEMA IDENTIFICADO

O Easypanel está **GERANDO AUTOMATICAMENTE** um Dockerfile do Nixpacks e **IGNORANDO** o nosso Dockerfile.

Veja na linha do erro:
```
-f /etc/easypanel/projects/corretora/app/code/.nixpacks/Dockerfile
```

Ele está usando `.nixpacks/Dockerfile` (gerado automaticamente) em vez de `Dockerfile` (o nosso).

## ✅ SOLUÇÃO - PASSO A PASSO

### PASSO 1: Acesse o Easypanel

1. Abra seu navegador
2. Vá para: `https://seu-easypanel.com` (ou o endereço do seu Easypanel)
3. Faça login

### PASSO 2: Acesse o Projeto

1. Na lista de projetos, clique em **`corretora`**
2. Você verá o serviço **`app`** (ou similar)

### PASSO 3: Edite o Serviço

1. Clique no serviço **`app`**
2. Procure por um botão **"Settings"**, **"Edit"**, **"Configure"** ou ícone de engrenagem ⚙️
3. Clique nele

### PASSO 4: Encontre as Configurações de Build

Procure por uma das seguintes seções:
- **"Build Settings"**
- **"Source"**
- **"General"**
- **"Advanced Settings"**

### PASSO 5: MUDE O BUILDER TYPE

**ISTO É CRÍTICO!**

Procure por um campo chamado:
- **"Builder"**
- **"Builder Type"**
- **"Build Method"**
- **"Build Provider"**

Você verá opções como:
- ⚠️ **Nixpacks** (está selecionado atualmente - ERRADO!)
- ✅ **Docker** (selecione esta!)
- **Buildpacks**
- **Heroku**

**SELECIONE: Docker**

### PASSO 6: Configure o Dockerfile Path (se aparecer)

Após selecionar "Docker", pode aparecer um campo:
- **"Dockerfile"** ou **"Dockerfile Path"**

Configure como:
```
Dockerfile
```

Ou:
```
./Dockerfile
```

### PASSO 7: Configure o Build Context (se aparecer)

Se houver um campo **"Build Context"** ou **"Context"**:
```
.
```

Ou deixe vazio (usará a raiz por padrão).

### PASSO 8: Verifique a Porta

Certifique-se de que a porta está configurada como:
```
5000
```

### PASSO 9: Salve as Configurações

1. Clique em **"Save"**, **"Update"** ou **"Apply"**
2. Aguarde a confirmação

### PASSO 10: Faça o Rebuild

1. Procure por um botão **"Deploy"**, **"Rebuild"** ou **"Redeploy"**
2. Clique nele
3. Aguarde o build

## 📸 ONDE ENCONTRAR NO EASYPANEL

### Opção 1: Interface Principal

```
Projetos → corretora → app → ⚙️ Settings → Source/Build
```

### Opção 2: Menu Lateral

```
app → General → Builder Type
```

### Opção 3: Advanced Settings

```
app → Advanced → Build Configuration
```

## ✅ COMO SABER SE ESTÁ CORRETO

Após configurar, você deve ver:

**ANTES (ERRADO):**
```
╔══════════════════════════════ Nixpacks v1.34.1 ══════════════════════════════╗
```

**DEPOIS (CORRETO):**
```
Building with Docker...
Step 1/10 : FROM python:3.11-slim
```

## 🎯 CONFIGURAÇÃO FINAL

Certifique-se de que está assim:

```
Builder Type: Docker
Dockerfile: Dockerfile
Build Context: .
Port: 5000
```

## 🔍 ALTERNATIVA - CRIE UM NOVO SERVIÇO

Se não encontrar onde mudar o Builder Type:

1. **Pause ou delete o serviço atual**
2. **Crie um novo serviço:**
   - Clique em **"Add Service"** ou **"New Service"**
   - Selecione **"From GitHub"** ou **"From Git"**
   - Conecte seu repositório
   - **IMPORTANTE: Selecione "Docker" como Builder Type**
   - Configure:
     - Name: `app`
     - Branch: `main`
     - Dockerfile: `Dockerfile`
     - Port: `5000`
   - Adicione as variáveis de ambiente
   - Deploy

## 📞 SE AINDA NÃO FUNCIONAR

### Verifique no Easypanel

1. **Vá para o serviço**
2. **Procure por "Logs" ou "Build Logs"**
3. **Verifique se ainda aparece "Nixpacks"**

### Se ainda aparecer Nixpacks

Possíveis causas:
1. **Configuração global do projeto** (não do serviço)
   - Vá para Settings do projeto `corretora`
   - Procure por "Default Builder" ou "Project Settings"
   - Mude para Docker

2. **Arquivo de configuração oculto**
   - Verifique se não há `.easypanel/config.json` ou similar no repositório

3. **Cache do Easypanel**
   - Tente fazer "Clear Cache" antes de rebuildar
   - Ou delete e recrie o serviço

### Suporte Easypanel

Se nada funcionar:
- **Documentação**: https://easypanel.io/docs
- **Discord**: https://discord.gg/easypanel
- **GitHub**: https://github.com/easypanel-io/easypanel

## 🎉 SUCESSO

Quando configurar corretamente, você verá no log:

```
Building with Docker...
Step 1/10 : FROM python:3.11-slim
Step 2/10 : WORKDIR /app
Step 3/10 : RUN apt-get update && apt-get install -y gcc g++ libpq-dev curl
...
Successfully built abc123def456
```

E **NÃO** verá:
```
╔══════════════════════════════ Nixpacks v1.34.1 ══════════════════════════════╗
```

## 🚀 CONCLUSÃO

O código está **100% correto**!

Você só precisa **CONFIGURAR O EASYPANEL** para usar **Docker** em vez de **Nixpacks**.

**CONFIGURE NO PAINEL DO EASYPANEL:**
```
Builder Type: Docker (NÃO Nixpacks)
```

Depois disso, o build funcionará perfeitamente! 🎉
