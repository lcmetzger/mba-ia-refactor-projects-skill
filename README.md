# Desafio: Skill refactor-arch

Repositório do desafio MBA IA. Contém a skill `refactor-arch` para analisar, auditar e refatorar backends legados para o padrão MVC, com workflow em três fases e persistência de relatórios em `reports/`.

**Ferramenta:** [Gemini CLI](https://geminicli.com/docs/cli/creating-skills/)  
**Path da skill:** `.agents/skills/refactor-arch/` (convenção Gemini CLI, equivalente a `.gemini/skills/`)

Enunciado do desafio: [ENUNCIADO_DESAFIO.md](ENUNCIADO_DESAFIO.md)

## Estrutura do repositório

```
mba-ia-refactor-projects-skill/
├── README.md
├── ENUNCIADO_DESAFIO.md
├── reports/
│   ├── audit-project-1.md
│   ├── audit-project-2.md
│   └── audit-project-3.md
├── code-smells-project/
│   └── .agents/skills/refactor-arch/
├── ecommerce-api-legacy/
│   └── .agents/skills/refactor-arch/
└── task-manager-api/
    └── .agents/skills/refactor-arch/
```

## A) Análise Manual

Análise feita antes de construir a skill, para calibrar o catálogo de anti-patterns e as heurísticas de detecção. Cada projeto tem no mínimo cinco problemas documentados, com pelo menos um CRITICAL ou HIGH, dois MEDIUM e dois LOW.

### Projeto 1: code-smells-project (Python/Flask, E-commerce)

| # | Severidade | Problema | Local | Justificativa |
|---|------------|----------|-------|---------------|
| 1 | CRITICAL | God Class: `models.py` concentra SQL, regras de negócio e quatro domínios | `models.py:1-314` | Viola SRP e MVC; qualquer alteração impacta produtos, usuários, pedidos e relatórios |
| 2 | CRITICAL | SQL Injection por concatenação de strings | `models.py:28,47-49,110,158` | Entrada do usuário interpolada em SQL |
| 3 | CRITICAL | Credenciais hardcoded (`SECRET_KEY`) | `app.py:7` | Chave de sessão versionada no repositório |
| 4 | CRITICAL | Endpoint de execução arbitrária de SQL | `app.py:59-78` (`/admin/query`) | Permite qualquer comando SQL via POST |
| 5 | HIGH | Vazamento de dados sensíveis no health check | `controllers.py:286-289` | Retorna `secret_key`, `db_path` e `debug: true` |
| 6 | HIGH | Senhas retornadas em listagem de usuários | `models.py:72-86` | Campo `senha` incluído no JSON de `get_todos_usuarios` |
| 7 | MEDIUM | Padrão N+1 em pedidos com itens | `models.py:177-199` | Loop de pedidos com queries aninhadas por item |
| 8 | MEDIUM | Rotas admin sem autenticação | `app.py:47-57` | `/admin/reset-db` apaga dados sem controle de acesso |
| 9 | LOW | Magic numbers em regras de desconto | `models.py:257-262` | Thresholds e taxas sem constantes nomeadas |
| 10 | LOW | Logging via `print` | `controllers.py:8,57,208-210` | Dificulta observabilidade em produção |

### Projeto 2: ecommerce-api-legacy (Node.js/Express, LMS + Checkout)

| # | Severidade | Problema | Local | Justificativa |
|---|------------|----------|-------|---------------|
| 1 | CRITICAL | Credenciais e chaves de pagamento hardcoded | `src/utils.js:1-7` | `dbPass`, `paymentGatewayKey` e SMTP no código |
| 2 | CRITICAL | God Object `AppManager` | `src/AppManager.js:4-139` | Classe única concentra persistência, regras e HTTP |
| 3 | HIGH | Dados de cartão e chave de gateway em log | `src/AppManager.js:45` | `console.log` expõe número de cartão e chave |
| 4 | HIGH | Criptografia fraca (`badCrypto`) | `src/utils.js:17-23` | Hash customizado e previsível |
| 5 | HIGH | Estado global mutável | `src/utils.js:9-10` | `globalCache` e `totalRevenue` sem controle de concorrência |
| 6 | MEDIUM | N+1 com callbacks aninhados no relatório financeiro | `src/AppManager.js:89-127` | Para cada curso, matrículas, usuário e pagamento em sequência |
| 7 | MEDIUM | Rota admin sem autenticação | `src/AppManager.js:80-128` | `/api/admin/financial-report` sem middleware de auth |
| 8 | LOW | Nomes crípticos no body da requisição | `src/AppManager.js:29-33` | `usr`, `eml`, `pwd`, `c_id` |
| 9 | LOW | DELETE de usuário deixa dados órfãos | `src/AppManager.js:131-136` | Sem transação ou cascade |

### Projeto 3: task-manager-api (Python/Flask, Task Manager)

| # | Severidade | Problema | Local | Justificativa |
|---|------------|----------|-------|---------------|
| 1 | CRITICAL | Hash de senha com MD5 | `models/user.py:29-32` | Algoritmo obsoleto e vulnerável |
| 2 | HIGH | `SECRET_KEY` hardcoded | `app.py:13` | Configuração deveria vir de ambiente |
| 3 | HIGH | Hash de senha exposto em `to_dict()` | `models/user.py:16-25` | API pode vazar hash em respostas JSON |
| 4 | HIGH | Token JWT fake | `routes/user_routes.py:207-211` | Autenticação simulada, sem validação real |
| 5 | HIGH | Credenciais SMTP hardcoded | `services/notification_service.py:9-10` | Senha de e-mail no código-fonte |
| 6 | MEDIUM | N+1 em listagem de tasks | `routes/task_routes.py:16-57` | `User.query.get` e `Category.query.get` dentro do loop |
| 7 | MEDIUM | Lógica de negócio nas rotas | `routes/task_routes.py:30-39`, `report_routes.py:33-43` | Blueprints fazem papel de controller |
| 8 | MEDIUM | `except` genérico | `routes/task_routes.py:62`, `user_routes.py:130` | Engole erros e dificulta diagnóstico |
| 9 | LOW | Imports não utilizados | `app.py:7` | `os`, `sys`, `json` importados sem uso |
| 10 | LOW | Uso de `datetime.utcnow()` (deprecated) | Vários arquivos | API legada em Python 3.12+ |

O projeto 3 já tinha pastas `models/`, `routes/` e `services/`, mas a separação MVC ainda era incompleta: rotas concentravam orquestração e regras que deveriam estar em controllers e services.

## B) Construção da Skill

### Localização

| Item | Valor |
|------|-------|
| Nome | `refactor-arch` |
| Origem | `code-smells-project/.agents/skills/refactor-arch/` |
| Cópias | `ecommerce-api-legacy/` e `task-manager-api/` |
| Ferramenta | Gemini CLI |

### Estrutura interna

```
refactor-arch/
├── SKILL.md
└── references/
    ├── project-analysis.md
    ├── anti-patterns-catalog.md
    ├── audit-report-template.md
    ├── report-persistence.md
    ├── mvc-guidelines.md
    └── refactoring-playbook.md
```

### Decisões de design

O `SKILL.md` concentra o workflow das três fases, regras globais e formatos de saída. O conhecimento de domínio fica nos arquivos de `references/`, carregados conforme a fase.

As fases são sequenciais e com escopo restrito: a Fase 1 só analisa, sem alterar arquivos; a Fase 2 grava relatório em `../reports/` e pausa com confirmação `[y/n]`; a Fase 3 só roda após confirmação e refatora o código.

A persistência na Fase 2 usa mapeamento fixo por pasta do projeto:

| Pasta do projeto | Arquivo gerado |
|------------------|----------------|
| `code-smells-project` | `reports/audit-project-1.md` |
| `ecommerce-api-legacy` | `reports/audit-project-2.md` |
| `task-manager-api` | `reports/audit-project-3.md` |

O catálogo descreve sinais de detecção independentes de stack (SQL concatenado, God Class, secrets hardcoded), com exemplos para Python e Node quando necessário.

### Anti-patterns no catálogo (16 itens)

| ID | Nome | Severidade |
|----|------|------------|
| AP-01 | God Class / God File | CRITICAL |
| AP-02 | SQL Injection | CRITICAL |
| AP-03 | Hardcoded Secrets | CRITICAL |
| AP-04 | Arbitrary SQL/Code Execution | CRITICAL |
| AP-05 | Missing Authentication | CRITICAL / HIGH |
| AP-06 | Sensitive Data Exposure | HIGH |
| AP-07 | Business Logic in Controllers/Routes | HIGH |
| AP-08 | Global Mutable State | HIGH |
| AP-09 | N+1 Query Pattern | MEDIUM |
| AP-10 | Fat Route Registration | MEDIUM |
| AP-11 | Duplicate Code Blocks | MEDIUM |
| AP-12 | Missing Input Validation | MEDIUM |
| AP-13 | Deprecated APIs | MEDIUM |
| AP-14 | Magic Numbers | LOW |
| AP-15 | Print/Debug Logging | LOW |
| AP-16 | Inconsistent Naming | LOW |

Esses itens cobrem os problemas encontrados nos três projetos: monolito Flask desorganizado, God Object Express e Flask parcialmente estruturado com falhas de segurança e performance.

O playbook traz 12 transformações (T-01 a T-12), cada uma com exemplo antes/depois para os anti-patterns mais comuns.

### Agnosticidade de tecnologia

A Fase 1 detecta linguagem e framework por arquivos de dependência (`requirements.txt`, `package.json`) e por imports. O catálogo usa sinais que não dependem de uma stack específica. As guidelines MVC definem estruturas alvo para Flask monolito, Express e Flask com camadas existentes. A persistência usa path relativo `../reports/` a partir de qualquer subprojeto do monorepo.

### Desafios e soluções

| Desafio | Solução |
|---------|---------|
| Projeto 3 já tinha `routes/` e `models/` | Guidelines de evolução incremental; Fase 3 cria `controllers/` e move orquestração |
| Monorepo com três subpastas | `report-persistence.md` com mapeamento fixo por nome da pasta |
| Fase 2 não pode alterar código | Escrita permitida apenas em `../reports/` |
| APIs deprecated variam por stack | AP-13 com tabela Flask/Node e detecção condicional |

## C) Resultados

### Relatórios de auditoria (Fase 2)

| Projeto | Arquivo | CRITICAL | HIGH | MEDIUM | LOW | Total |
|---------|---------|----------|------|--------|-----|-------|
| code-smells-project | `reports/audit-project-1.md` | 5 | 3 | 1 | 2 | 11 |
| ecommerce-api-legacy | `reports/audit-project-2.md` | 2 | 3 | 2 | 1 | 8 |
| task-manager-api | `reports/audit-project-3.md` | 2 | 2 | 1 | 2 | 7 |

Os relatórios seguem o template definido em `references/audit-report-template.md`, com arquivo e linha por finding, ordenados de CRITICAL para LOW. A Fase 2 pausou em cada projeto aguardando confirmação antes da refatoração.

### Comparação antes/depois da estrutura

#### Projeto 1: code-smells-project

Antes:

```
code-smells-project/
├── app.py
├── controllers.py
├── models.py
├── database.py
└── requirements.txt
```

Depois:

```
code-smells-project/
├── app.py
├── src/
│   ├── config/settings.py
│   ├── database/connection.py
│   ├── models/
│   ├── controllers/
│   ├── views/routes.py
│   └── services/
└── requirements.txt
```

#### Projeto 2: ecommerce-api-legacy

Antes:

```
ecommerce-api-legacy/src/
├── app.js
├── AppManager.js
└── utils.js
```

Depois:

```
ecommerce-api-legacy/src/
├── app.js
├── config/
├── database/
├── models/
├── controllers/
├── routes/
├── services/
└── middlewares/
```

#### Projeto 3: task-manager-api

Antes:

```
task-manager-api/
├── app.py
├── database.py
├── models/
├── routes/
├── services/
└── utils/
```

Depois:

```
task-manager-api/
├── app.py
├── config/
├── database/
├── models/
├── controllers/
├── routes/
├── services/
├── middlewares/
└── utils/
```

### Checklist de validação

#### Projeto 1: code-smells-project

**Fase 1**
- [x] Linguagem: Python
- [x] Framework: Flask 3.1.1
- [x] Domínio: E-commerce (produtos, pedidos, usuários)
- [x] Arquivos analisados condizem com a realidade

**Fase 2**
- [x] Relatório segue o template
- [x] Findings com arquivo e linha
- [x] Ordenação CRITICAL para LOW
- [x] Mínimo de 5 findings
- [x] APIs deprecated incluídas
- [x] Pausa com `[y/n]` antes da Fase 3
- [x] Salvo em `reports/audit-project-1.md`

**Fase 3**
- [x] Estrutura MVC
- [x] Config sem hardcoded
- [x] Models, views e controllers separados
- [x] Error handling centralizado
- [x] Aplicação inicia sem erros
- [x] Endpoints originais respondem

#### Projeto 2: ecommerce-api-legacy

**Fase 1**
- [x] Linguagem: JavaScript (Node.js)
- [x] Framework: Express
- [x] Domínio: LMS + checkout
- [x] Arquivos analisados corretos

**Fase 2**
- [x] Template, linhas exatas e mínimo de 5 findings
- [x] Salvo em `reports/audit-project-2.md`
- [x] Confirmação `[y/n]`

**Fase 3**
- [x] MVC aplicado ao Express
- [x] App inicia com `node src/app.js`
- [x] Rotas de checkout e admin respondem

#### Projeto 3: task-manager-api

**Fase 1**
- [x] Python + Flask
- [x] Domínio: Task Manager
- [x] Arquitetura parcialmente organizada identificada

**Fase 2**
- [x] Problemas detectados mesmo com camadas existentes
- [x] Salvo em `reports/audit-project-3.md`
- [x] Confirmação `[y/n]`

**Fase 3**
- [x] Melhoria estrutural sem quebrar endpoints
- [x] Aplicação inicia
- [x] `/health`, `/tasks`, `/users` e `/login` respondem

### Logs de validação

Projeto 1 (code-smells-project):

```
$ python app.py
==================================================
SERVIDOR REFATORADO INICIADO
Rodando em http://localhost:5000
==================================================

$ curl http://127.0.0.1:5005/health
{"status":"ok","database":"connected","versao":"1.0.0",...}

$ curl http://127.0.0.1:5005/produtos
{"dados":[{"categoria":"informatica",...}],"sucesso":true}
```

Projeto 2 (ecommerce-api-legacy):

```
$ node src/app.js
Frankenstein LMS rodando na porta 3000...

$ curl http://localhost:3000/api/admin/financial-report
{"error":"Unauthorized"}
```

A rota admin passou a exigir autenticação após a refatoração.

Projeto 3 (task-manager-api):

```
$ python app.py
 * Running on http://127.0.0.1:5005

$ curl http://127.0.0.1:5005/health
{"status":"ok","database":"connected",...}

$ curl http://127.0.0.1:5005/tasks
[{"title":"Refactor the API to MVC architecture",...}]
```

### Observações por stack

| Stack | Comportamento da skill |
|-------|------------------------|
| Flask monolito (P1) | Refatoração mais invasiva; maior ganho estrutural |
| Express (P2) | Decomposição do `AppManager`; atenção a callbacks e `utils.js` |
| Flask parcial (P3) | Evolução incremental; criação de `controllers/` sem descartar blueprints válidos |

## D) Como Executar

### Pré-requisitos

1. [Gemini CLI](https://geminicli.com/docs/cli/creating-skills/) instalado e autenticado
2. Python 3.10+ para projetos 1 e 3
3. Node.js 18+ para projeto 2
4. Skill copiada nos três projetos (já presente neste repositório)

### Copiar a skill (se necessário)

```bash
mkdir -p ecommerce-api-legacy/.agents/skills task-manager-api/.agents/skills

cp -r code-smells-project/.agents/skills/refactor-arch \
      ecommerce-api-legacy/.agents/skills/

cp -r code-smells-project/.agents/skills/refactor-arch \
      task-manager-api/.agents/skills/
```

### Executar a skill

```bash
# Projeto 1
cd code-smells-project
gemini
/skills refactor-arch

# Projeto 2
cd ../ecommerce-api-legacy
gemini
/skills refactor-arch

# Projeto 3
cd ../task-manager-api
gemini
/skills refactor-arch
```

Na Fase 2, revise o relatório salvo em `../reports/` e confirme com `y` para iniciar a refatoração.

### Validar refatoração

Projeto 1:

```bash
cd code-smells-project
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py

curl http://127.0.0.1:5005/health
curl http://127.0.0.1:5005/produtos
```

Projeto 2:

```bash
cd ecommerce-api-legacy
npm install
node src/app.js

curl http://localhost:3000/api/admin/financial-report
```

Projeto 3:

```bash
cd task-manager-api
cp .env.example .env
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt passlib
python app.py

curl http://127.0.0.1:5005/health
curl http://127.0.0.1:5005/tasks
curl -X POST http://127.0.0.1:5005/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@tasks.com","password":"admin123"}'
```

### Ordem sugerida

1. Executar no projeto 1, revisar `reports/audit-project-1.md`, confirmar Fase 3
2. Copiar skill e executar no projeto 2
3. Copiar skill e executar no projeto 3
4. Validar os três projetos com os comandos acima

Se a skill não detectar problemas suficientes ou a refatoração falhar, ajuste os arquivos em `references/` e execute novamente. Duas a quatro iterações são comuns.

## Critérios de aceite

| Critério | Requisito | Resultado |
|----------|-----------|-----------|
| Fase 1 detecta stack | 3/3 projetos | Atendido |
| Fase 2 encontra >= 5 findings | 3/3 projetos | Atendido |
| Fase 2 inclui >= 1 CRITICAL ou HIGH | 3/3 projetos | Atendido |
| Fase 3 aplicação funciona | 3/3 projetos | Atendido |

## Referências

- [Gemini CLI: Creating Agent Skills](https://geminicli.com/docs/cli/creating-skills/)
- [Agent Skills Specification](https://github.com/agentskills/agentskills)
- [Claude Code: Skills](https://docs.anthropic.com/en/docs/claude-code/skills)
- Enunciado: [ENUNCIADO_DESAFIO.md](ENUNCIADO_DESAFIO.md)
