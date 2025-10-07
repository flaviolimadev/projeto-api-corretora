# 🚨 INSTRUÇÕES CRÍTICAS - EASYPANEL

## ⚠️ PROBLEMA IDENTIFICADO

O Easypanel está **FORÇANDO** o uso do Nixpacks automaticamente, mesmo com o Dockerfile presente. 

O erro mostra que está usando:
```
/etc/easypanel/projects/corretora/app/code/.nixpacks/Dockerfile
```

Em vez do nosso:
```
/etc/easypanel/projects/corretora/app/code/Dockerfile
```

## ✅ SOLUÇÃO - CONFIGURAR NO PAINEL DO EASYPANEL

### 1. **Acesse o Easypanel**
- Vá para: https://seu-easypanel.com
- Faça login na sua conta

### 2. **Edite o Serviço**
- Vá para o projeto `corretora`
- Clique no serviço `app`
- Clique em **"Edit"** ou **"Settings"**

### 3. **Configure o Build**

#### Opção A: Builder Type
Procure por uma opção chamada **"Builder Type"** ou **"Build Method"**:
- Selecione: **`Docker`** ou **`Dockerfile`**
- NÃO use: **`Nixpacks`** ou **`Auto`**

#### Opção B: Build Settings
Procure por **"Build Settings"** ou **"Advanced Settings"**:
- **Dockerfile Path**: `Dockerfile` (ou `./Dockerfile`)
- **Build Context**: `.` ou `/` (raiz do projeto)
- **Builder**: `Docker` ou `Dockerfile`

#### Opção C: Configuração via YAML
Se houver opção de configuração via YAML ou JSON:
```yaml
build:
  type: docker
  dockerfile: Dockerfile
  context: .
```

### 4. **Salve e Rebuild**
- Clique em **"Save"** ou **"Update"**
- Clique em **"Rebuild"** ou **"Deploy"**

## 📋 CHECKLIST IMPORTANTE

Antes de fazer o deploy, verifique:

- [ ] Builder Type está como **`Docker`** (NÃO Nixpacks)
- [ ] Dockerfile Path está como **`Dockerfile`**
- [ ] Build Context está como **`.`** (raiz)
- [ ] Port está como **`5000`**
- [ ] Variáveis de ambiente estão configuradas

## 🔧 CONFIGURAÇÕES NECESSÁRIAS

### Build Settings
```
Builder Type: Docker
Dockerfile Path: Dockerfile
Build Context: .
Port: 5000
```

### Environment Variables
```env
DATABASE_URL=postgres://postgres:6b7215f9594dea0d0673@easypainel.ctrlser.com:5435/corretora?sslmode=disable
API_HOST=0.0.0.0
API_PORT=5000
FLASK_ENV=production
SECRET_KEY=your-super-secret-production-key-change-this-in-easypanel
WORKER_ENABLED=True
SYNC_INTERVAL_CATEGORIES=3600
SYNC_INTERVAL_ASSETS=1800
SYNC_INTERVAL_CANDLES=60
SYNC_INTERVAL_CURRENT=1
CACHE_ENABLED=True
CACHE_TTL=300
LOG_LEVEL=INFO
```

## 🎯 ALTERNATIVA - CRIAR NOVO SERVIÇO

Se a edição não funcionar, crie um novo serviço:

1. **Delete o serviço atual** (ou pause)
2. **Crie um novo serviço**:
   - Name: `app`
   - Type: **`Docker`** (NÃO Nixpacks)
   - Repository: seu repositório GitHub
   - Branch: `main`
   - Dockerfile: `Dockerfile`
   - Port: `5000`

3. **Configure as variáveis de ambiente**
4. **Deploy**

## 🔍 COMO VERIFICAR SE ESTÁ CORRETO

Após configurar, antes de fazer o deploy:

1. Verifique se o **Builder Type** está como **`Docker`**
2. Verifique se **NÃO** aparece menção a **Nixpacks**
3. Verifique se o **Dockerfile Path** está correto

## 📸 CAPTURAS DE TELA (ONDE ENCONTRAR)

### No painel do Easypanel, procure por:
- **Settings** → **Build Settings**
- **Advanced** → **Builder Configuration**
- **Deploy** → **Build Method**

### Procure por campos como:
- **Builder Type**
- **Build Method**
- **Dockerfile Path**
- **Build Context**

## 🚨 SE AINDA ASSIM NÃO FUNCIONAR

Se mesmo após configurar o Easypanel ainda usar Nixpacks:

1. **Verifique se há um arquivo `.easypanel` ou `.easypanel.yaml` na raiz**
   - Se houver, delete-o

2. **Verifique se há configuração global do projeto**
   - Vá para Settings do projeto (não do serviço)
   - Procure por configurações de build padrão

3. **Entre em contato com o suporte do Easypanel**
   - Explique que quer usar Dockerfile em vez de Nixpacks
   - Envie o link do seu repositório

## 📞 SUPORTE EASYPANEL

Se precisar de ajuda:
- Documentação: https://easypanel.io/docs
- Discord: https://discord.gg/easypanel
- Email: support@easypanel.io

## ✅ APÓS CONFIGURAR CORRETAMENTE

Você deve ver no log de build:
```
Building with Docker...
Using Dockerfile at: /app/Dockerfile
```

E NÃO deve ver:
```
╔══════════════════════════════ Nixpacks v1.34.1 ══════════════════════════════╗
```

## 🎉 CONCLUSÃO

O problema NÃO está no código, está na **CONFIGURAÇÃO DO EASYPANEL**.

Você DEVE configurar o Easypanel para usar **Docker/Dockerfile** em vez de **Nixpacks**.

🚀 **Configure o Builder Type para Docker e faça o rebuild!**
