# Sistema de Precificação

Sistema web para cadastro de lojas e produtos e gerenciamento do ciclo de vida de alterações de preço. A implementação preserva a arquitetura existente com **Flask**, **SQLAlchemy**, **SQLite**, **JWT**, **CORS** e frontend em **HTML, CSS e JavaScript vanilla**.

## Requisitos

- **Python 3.9 ou superior**
- **Git**
- VS Code ou outro editor de código

O backend usa Flask e o frontend é servido como arquivos estáticos. Não é necessário Node.js para executar o projeto.

---

## 1. Clonar o projeto

```bash
git clone https://github.com/LuizzHSA/Sistema-precificador.git
cd Sistema-precificador
```

Se o projeto já estiver clonado, apenas abra o terminal na pasta raiz `Sistema-precificador`.

---

## 2. Backend

### Windows — PowerShell

Abra um terminal e execute:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python seed.py
python main.py
```

Se o PowerShell bloquear a ativação do ambiente virtual, execute uma vez:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Depois tente novamente:

```powershell
.venv\Scripts\Activate.ps1
```

### Windows — CMD

Se estiver usando o Prompt de Comando em vez do PowerShell:

```cmd
cd backend
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
python seed.py
python main.py
```

### Linux / macOS

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
python3 seed.py
python3 main.py
```

A API estará disponível em:

```text
http://localhost:5000
```

O banco SQLite é criado automaticamente.

### Variáveis de ambiente

Para configurar outro banco ou segredo, copie `.env.example` para `.env` e ajuste:

```text
DATABASE_URL
SECRET_KEY
JWT_SECRET_KEY
CORS_ORIGINS
API_PORT
```

Para desenvolvimento local com SQLite, não é necessário configurar PostgreSQL.

---

## 3. Testar o Backend

Com o backend em execução, abra no navegador:

```text
http://localhost:5000/health
```

Você também pode executar a suíte de testes.

### Windows — PowerShell / CMD

Com o ambiente virtual ativado:

```powershell
cd backend
pytest -q
```

### Linux / macOS

```bash
cd backend
source .venv/bin/activate
pytest -q
```

Os testes cobrem health check, login válido e inválido, proteção JWT, CRUD de produtos e lojas, filtros, métricas e o fluxo `pending → active → executed`, incluindo a atualização do preço do produto.

---

## 4. Frontend

**Não feche o terminal do backend.**

Abra um **segundo terminal** na raiz do projeto.

### Windows / Linux / macOS

```bash
cd frontend
python -m http.server 8080
```

Depois acesse:

```text
http://localhost:8080
```

O frontend utiliza a API em `http://localhost:5000` por padrão. Caso a API esteja em outra URL, defina `window.API_BASE_URL` antes dos scripts do frontend ou altere a configuração padrão em `frontend/js/api.js`.

---

## 5. Fluxo completo de execução

Ao abrir o projeto novamente, o fluxo recomendado é:

### Terminal 1 — Backend

```powershell
cd Sistema-precificador\backend
.venv\Scripts\Activate.ps1
python main.py
```

### Terminal 2 — Frontend

```powershell
cd Sistema-precificador\frontend
python -m http.server 8080
```

Depois abra:

```text
http://localhost:8080
```

> **Importante:** o ambiente virtual `.venv` precisa ter sido criado e as dependências instaladas anteriormente. Se a pasta `.venv` não existir, siga novamente a seção **2. Backend — Windows**.

---

## 6. Credenciais de desenvolvimento

A carga de demonstração usa:

```text
E-mail: admin@pricetracker.com
Senha: admin123
```

Essas credenciais são somente para desenvolvimento e não devem ser utilizadas em produção.

---

## 7. API principal

| Método | Endpoint | Finalidade |
|---|---|---|
| GET | `/health` | Verificar disponibilidade |
| POST | `/api/auth/login` | Obter JWT |
| GET | `/api/auth/me` | Consultar sessão atual |
| POST | `/api/auth/logout` | Encerrar sessão do cliente |
| GET/POST/PUT/DELETE | `/api/stores` | CRUD de lojas |
| GET/POST/PUT/DELETE | `/api/products` | CRUD de produtos |
| GET | `/api/products/<id>/history` | Detalhes e histórico de alterações do produto |
| GET/POST/PUT/DELETE | `/api/price-changes` | CRUD de alterações |
| POST | `/api/price-changes/<id>/activate` | `pending` para `active` |
| POST | `/api/price-changes/<id>/execute` | `active` para `executed` e atualiza o produto |
| GET | `/api/dashboard` | Métricas e alterações recentes |

Todas as rotas, exceto `/health` e `/api/auth/login`, exigem `Authorization: Bearer <token>`. Alterações executadas não podem ser editadas ou canceladas. Alterações pendentes ou ativas podem ser canceladas.

---

## 8. Worker

O worker executa automaticamente alterações `active` cuja data efetiva venceu.

Para executar uma rodada manualmente:

```bash
cd backend
python worker.py --max-retries 3
```

Para execução contínua:

```bash
python worker.py --loop --interval 60
```

O processamento registra logs em `execution_logs`, auditoria em `audit_events` e retry controlado por `MAX_RETRIES`. Notificações por email são opcionais e utilizam SMTP configurado por ambiente; sem SMTP, o comportamento é dry-run no log.

---

## 9. Docker

A execução completa também pode ser feita com Docker Compose.

No Linux/macOS:

```bash
export SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
export JWT_SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
docker compose up -d --build
```

No PowerShell:

```powershell
$env:SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(32))"
$env:JWT_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(32))"
docker compose up -d --build
```

O Compose inicializa PostgreSQL, Redis, API, frontend Nginx e worker.

---

## 10. CI/CD

O workflow `.github/workflows/ci.yml` executa testes com cobertura mínima de 70%, compilação Python, sintaxe JavaScript, validação do Compose e builds das imagens.

---

## 11. Estrutura principal

```text
Sistema-precificador/
├── backend/
│   ├── .venv/              # Ambiente virtual local — não versionar
│   ├── main.py             # Inicialização da API
│   ├── seed.py             # Dados iniciais de desenvolvimento
│   ├── worker.py            # Processamento automático
│   ├── requirements.txt     # Dependências Python
│   └── ...
├── frontend/
│   ├── index.html
│   ├── css/
│   └── js/
├── docs/
├── scripts/
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 12. Solução rápida para problemas comuns

### `python` não é reconhecido

Teste:

```powershell
py --version
```

Se `py` funcionar, substitua `python` por `py` nos comandos de criação e instalação do ambiente virtual.

### `.venv\Scripts\Activate.ps1` não é reconhecido

Verifique se você está dentro da pasta `backend` e se a pasta `.venv` existe:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### `pip install -r requirements.txt` falhou

Certifique-se de que o ambiente virtual está ativado:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Porta 5000 ocupada

O backend usa a porta `5000` por padrão. Feche o processo que está usando a porta ou configure `API_PORT` no `.env`.

### Porta 8080 ocupada

Escolha outra porta para o frontend:

```powershell
python -m http.server 8081
```

Nesse caso, acesse:

```text
http://localhost:8081
```

### O frontend abre, mas não consegue fazer login

Verifique se o backend está rodando em:

```text
http://localhost:5000/health
```

Depois confirme se o frontend está apontando para a URL correta da API em `frontend/js/api.js`.

---

## 13. Documentação operacional

Consulte:

- `docs/OPERATIONS.md` — operação, monitoramento e rollback
- `docs/API.md` — documentação dos endpoints

Backups podem ser feitos com `scripts/backup.sh`, que suporta SQLite e PostgreSQL e aplica retenção configurável por `RETENTION_DAYS`.
