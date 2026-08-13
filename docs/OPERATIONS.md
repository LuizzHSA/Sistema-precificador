# Operação e produção

## Arquitetura

A aplicação é composta por uma API Flask servida por Gunicorn, um frontend estático servido por Nginx, PostgreSQL para persistência, Redis reservado para evolução de filas e um worker contínuo que processa alterações vencidas. O worker executa `backend/worker.py --loop --interval 60` e pode ser ajustado por `WORKER_INTERVAL_SECONDS`.

## Execução com Docker Compose

Copie as variáveis de ambiente, gere segredos fortes e suba os serviços:

```bash
cp backend/.env.example .env
export SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
export JWT_SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
docker compose up -d --build
```

O frontend ficará em `http://localhost:8080`, a API em `http://localhost:5000` e o endpoint operacional em `/health/ready`. Em produção, coloque um proxy TLS gerenciado na frente do Nginx ou utilize um ingress com certificado automático; os containers não devem ser expostos diretamente à internet sem HTTPS.

## Automação e retries

Alterações com status `active` e `effective_date` vencida são executadas uma única vez por ciclo. Cada execução cria um registro em `execution_logs` e um evento em `audit_events`. Em caso de falha, `retry_count` é incrementado até `MAX_RETRIES`. O endpoint autenticado `POST /api/automation/run` permite execução manual e o `GET /api/execution-logs` permite inspeção.

## Email

Sem `SMTP_HOST`, a aplicação não envia email: registra a notificação como dry-run. Para ativar envio, configure `NOTIFICATION_EMAIL`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_FROM` e `SMTP_TLS`. O template padrão inclui produto, loja, status e valores da alteração.

## Backup e restauração

O script `scripts/backup.sh` suporta SQLite e PostgreSQL:

```bash
DATABASE_URL="postgresql://usuario:senha@host:5432/price_tracker" BACKUP_DIR=/var/backups/price-tracker ./scripts/backup.sh
SQLITE_PATH=backend/instance/price_tracker.db BACKUP_DIR=./backups ./scripts/backup.sh
```

Use `pg_restore` para dumps PostgreSQL e `sqlite3 arquivo.db ".restore 'backup.sqlite'"` para SQLite. Recomenda-se agendar o script diariamente, manter retenção mínima de 14 dias e testar restaurações periodicamente em ambiente separado.

## CI/CD

O workflow `.github/workflows/ci.yml` executa compilação Python, testes com cobertura mínima de 70%, verificação de sintaxe JavaScript, validação do Compose e builds das imagens backend e frontend. Um deploy real em staging ou produção exige credenciais e um destino de hospedagem configurados como secrets do repositório; o pipeline não inventa credenciais nem publica automaticamente sem esses secrets.

## Monitoramento

Use `/health` para liveness, `/health/ready` para verificar conexão com o banco e `/metrics` para métricas agregadas. Os logs são emitidos em stdout no formato compatível com coletores de container. Alertas recomendados: readiness diferente de 200, crescimento de `execution_logs` com status `failed`, HTTP 5xx e worker sem processamento por período superior ao intervalo configurado.

## Rollback

Imagens devem ser identificadas pelo SHA do commit. Para rollback, pare a versão atual, suba a imagem anterior, valide `/health/ready` e confira a consistência do banco. Alterações de schema devem ser compatíveis com a versão anterior; antes de qualquer migração destrutiva, execute `scripts/backup.sh`.
