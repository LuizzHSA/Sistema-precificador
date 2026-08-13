# 📑 Índice de Documentação & Arquivos

> Sistema de Monitoramento de Alterações de Preço  
> Data: 15/04/2026 | Status: 🟡 Em Progresso

---

## 📊 Documentação Principal

### 1. **[ROADMAP.md](./ROADMAP.md)** - Plano Completo do Projeto
- 6 fases de desenvolvimento (Fundação → Deployment)
- 18+ sprints planejadas
- Timeline até Abril 2026
- **Última Atualização**: 15/04/2026

### 2. **[SPRINT_1_KANBAN.md](./SPRINT_1_KANBAN.md)** ⭐ **NOVO**
- Status real-time da Sprint 1 (15-19/04)
- Kanban board com 15 tarefas
- Métricas: 66% concluído, 10/15 tarefas done
- Próximos passos para iniciar o sistema
- **Status**: 🟡 QUASE CONCLUÍDO

### 3. **[README.md](./README.md)** - Visão Geral & Quick Start
- Tecnologias utilizadas
- Como fazer setup local
- Estrutura do projeto
- Credenciais padrão para teste
- **Acesso**: Início Rápido em 5 minutos

### 4. **[docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)** - Arquitetura Técnica
- Diagrama da arquitetura (Frontend → Backend → Database)
- Stack tecnológico detalhado
- Estrutura de pastas backend & frontend
- Fluxo de dados (autenticação, alterações de preço)
- Padrões de design utilizados

---

## 📁 Estrutura de Arquivos do Projeto

```
sistema-precificador/
├── 📊 [ROADMAP.md]                    # Plano 6 fases (18+ sprints)
├── 📋 [SPRINT_1_KANBAN.md]            # ⭐ NEW - Status Sprint 1
├── 📖 [README.md]                     # Setup & Quick start
├── 📌 [.gitignore]                    # Git ignore rules
├── 🔧 [setup.py]                      # Setup script automático
├── 🎨 [kanban.mmd]                    # Diagrama Mermaid Kanban
│
├── 💻 backend/
│   ├── venv/                          # Virtual environment (Python 3.13)
│   ├── app/
│   │   ├── __init__.py                # Extensions: SQLAlchemy, JWT
│   │   ├── main.py                    # Flask app factory
│   │   ├── config.py                  # Dev/Prod/Test configs
│   │   ├── models/
│   │   │   └── __init__.py            # Store, Product, PriceChange
│   │   ├── routes/
│   │   │   ├── auth.py                # Login, /me, logout
│   │   │   └── price_changes.py       # CRUD price changes
│   │   └── utils/
│   │       └── decorators.py          # Error handling, JWT
│   ├── tests/
│   │   ├── conftest.py                # Pytest fixtures
│   │   ├── test_auth.py               # Auth tests
│   │   └── test_price_changes.py      # Price tests
│   ├── requirements.txt               # 10 dependências (Flask, SQLAlchemy, etc)
│   ├── .env.example                   # Variáveis de ambiente template
│   ├── main.py                        # Entry point (python main.py)
│   ├── init_db.py                     # Cria tabelas no banco
│   └── seed.py                        # Popula dados de amostra
│
├── 🎨 frontend/
│   ├── index.html                     # SPA shell with sidebar + modal
│   ├── css/
│   │   ├── style.css                  # Layout (400+ lines, variáveis CSS)
│   │   └── components.css             # Components (500+ lines, buttons, cards)
│   ├── js/
│   │   ├── app.js                     # Router + initialization
│   │   ├── api.js                     # HTTP client with JWT
│   │   ├── store.js                   # Event-driven state management
│   │   ├── pages/
│   │   │   ├── dashboard.js           # KPI dashboard
│   │   │   ├── price-changes.js       # Price changes table
│   │   │   ├── products.js            # Products page (placeholder)
│   │   │   └── stores.js              # Stores page (placeholder)
│   │   └── components/
│   │       ├── modal.js               # Modal dialogs
│   │       └── form.js                # Form helpers
│   └── assets/                        # Imagens / Ícones (futuro)
│
└── 📚 docs/
    └── ARCHITECTURE.md                # Arquitetura técnica
```

---

## 🚀 Como Usar Este Índice

### Para **Desenvolvedores** 👨‍💻
1. Leia [README.md](./README.md) - Setup em 5 minutos
2. Consulte [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) - Arquitetura
3. Acompanhe [SPRINT_1_KANBAN.md](./SPRINT_1_KANBAN.md) - Status da sprint

### Para **Project Manager** 📊
1. Veja [ROADMAP.md](./ROADMAP.md) - Plano geral (6 fases)
2. Acompanhe [SPRINT_1_KANBAN.md](./SPRINT_1_KANBAN.md) - Progresso atual
3. Métricas: 66% Sprint 1, 10/15 tarefas concluídas

### Para **Stakeholders** 👔
1. [README.md](./README.md) - Visão rápida (tecnologias, objetivo)
2. [SPRINT_1_KANBAN.md](./SPRINT_1_KANBAN.md) - Status e timeline
3. Banco dados: ✅ 2 lojas, 3 produtos, 3 alterações de teste

---

## ✅ Checklist de Setup

- [x] Estrutura do projeto criada
- [x] Backend (Flask) com modelos
- [x] Frontend (HTML/CSS/JS) SPA
- [x] Banco de dados SQLite 
- [x] Autenticação JWT
- [x] API endpoints (auth + price-changes)
- [x] Dados de amostra (seed)
- [x] Documentação básica
- [x] **Kanban Sprint 1** ⭐ NEW
- [ ] Sistema rodando localmente (next: `python main.py`)
- [ ] Testes automatizados
- [ ] Deploy em produção

---

## 🔧 Comandos Rápidos

```bash
# Setup inicial (uma vez)
python setup.py

# Backend (Terminal 1)
cd backend
source venv/bin/activate  # ou venv\Scripts\activate
python main.py
# → http://localhost:5000

# Frontend (Terminal 2)
cd frontend
python -m http.server 8080
# → http://localhost:8080

# Dados de Teste
# Email: admin@pricetracker.com
# Senha: admin123

# Ver status banco
cd backend
python init_db.py
python seed.py
```

---

## 📈 Métricas Atuais

| Métrica | Valor |
|---------|-------|
| **Sprint 1 (%)** | 66% ✅ |
| **Tarefas Concluídas** | 10/15 |
| **Linhas Backend** | ~1,200 |
| **Linhas Frontend** | ~600 |
| **Dependências** | 10 |
| **Tabelas BD** | 3 (stores, products, price_changes) |
| **Registros Teste** | 8 (2 + 3 + 3) |

---

## 📞 Links Importantes

| Documento | Propósito | Público |
|-----------|-----------|---------|
| [ROADMAP.md](./ROADMAP.md) | Plano completo | Todos |
| [SPRINT_1_KANBAN.md](./SPRINT_1_KANBAN.md) | Status Sprint 1 | Dev Team |
| [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) | Detalhes técnicos | Developers |
| [README.md](./README.md) | Setup & overview | Todos |
| [kanban.mmd](./kanban.mmd) | Diagrama visual Mermaid | Todos |

---

## 🎯 Próximas Ações (Prioridade)

1. **CRÍTICO** 🔴: Iniciar backend com `python main.py`
2. **CRÍTICO** 🔴: Iniciar frontend com `python -m http.server 8080`
3. **ALTA** 🟠: Testar login (admin@pricetracker.com / admin123)
4. **ALTA** 🟠: Verificar API endpoints (GET /health)
5. **MÉDIA** 🟡: Documentação final (README + QUICKSTART)
6. **MÉDIA** 🟡: Unit tests automation
7. **BAIXA** 🟢: Sprint 1 retrospective (19/04)

---

## 📅 Timeline Sprint 1

```
15/04 (MON) → Setup + Backend Models + Frontend HTML/CSS ✅
16/04 (TUE) → Database + API Endpoints ✅
17/04 (WED) → JWT Auth + Seed Data ✅
18/04 (THU) → Integration Testing 🔄
19/04 (FRI) → Documentation + Code Review ⏳
```

**Sprint 1 Objetivo**: Sistema rodando localmente com login funcional 🎯

---

**Última Atualização**: 2026-04-15 22:30 UTC  
**Próxima Sincronização**: 2026-04-16 09:00 UTC  
**Responsável**: Tech Lead / Dev Team
