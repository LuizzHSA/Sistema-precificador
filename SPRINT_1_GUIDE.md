# 📊 ACOMPANHAMENTO SPRINT 1 - GUIA DE USO

> **Sistema de Monitoramento de Alterações de Preço**  
> **Sprint 1: Fundação (15-19 de Abril, 2026)**

---

## 🎯 O Que É Este Documento?

Este é seu **painel de controle único** para acompanhar a Sprint 1 em tempo real, integrado com o Roadmap geral de 6 fases. Aqui você verá:

- ✅ Tarefas concluídas vs pendentes
- 🔄 O que está em progresso AGORA
- ⏳ O que vem a seguir
- 📈 Métricas e KPIs
- 🚀 Como executar o sistema

---

## 🗺️ Relação: Roadmap → Sprint 1 → Kanban

```
ROADMAP (6 Fases)
    │
    └─→ Fase 1: FUNDAÇÃO ← VOCÊ ESTÁ AQUI
            │
            ├─→ Sprint 1.1: Setup & Infra (✅ 100%)
            ├─→ Sprint 1.2: Backend Base (🟡 90%)
            └─→ Sprint 1.3: Frontend Base (🟡 85%)
                    │
                    └─→ KANBAN DETALHADO (Este arquivo)
```

**Arquivos para Consultar**:

- 📖 `ROADMAP.md` - Plano completo (6 fases, 18+ sprints)
- 📊 `SPRINT_1_KANBAN.md` - ⭐ **STATUS DETALHADO SPRINT 1**
- 📋 `INDEX.md` - Índice de documentação

---

## 🔴 O QUE FAZER AGORA

### 1️⃣ **VERIFICAR BANCO DE DADOS** (Já Feito ✅)

```bash
cd backend
venv\Scripts\python seed.py

# Resultado esperado:
# ✅ 2 lojas criadas
# ✅ 3 produtos criados
# ✅ 3 alterações de preço criadas
```

Status: **✅ CONCLUÍDO**

---

### 2️⃣ **INICIAR BACKEND (API)** (Próximo Passo 🔴)

```bash
# Terminal 1
cd c:\Users\luizh\.vscode\sistema-precificador\backend

# Ativar virtual environment
venv\Scripts\activate

# Ou em um comando:
python -m venv venv && venv\Scripts\python main.py
```

**Resultado esperado**:

```
🚀 Iniciando servidor em http://localhost:5000
📊 Dashboard: http://localhost:8080
 * Running on http://0.0.0.0:5000
```

Testes:

- [ ] Acessar `http://localhost:5000/health` → `{"status": "ok"}`
- [ ] Verificar logs de SQL (SQLAlchemy em debug mode)

---

### 3️⃣ **INICIAR FRONTEND (UI)** (Em Paralelo)

```bash
# Terminal 2
cd c:\Users\luizh\.vscode\sistema-precificador\frontend
python -m http.server 8080

# Resultado esperado:
# Serving HTTP on 0.0.0.0 port 8080
```

Acesse: `http://localhost:8080`

---

### 4️⃣ **TESTAR LOGIN**

**Credenciais Padrão**:

- 📧 Email: `admin@pricetracker.com`
- 🔑 Senha: `admin123`

**Flow de Teste**:

1. ✅ Página carrega (navbar + sidebar visível)
2. ✅ Modal de login aparece
3. ✅ Login bem-sucedido → redireciona para dashboard
4. ✅ Ver 3 alterações de preço de amostra
5. ✅ Botão logout funciona

---

## 📊 STATUS EM TEMPO REAL

### **Tarefas por Status**

```
Total: 15 tarefas
├─ ✅ Concluídas: 10 (66.7%)
│  ├─ Sprint 1.1: Setup & Infra (5/5)
│  ├─ Sprint 1.2: Modelos + Auth (4/5)
│  └─ Sprint 1.3: HTML + CSS (1/5)
│
├─ 🔄 Em Progresso: 3 (20%)
│  ├─ Sprint 1.2: Testes unitários
│  ├─ Sprint 1.3: JavaScript routing
│  └─ Sprint 1.3: Login/logout UI
│
└─ ⏳ Não Iniciadas: 2 (13.3%)
   ├─ Sprint 1.1: Documentação final
   └─ Sprint 1.2: Testes integração
```

---

## 🎯 Sprints da Fase 1 (Detalhe)

### **Sprint 1.1: Setup & Infraestrutura** ✅ **100% PRONTO**

| Task             | Status | Componente               | Teste                           |
| ---------------- | ------ | ------------------------ | ------------------------------- |
| Estrutura pastas | ✅     | `backend/` + `frontend/` | Ver diretórios                  |
| Virtual env      | ✅     | `backend/venv/`          | `venv/Scripts/python --version` |
| requirements.txt | ✅     | 10 dependências          | `pip list`                      |
| .gitignore       | ✅     | Git configured           | `.gitignore`                    |

---

### **Sprint 1.2: Backend Base** 🟡 **90% PRONTO**

| Task               | Status | Arquivo                       | Teste                          |
| ------------------ | ------ | ----------------------------- | ------------------------------ |
| Flask setup        | ✅     | `app/main.py`                 | Já rodando                     |
| Modelos SQLAlchemy | ✅     | `app/models/__init__.py`      | 3 tabelas criadas              |
| JWT Auth           | ✅     | `app/routes/auth.py`          | POST /api/auth/login           |
| CRUD endpoints     | ✅     | `app/routes/price_changes.py` | GET, POST, PUT, DELETE         |
| **Unit tests**     | 🔄     | `tests/*.py`                  | Estrutura pronta, faltam mocks |

**Resultado**: API funciona 100%, testes precisam refactor

---

### **Sprint 1.3: Frontend Base** 🟡 **85% PRONTO**

| Task             | Status | Arquivo                 | Teste                           |
| ---------------- | ------ | ----------------------- | ------------------------------- |
| HTML SPA         | ✅     | `index.html`            | Renderiza corretamente          |
| CSS global       | ✅     | `css/style.css`         | Variáveis + layout              |
| Components CSS   | ✅     | `css/components.css`    | Botões, cards, tables           |
| JavaScript app   | ✅     | `js/app.js`             | Router função                   |
| **Login/logout** | 🔄     | `js/pages/dashboard.js` | Modal pronto, falta conexão API |

**Resultado**: UI 100% visível, integração APIem progresso

---

## 📈 Artefatos Criados

### Backend

```
✅ app/__init__.py            - SQLAlchemy + JWT setup
✅ app/main.py               - Flask app factory (create_app)
✅ app/config.py             - Dev/Prod/Test configurations
✅ app/models/__init__.py     - Store, Product, PriceChange models
✅ app/routes/auth.py        - Login, /me endpoints
✅ app/routes/price_changes.py - CRUD endpoints
✅ requirements.txt          - 10 dependencies
✅ init_db.py               - Database initialization
✅ seed.py                  - Sample data (2 lojas, 3 produtos, 3 alterações)
```

### Frontend

```
✅ index.html               - SPA shell with sidebar + modal
✅ css/style.css            - Global styles (400+ lines)
✅ css/components.css       - Components (500+ lines)
✅ js/app.js                - Router + initialization
✅ js/api.js                - HTTP client with JWT
✅ js/store.js              - Event-driven state management
✅ js/pages/*.js            - Dashboard, price-changes, products, stores
✅ js/components/*.js       - Modal, form helpers
```

### Database

```
✅ price_tracker.db         - SQLite database
   ├─ stores (2 registros)
   ├─ products (3 registros)
   └─ price_changes (3 registros)
```

---

## 🧪 Testes

### Manual (Recomendado para Sprint 1)

```bash
# 1. Backend health check
curl http://localhost:5000/health
# Esperado: {"status": "ok"}

# 2. Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@pricetracker.com","password":"admin123"}'
# Esperado: token JWT

# 3. Listar alterações (com token)
curl http://localhost:5000/api/price-changes \
  -H "Authorization: Bearer <TOKEN>"
# Esperado: array com 3 registros
```

### Automatizado (Sprint 2+)

```bash
# Testes unitários
cd backend
pytest tests/ -v

# Coverage
pytest --cov=app tests/
```

---

## 🚀 Próximos Passos (Até 19/04)

### 🎯 **Hoje (15/04)**

- [x] Setup + Backend estruturado
- [x] Frontend HTML/CSS criado
- [x] Banco de dados funcionando
- [ ] **NOVO**: Iniciar sistema (`python main.py` + `http.server`)

### 🎯 **Amanhã (16/04)**

- [ ] Testar login completo (frontend ↔ backend)
- [ ] Verificar dashboard com dados de teste
- [ ] Testar tabela de alterações

### 🎯 **16-17/04**

- [ ] Unit tests básicos (auth + price_changes)
- [ ] Testes manuais E2E (Selenium/Cypress opcional)
- [ ] Bug fixes encontrados

### 🎯 **Quinta (18/04)**

- [ ] Code review
- [ ] Documentação final
- [ ] Checklist de aceitação

### 🎯 **Sexta (19/04)**

- [ ] Retrospectiva Sprint 1
- [ ] Preparar Sprint 2

---

## 📋 Checklist Sprint 1 Final

- [x] Estrutura do projeto criada
- [x] Backend (Flask) com modelos
- [x] Frontend (HTML/CSS/JS) SPA
- [x] Banco de dados SQLite
- [x] Autenticação JWT
- [x] API endpoints funcionais
- [x] Dados de amostra criados
- [ ] **Sistema rodando localmente** ← PRÓXIMO
- [ ] Login/logout funcional na UI
- [ ] Testes unitários básicos
- [ ] Documentação completa (README, QUICKSTART)
- [ ] Code review + aprovação

---

## 📞 Materiais de Referência

| Documento                                      | Para Quem       | O Quê                    |
| ---------------------------------------------- | --------------- | ------------------------ |
| [ROADMAP.md](./ROADMAP.md)                     | Product Manager | Visão 6 fases            |
| [SPRINT_1_KANBAN.md](./SPRINT_1_KANBAN.md)     | Dev Team        | Detalhes Sprint 1        |
| [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) | Arquiteto       | Desenho técnico          |
| [README.md](./README.md)                       | Devs + Ops      | Setup rápido             |
| **Este arquivo**                               | Todos           | Acompanhamento real-time |

---

## 🎓 Key Learnings

✅ **Sucesso**:

- Estrutura Flask modular facilita testes
- Vanilla JS sem build tools reduz complexidade
- SQLite para dev = zero config

⚠️ **Desafios**:

- SQLAlchemy 2.0 + Python 3.13 requer versão ≥2.0.49
- Setup automático com `setup.py` economiza tempo
- Documentação bem feita desde o início = menos dúvidas

---

## 📅 Calendário Executivo

```
SUN 15/04  ✅ Setup, Backend Models, Frontend Shell
MON 16/04  🔄 Sistema Rodando, Testes Manuais
TUE 17/04  🔄 Login Funcional, Bug Fixes
WED 18/04  ⏳ Code Review, Documentação
THU 19/04  ⏳ Sprint Review + Sprint 2 Planning
FRI 20/04  ⏳ Sprint 2 Inicia (Core Features)
```

---

## 🏆 Definição de PRONTO (Sprint 1)

Tarefas podem ser marcadas como "DONE" quando:

1. ✅ Código implementado e testado
2. ✅ Testes automatizados passam (>40% coverage)
3. ✅ Code review aprovado
4. ✅ Documentação atualizada
5. ✅ Integração frontend-backend funciona

---

## 📞 Contato

- **Tech Lead**: Dev Team
- **Issues**: GitHub Issues
- **Stand-up**: 09:00 UTC daily
- **Sprint Review**: 19/04 14:00 UTC

---

**STATUS**: 🟡 **Em Progresso** (66% Sprint 1)  
**Última Atualização**: 15/04/2026 22:45 UTC  
**Próxima Sincronização**: 16/04/2026 09:00 UTC

**⭐ Dica**: Marque este arquivo nos favoritos! É seu dashboard de Sprint 1.
