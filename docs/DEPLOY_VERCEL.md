# Deploy na Vercel com Services

O projeto usa dois serviços dentro de um único projeto Vercel:

- `frontend`: HTML/CSS/JavaScript estático, público em `/`.
- `backend`: Flask, público em `/api/*`, `/health`, `/health/ready` e `/metrics`.

Não há Service Binding entre frontend e backend porque o frontend roda no navegador e chama a API pela rota pública de mesma origem (`/api`).

## 1. Banco de dados

Não use SQLite como banco de produção na Vercel. O filesystem das Functions não deve ser tratado como armazenamento persistente.

Crie um PostgreSQL externo (por exemplo, via integração de banco disponível na Vercel) e configure a variável:

```
DATABASE_URL=postgresql://USUARIO:SENHA@HOST:5432/BANCO
```

## 2. Variáveis de ambiente obrigatórias

Configure no projeto Vercel, para Production e Preview conforme necessário:

```
FLASK_ENV=production
DEBUG=false
DATABASE_URL=postgresql://...
SECRET_KEY=<segredo forte com pelo menos 32 caracteres>
JWT_SECRET_KEY=<segredo forte diferente>
AUTH_EMAIL=<email de login>
AUTH_PASSWORD_HASH=<hash gerado pelo Werkzeug>
AUTH_NAME=Administrador
LOG_LEVEL=INFO
```

Para gerar o hash da senha localmente:

```powershell
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('SUA_SENHA'))"
```

Como frontend e backend ficam no mesmo domínio, `CORS_ORIGINS` não é necessário para o fluxo normal. Se você também acessar a API por outro domínio, defina essa variável explicitamente.

## 3. Aplicar as migrations

Depois de criar o PostgreSQL e antes de usar a aplicação em produção, aplique a migration existente:

```powershell
cd backend
$env:FLASK_ENV="production"
$env:DATABASE_URL="<sua DATABASE_URL>"
$env:SECRET_KEY="<seu secret>"
$env:JWT_SECRET_KEY="<seu jwt secret>"
$env:AUTH_EMAIL="<seu email>"
$env:AUTH_PASSWORD_HASH="<seu hash>"
python -m flask --app app.main:create_app db upgrade
```

## 4. Testar localmente com Vercel Services

Instale/atualize a CLI:

```
npm install -g vercel@latest
```

Na raiz do repositório:

```
vercel dev -L
```

Teste:

```
http://localhost:3000/
http://localhost:3000/api/auth/login
http://localhost:3000/health
http://localhost:3000/health/ready
http://localhost:3000/metrics
```

## 5. Importar o repositório na Vercel

1. Crie um novo Project na Vercel.
2. Importe `LuizzHSA/Sistema-precificador`.
3. Mantenha o Root Directory do projeto na raiz do repositório.
4. Adicione as variáveis de ambiente.
5. Faça o deploy.

O `vercel.json` define os dois serviços e o roteamento.

## Decisões adotadas

### Serviços

- Nome do serviço do frontend: `frontend`
- Nome do serviço do backend: `backend`

### Rotas públicas

- `frontend`: `/(.*)` como catch-all
- `backend`: `/api/(.*)`
- `backend`: `/health`
- `backend`: `/health/(.*)`
- `backend`: `/metrics`

### Bindings

Nenhum binding foi adicionado.

O frontend atual é estático e executa no navegador. Ele já usa `/api` em produção, portanto a requisição passa pelo roteamento público da Vercel e chega ao Flask no mesmo domínio.
