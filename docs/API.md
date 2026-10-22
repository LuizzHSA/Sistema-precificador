# API operacional

A API usa JSON e autenticação `Bearer JWT` em todas as rotas privadas. `POST /api/auth/register` e `POST /api/auth/login` são públicos; o cadastro exige nome, e-mail válido e senha com no mínimo 10 caracteres. O cadastro retorna um token JWT e os dados básicos da conta. Cada conta possui lojas, produtos, alterações de preço, logs e auditoria isolados dos demais usuários.

| Método | Endpoint                     | Descrição                                     |
| ------ | ---------------------------- | --------------------------------------------- |
| POST   | `/api/auth/register`       | Cria conta e inicia sessão                               |
| POST   | `/api/auth/login`          | Autentica uma conta existente                            |
| GET    | `/api/auth/me`             | Retorna a conta autenticada                              |
| POST   | `/api/auth/logout`         | Encerra a sessão no cliente                              |
| GET    | `/health`                    | Liveness sem autenticação                     |
| GET    | `/health/ready`              | Readiness e teste de banco                    |
| GET    | `/metrics`                   | Contadores operacionais                       |
| GET    | `/api/products/<id>/history` | Detalhes do produto e histórico de alterações |
| POST   | `/api/automation/run`        | Processa alterações vencidas                  |
| GET    | `/api/execution-logs`        | Últimas execuções da automação                |
| GET    | `/api/audit-events`          | Eventos de auditoria recentes                 |

Respostas de erro seguem o formato `{ "error": "mensagem" }`. O limite padrão de payload é 1 MiB e o rate limit padrão é de 120 requisições por minuto por endereço, configurável por ambiente.
