# Análise de Projeto — Heurísticas (Fase 1)

## 1. Detecção de linguagem

| Sinal | Linguagem |
|-------|-----------|
| `*.py`, `requirements.txt`, `pyproject.toml` | Python |
| `*.js`, `*.ts`, `package.json` | JavaScript/TypeScript |
| `go.mod`, `*.go` | Go |
| `pom.xml`, `build.gradle`, `*.java` | Java |

Conte arquivos `.py` / `.js` / `.ts` na raiz e em `src/`, excluindo testes se o usuário não pedir cobertura de testes.

## 2. Detecção de framework

### Python

| Arquivo / import | Framework |
|------------------|-----------|
| `from flask import` ou `import flask` | Flask |
| `from fastapi import` | FastAPI |
| `django` em requirements | Django |

Versão: leia `requirements.txt` ou `pip show` no lockfile.

### Node.js

| Dependência package.json | Framework |
|--------------------------|-----------|
| `express` | Express |
| `fastify` | Fastify |
| `koa` | Koa |

## 3. Dependências principais

- **Python:** primeiras linhas de `requirements.txt` (framework, ORM, cors, auth).
- **Node:** `dependencies` em `package.json` (exclua devDependencies na listagem resumida).

## 4. Banco de dados

| Sinal | Banco |
|-------|-------|
| `sqlite3`, `*.db`, `loja.db` | SQLite |
| `mongoose`, `mongodb` | MongoDB |
| `pg`, `sequelize` + postgres | PostgreSQL |
| `CREATE TABLE` em código | Schema embutido (documentar nomes das tabelas) |

Liste tabelas encontradas em migrations, `database.py`, ou scripts SQL inline.

## 5. Domínio da aplicação

Inferir pelo vocabulário de rotas, modelos e tabelas:

| Padrões no código | Domínio |
|-------------------|---------|
| `produto`, `pedido`, `usuario`, `carrinho` | E-commerce API |
| `curso`, `matricula`, `checkout`, `payment` | LMS / E-learning com checkout |
| `task`, `todo`, `categoria`, `assignee` | Task Manager API |

Descreva em uma frase: entidades principais + tipo de API (REST).

## 6. Mapeamento de arquitetura

Classifique a organização atual:

| Padrão observado | Classificação |
|------------------|---------------|
| 1–4 arquivos na raiz com SQL + rotas + lógica misturados | Monolítica — sem separação de camadas |
| `models/`, `routes/`, `services/` presentes mas controllers ausentes ou lógica em routes | Parcialmente organizada — camadas incompletas |
| `controllers/`, `models/`, `routes/` separados | MVC parcial ou completo |
| Classe única `AppManager.js` com DB + rotas + regras | God Object centralizado |

Documente:
- Onde ficam as **rotas** (app principal, Blueprint, Router Express).
- Onde ficam **queries SQL** ou acesso a dados.
- Onde ficam **regras de negócio** (cálculos, validações complexas, notificações).

## 7. Inventário de arquivos

Conte apenas código de aplicação:
- Incluir: `app.py`, `controllers.py`, `models.py`, `src/**/*.js`, `routes/*.py`, `services/*.py`
- Excluir: `README.md`, `api.http`, `seed.py` (mencionar separadamente se existir), configs de IDE

## 8. Endpoints

Extraia rotas de:
- Flask: `app.add_url_rule`, `@app.route`, Blueprints
- Express: `app.get/post`, `router.*`, métodos em `setupRoutes`

Liste método HTTP + path para validação na Fase 3.

## 9. Checklist rápido Fase 1

- [ ] Linguagem identificada com evidência
- [ ] Framework + versão (se disponível)
- [ ] Domínio descrito corretamente
- [ ] Contagem de arquivos condiz com o disco
- [ ] Tabelas/schema documentados
- [ ] Resumo impresso no template PHASE 1
