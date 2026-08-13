# Sistema de Precificação

Sistema web para cadastro de lojas e produtos e gerenciamento do ciclo de vida de alterações de preço. A implementação preserva a arquitetura existente com **Flask**, **SQLAlchemy**, **SQLite**, **JWT**, **CORS** e frontend em **HTML, CSS e JavaScript vanilla**.

## Requisitos

É necessário ter Python 3.9 ou superior. O frontend pode ser servido por qualquer servidor HTTP estático; o comando `python -m http.server` é suficiente para desenvolvimento.

## Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python seed.py
python main.py
```

A API estará disponível em `http://localhost:5000`. O banco SQLite é criado automaticamente. Para configurar outro banco ou segredo, copie `.env.example` para `.env` e ajuste `DATABASE_URL`, `SECRET_KEY`, `JWT_SECRET_KEY`, `CORS_ORIGINS` e `API_PORT`.

## Frontend

Com o backend em execução, abra outro terminal:

```bash
cd frontend
python3 -m http.server 8080
```

Acesse `http://localhost:8080`. Caso a API esteja em outra URL, defina `window.API_BASE_URL` antes dos scripts do frontend ou altere a configuração padrão em `frontend/js/api.js`.

## Credenciais de desenvolvimento

A carga de demonstração usa `admin@pricetracker.com` com senha `admin123`. Essas credenciais são somente para desenvolvimento e não devem ser utilizadas em produção.

## API principal

| Método | Endpoint | Finalidade |
|---|---|---|
| GET | `/health` | Verificar disponibilidade |
| POST | `/api/auth/login` | Obter JWT |
| GET | `/api/auth/me` | Consultar sessão atual |
| POST | `/api/auth/logout` | Encerrar sessão do cliente |
| GET/POST/PUT/DELETE | `/api/stores` | CRUD de lojas |
| GET/POST/PUT/DELETE | `/api/products` | CRUD de produtos |
| GET/POST/PUT/DELETE | `/api/price-changes` | CRUD de alterações |
| POST | `/api/price-changes/<id>/activate` | `pending` para `active` |
| POST | `/api/price-changes/<id>/execute` | `active` para `executed` e atualiza o produto |
| GET | `/api/dashboard` | Métricas e alterações recentes |

Todas as rotas, exceto `/health` e `/api/auth/login`, exigem `Authorization: Bearer <token>`. Alterações executadas não podem ser editadas ou canceladas. Alterações pendentes ou ativas podem ser canceladas.

## Testes

```bash
cd backend
source .venv/bin/activate
pytest -q
```

Os testes cobrem health check, login válido e inválido, proteção JWT, CRUD de produtos e lojas, filtros, métricas e o fluxo `pending → active → executed`, incluindo a atualização do preço do produto.
