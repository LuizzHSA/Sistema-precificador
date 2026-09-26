# Sistema Precificador

Aplicação web para **cadastro de lojas e produtos, gerenciamento de alterações de preço e acompanhamento do histórico das operações**.

Este repositório contém a versão apresentada como produto funcional do projeto acadêmico. O objetivo é permitir que outra pessoa compreenda o sistema, execute-o localmente e valide seus principais fluxos a partir das instruções deste documento.

## Objetivo do produto

O Sistema Precificador foi desenvolvido para organizar o gerenciamento de produtos e alterações de preço em uma aplicação web centralizada.

A solução permite cadastrar lojas e produtos, registrar alterações de preço, acompanhar o status dessas alterações e manter um histórico das operações realizadas.

## Tecnologias utilizadas

### Back-end

- Python 3
- Flask
- SQLAlchemy
- Flask-Migrate
- JWT para autenticação
- Pytest para testes automatizados

### Front-end

- HTML5
- CSS3
- JavaScript

### Banco de dados

- SQLite no ambiente local
- PostgreSQL suportado nos testes de integração e preparado para ambiente de produção

### Desenvolvimento e qualidade

- Git
- GitHub
- GitHub Actions
- Testes automatizados
- Cobertura mínima de 70% no pipeline de CI

## Arquitetura simplificada

```text
Usuário
   ↓
Frontend HTML/CSS/JavaScript
   ↓
API Flask
   ↓
Regras da aplicação
   ↓
Banco de dados
```

## Recursos entregues

A versão atual possui os seguintes recursos principais:

- autenticação com JWT;
- login e logout;
- cadastro de lojas;
- consulta de lojas;
- exclusão de lojas;
- cadastro de produtos;
- consulta e busca de produtos;
- edição de produtos;
- exclusão de produtos;
- validação de dados de produtos;
- controle de SKU duplicado;
- criação de alterações de preço;
- filtros de alterações por status, loja e produto;
- ativação de alterações de preço;
- cancelamento de alterações permitidas;
- execução de alterações ativas;
- atualização do preço atual do produto após a execução;
- cálculo da diferença de preço e variação percentual;
- histórico de alterações por produto;
- dashboard com informações operacionais;
- paginação;
- logs de execução;
- eventos de auditoria;
- endpoint de saúde da aplicação;
- endpoint de readiness com verificação do banco;
- métricas operacionais básicas.

## Requisitos para execução local

Para a forma mais simples de execução:

- Windows;
- PowerShell;
- Python 3.9 ou superior;
- Git.

Não é necessário Docker ou PostgreSQL para executar a aplicação localmente.

## Instalação

Clone o repositório:

```powershell
git clone https://github.com/LuizzHSA/Sistema-precificador.git
cd Sistema-precificador
```

Prepare o ambiente do back-end:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
cd ..
```

## Executar o sistema

Na raiz do projeto:

```powershell
.\start.ps1
```

O script:

1. prepara o banco de dados;
2. aplica as migrations;
3. carrega dados de exemplo;
4. inicia a API;
5. disponibiliza o frontend.

Após a inicialização:

- Frontend: http://localhost:8080
- API: http://localhost:5000

### Credenciais locais para demonstração

```text
Email: admin@pricetracker.com
Senha: admin123
```

> As credenciais acima são destinadas exclusivamente ao ambiente local de desenvolvimento/demonstração. Em um ambiente real, as credenciais devem ser definidas por variáveis de ambiente e não expostas no repositório.

## Execução manual

### Back-end

```powershell
cd backend
.\.venv\Scripts\python.exe init_db.py
.\.venv\Scripts\python.exe main.py
```

### Front-end

Em outro terminal:

```powershell
cd frontend
python -m http.server 8080
```

## Configuração

O projeto utiliza SQLite por padrão no ambiente local.

As configurações de banco, autenticação, secrets e demais variáveis estão exemplificadas em:

```text
backend/.env.example
```

Nunca envie secrets reais para o GitHub.

## Como testar

Com o ambiente preparado:

```powershell
.\test.ps1
```

Ou diretamente:

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q
```

## Integração contínua

O projeto possui um pipeline em:

```text
.github/workflows/ci.yml
```

A automação executa:

- instalação das dependências;
- verificação de compilação do código Python;
- testes automatizados do back-end;
- cobertura mínima de 70%;
- geração do relatório de cobertura;
- verificação de sintaxe dos arquivos JavaScript;
- testes de integração utilizando PostgreSQL.

## Principais fluxos para validação

### Fluxo 1 — Acesso ao sistema

1. executar a aplicação;
2. abrir http://localhost:8080;
3. realizar login com as credenciais locais;
4. acessar o dashboard.

**Resultado esperado:** o usuário autenticado acessa a área principal da aplicação.

### Fluxo 2 — Cadastro de loja e produto

1. cadastrar uma loja;
2. cadastrar um produto associado à loja;
3. informar nome, SKU e preço válido;
4. consultar o produto cadastrado.

**Resultado esperado:** os registros são armazenados e aparecem na consulta.

### Fluxo 3 — Alteração de preço

1. selecionar um produto;
2. criar uma alteração de preço;
3. informar o novo preço e a data efetiva;
4. ativar a alteração;
5. executar a alteração quando permitido;
6. consultar novamente o produto.

**Resultado esperado:** o preço atual do produto é atualizado e a alteração é registrada no histórico.

### Fluxo 4 — Situação inválida

Um exemplo de erro que pode ser demonstrado é tentar cadastrar um produto com preço igual a zero.

**Resultado esperado:** a API rejeita a operação com HTTP 400.

Outro cenário possível é cadastrar outro produto com o mesmo SKU na mesma regra de unicidade.

**Resultado esperado:** a API rejeita a duplicidade com HTTP 409.

## Evidências recomendadas para a apresentação

Para a entrega acadêmica, registrar screenshots ou gravações dos seguintes pontos:

1. tela de login ou dashboard;
2. cadastro de uma loja e de um produto;
3. produto aparecendo na listagem;
4. criação de uma alteração de preço;
5. alteração ativada e executada;
6. preço atualizado no produto;
7. histórico da alteração;
8. tentativa de operação inválida;
9. testes automatizados executados com sucesso;
10. página do GitHub mostrando a versão apresentada.

As imagens podem ser colocadas em uma pasta `docs/evidencias/` e depois referenciadas neste README.

## Versão apresentada

A versão acadêmica apresentada está baseada na branch:

```text
main
```

Como evidência de versão, utilize o commit da demonstração. No momento da preparação desta documentação, o último commit funcional identificado era:

```text
fe28ca24d409b42ec074fe53b842dd0776c7857c
Sistema refatorado e finalizado
```

Antes da apresentação final, recomenda-se confirmar se este continua sendo o commit que será demonstrado.

## Problemas conhecidos e limitações

A versão atual possui algumas limitações importantes:

- a execução simplificada está focada em Windows e PowerShell;
- não existe, no repositório atual, um deploy público de produção configurado;
- SQLite é utilizado por padrão no ambiente local;
- a configuração de produção ainda depende da definição da infraestrutura de hospedagem;
- envio real de e-mail depende de configuração SMTP;
- sem configuração SMTP, notificações trabalham em modo de simulação/dry-run;
- o processamento automático de alterações pode ser acionado pelo endpoint operacional, mas um agendador externo permanente depende da infraestrutura escolhida;
- monitoramento externo e alertas de disponibilidade ainda não estão configurados;
- algumas melhorias de infraestrutura, observabilidade e publicação continuam planejadas.

## O que foi atendido nesta versão

- aplicação executável localmente;
- autenticação;
- gerenciamento de lojas;
- gerenciamento de produtos;
- gerenciamento de alterações de preço;
- validações de dados;
- histórico;
- dashboard;
- testes automatizados;
- integração contínua;
- migrations;
- documentação de execução;
- endpoints operacionais.

## O que fica para depois

Itens que podem ser evoluídos em próximas versões:

- publicação em ambiente público;
- ambiente separado de homologação;
- automação de deploy;
- monitoramento externo;
- alertas de indisponibilidade;
- agendamento externo permanente;
- infraestrutura como código;
- containerização, caso passe a gerar valor para o ambiente de publicação;
- melhorias adicionais de segurança, performance e observabilidade.

## Demonstração para o cliente ou usuário final

Roteiro sugerido para uma demonstração curta:

1. apresentar o objetivo do sistema;
2. realizar o login;
3. mostrar o dashboard;
4. cadastrar ou selecionar uma loja;
5. cadastrar um produto;
6. criar uma alteração de preço;
7. ativar e executar a alteração;
8. mostrar o preço atualizado e o histórico;
9. demonstrar uma entrada inválida e a validação do sistema;
10. mostrar os testes automatizados;
11. apresentar as limitações conhecidas e próximos passos.

Esse roteiro demonstra tanto o caminho de sucesso quanto o tratamento de erros.

## Documentação adicional

O repositório possui documentação complementar:

- `docs/API.md` — endpoints operacionais e contrato básico da API;
- `docs/OPERATIONS.md` — operação, backup, monitoramento e rollback;
- `docs/BACKLOG.md` — backlog e evolução do projeto;
- `docs/ROADMAP.md` — planejamento de evolução.

## Estrutura principal

```text
Sistema-precificador/
├── .github/
│   └── workflows/
├── backend/
│   ├── app/
│   ├── migrations/
│   ├── tests/
│   ├── .env.example
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── css/
│   ├── js/
│   └── index.html
├── docs/
├── scripts/
├── start.ps1
├── test.ps1
└── README.md
```

## Equipe

Projeto desenvolvido por:

- Luiz Henrique Lopes de Sá
- Luiz Henrique Barbosa Buzatto
- Raphael Bahia Gonçalves

---

Este README foi organizado para permitir que outra pessoa **compreenda, execute, teste e demonstre** o Sistema Precificador sem depender de conhecimento prévio do projeto.
