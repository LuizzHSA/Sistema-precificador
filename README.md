<<<<<<< HEAD
commit 1
so para ter commiti aqui
=======
# Sistema de Monitoramento de Alterações de Preço

Sistema web simples para monitorar e gerenciar alterações de preços de produtos.

## Tecnologias

- **Backend**: Python 3.9+ + Flask
- **Frontend**: HTML5 + CSS3 + JavaScript ES6 (vanilla, sem frameworks)
- **Banco de Dados**: SQLite
- **Requirements**: requirements.txt com 10 dependências mínimas

## Estrutura do Projeto

````
sistema-precificador/
├── backend/                    # API Python Flask
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # Aplicação principal
│   │   ├── config.py          # Configurações
│   │   ├── models/            # Modelos de banco de dados
│   │   │   ├── __init__.py
│   │   │   ├── price_change.py
│   │   │   └── store.py
│   │   ├── routes/            # Rotas da API
│   │   │   ├── __init__.py
│   │   │   ├── price_changes.py
│   │   │   └── auth.py
│   │   ├── services/          # Lógica de negócio
│   │   │   ├── __init__.py
│   │   │   ├── price_service.py
│   │   │   └── notification_service.py
│   │   ├── utils/             # Utilitários
│   │   │   ├── __init__.py
│   │   │   └── decorators.py
│   │   ├── tests/                 # Testes
│   ├── requirements.txt       # Dependências
│   ├── .env.example          # Variáveis de ambiente
│   ├── init_db.py            # Inicializa banco de dados
│   └── seed.py               # Popula dados de amostra
│
├── frontend/                   # Interface web
│   ├── index.html            # Single Page Application
│   ├── css/
│   │   ├── style.css         # Estilos globais (layout, responsivo)
│   │   └── components.css    # Componentes reutilizáveis
│   ├── js/
│   │   ├── app.js            # Router e inicialização
│   │   ├── api.js            # Cliente HTTP com JWT
│   │   ├── store.js          # Gerenciamento de estado
│   │   ├── pages/            # Componentes de página
│   │   │   ├── dashboard.js
│   │   │   ├── price-changes.js
│   │   │   ├── products.js
│   │   │   └── stores.js
│   │   └── components/       # Componentes reutilizáveis
│   │       ├── modal.js
│   │       └── form.js
│   └── assets/               # Imagens e ícones
│
├── .github/                   # GitHub Actions (opcional)
├── .gitignore
├── README.md
├── ROADMAP.md                # Plano de desenvolvimento (6 fases)
└── docs/                     # Documentação
    └── ARCHITECTURE.md

## Início Rápido

### Requisitos
- Python 3.9+ (com pip)
- Navegador moderno (Chrome, Firefox, Safari, Edge)

### Setup Local

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app/main.py
````

#### Frontend

Basta abrir `frontend/index.html` no navegador ou servir com:

````bash
cd frontend
Servir em outro terminal com:

```bash
cd frontend
python -m http.server 8080
````

Acesse `http://localhost:8080` no navegador.

## Variáveis de Ambiente

Copie `backend/.env.example` para `backend/.env` ou use as configurações padrão:

```env
FLASK_ENV=development
DATABASE_URL=sqlite:///price_tracker.db
SECRET_KEY=dev-secret-key
JWT_SECRET=jwt-secret-key
API_PORT=5000
DEBUG=True
```

## Credenciais Padrão

Para login no sistema (dados de amostra):

- Email: `admin@pricetracker.com`
- Senha: `admin123
>>>>>>> ee44c56 (sprint 1)
