# Sistema de Precificacao

Aplicacao web para cadastro de lojas e produtos e gerenciamento de alteracoes de preco.

## Abrir facilmente no Windows

1. Abra o PowerShell na pasta do projeto.
2. Execute uma vez para preparar o ambiente:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
cd ..
```

3. Inicie o projeto:

```powershell
.\start.ps1
```

O navegador sera aberto em `http://localhost:8080`.

Credenciais locais:

```text
Email: admin@pricetracker.com
Senha: admin123
```

O script inicia a API em `http://localhost:5000`, aplica as migrations, carrega dados de exemplo e serve o frontend em `http://localhost:8080`.

## Testar

Com o ambiente preparado, execute:

```powershell
.\test.ps1
```

Ou diretamente:

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q
```

## Execucao manual

Backend:

```powershell
cd backend
.\.venv\Scripts\python.exe init_db.py
.\.venv\Scripts\python.exe main.py
```

Frontend, em outro terminal:

```powershell
cd frontend
python -m http.server 8080
```

A API usa SQLite por padrao. Para configurar banco, secrets e credenciais, use as variaveis em `backend/.env.example`.

## Requisitos

- Windows PowerShell
- Python 3.9 ou superior
- Git

Nao e necessario Node.js, Docker ou PostgreSQL para executar localmente.
