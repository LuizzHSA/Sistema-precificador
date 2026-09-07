# API operacional

A API usa JSON e autenticação `Bearer JWT` em todas as rotas privadas.

| Método | Endpoint                     | Descrição                                     |
| ------ | ---------------------------- | --------------------------------------------- |
| GET    | `/health`                    | Liveness sem autenticação                     |
| GET    | `/health/ready`              | Readiness e teste de banco                    |
| GET    | `/metrics`                   | Contadores operacionais                       |
| GET    | `/api/products/<id>/history` | Detalhes do produto e histórico de alterações |
| POST   | `/api/automation/run`        | Processa alterações vencidas                  |
| GET    | `/api/execution-logs`        | Últimas execuções da automação                |
| GET    | `/api/audit-events`          | Eventos de auditoria recentes                 |

Respostas de erro seguem o formato `{ "error": "mensagem" }`. O limite padrão de payload é 1 MiB e o rate limit padrão é de 120 requisições por minuto por endereço, configurável por ambiente.
