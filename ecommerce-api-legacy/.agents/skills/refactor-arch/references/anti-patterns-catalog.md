# Catálogo de Anti-Patterns

Use esta tabela na Fase 2. Para cada linha, busque os **sinais de detecção** no código. Reporte apenas ocorrências reais com arquivo e linha.

## Escala de severidade

| Nível | Critério |
|-------|----------|
| **CRITICAL** | Segurança grave, SQL injection, credenciais expostas, execução arbitrária, God Class impedindo manutenção |
| **HIGH** | Violação forte de MVC/SOLID: lógica de negócio em rotas, acoplamento global, vazamento de dados sensíveis |
| **MEDIUM** | N+1, validação ausente, duplicação, middlewares inadequados |
| **LOW** | Legibilidade, magic numbers, logs via print, nomenclatura ruim |

---

## Anti-patterns (mínimo 8)

### AP-01 — God Class / God File
- **Severidade:** CRITICAL
- **Sinais:** Um único arquivo (>200 linhas) com queries SQL, regras de negócio, formatação e múltiplos domínios; funções para produto, usuário, pedido e relatório no mesmo módulo.
- **Stacks:** `models.py` monolítico (Flask); `AppManager.js` com DB + rotas + checkout (Express).
- **Exemplo alvo:** `models.py` com `get_todos_produtos`, `criar_pedido`, `relatorio_vendas` no mesmo arquivo.

### AP-02 — SQL Injection (concatenação de strings)
- **Severidade:** CRITICAL
- **Sinais:** SQL montado com `+`, f-strings ou template literals interpolando entrada do usuário: `"WHERE id = " + str(id)`, `"VALUES ('" + nome + "'"`
- **Stacks:** Python sqlite3 sem placeholders; Node com `` `SELECT * FROM users WHERE id = ${id}` ``.
- **Busca:** `cursor.execute("...' +`, `execute(f"`, query dinâmica com `request.args` / `req.query` sem sanitização.

### AP-03 — Hardcoded Secrets / Credentials
- **Severidade:** CRITICAL
- **Sinais:** `SECRET_KEY`, `API_KEY`, senhas de DB, tokens de pagamento literais no código; objeto `config` com senhas em plain text.
- **Stacks:** `app.config["SECRET_KEY"] = "..."`; `utils.js` com `dbPass`, `paymentGatewayKey`.
- **Busca:** strings longas aleatórias, palavras `secret`, `password`, `pk_live`, `sk_`.

### AP-04 — Arbitrary Code / SQL Execution Endpoint
- **Severidade:** CRITICAL
- **Sinais:** Rota admin que executa SQL ou código vindo do body (`/admin/query`, `eval`, `exec`).
- **Impacto:** Acesso total ao banco ou servidor.

### AP-05 — Missing Authentication on Sensitive Routes
- **Severidade:** CRITICAL (admin/destrutivo) ou HIGH (dados privados)
- **Sinais:** `DELETE`, reset de DB, listagem de usuários com senha, relatórios sem middleware de auth.
- **Busca:** rotas `/admin/*`, listagem de `usuarios` sem filtro de campos sensíveis.

### AP-06 — Sensitive Data Exposure
- **Severidade:** HIGH
- **Sinais:** Endpoint de health/status retornando `secret_key`, `db_path`, senhas; API retornando campo `senha` em listagens.
- **Exemplo:** `health_check` com `"secret_key": "..."`; `get_todos_usuarios` incluindo `senha`.

### AP-07 — Business Logic in Controllers / Routes
- **Severidade:** HIGH
- **Sinais:** Controllers com cálculos de desconto, regras de estoque, notificações (`print("ENVIANDO EMAIL")`), validação de negócio extensa que deveria estar em service/model.
- **Express:** rotas inline em `setupRoutes` com loops e cálculo de total.

### AP-08 — Global Mutable State
- **Severidade:** HIGH
- **Sinais:** `global db_connection`, `globalCache`, `totalRevenue` mutáveis importados em vários módulos; variável de módulo reatribuída.
- **Impacto:** Dificulta testes e concorrência.

### AP-09 — N+1 Query Pattern
- **Severidade:** MEDIUM
- **Sinais:** Loop sobre registros pai com query filha dentro (`for row in rows: cursor.execute(... WHERE pedido_id = ...)`); múltiplos cursores (`cursor2`, `cursor3`) no mesmo fluxo.
- **Correção:** JOIN ou eager load.

### AP-10 — Fat Route Registration / Mixed Concerns in Entry Point
- **Severidade:** MEDIUM
- **Sinais:** Dezenas de `add_url_rule` ou rotas admin definidas diretamente em `app.py` em vez de módulo de views; lógica SQL no entry point (`reset_database`, `executar_query`).
- **Stacks:** Flask `app.py`; Express `app.js` minimal mas `AppManager` gigante.

### AP-11 — Duplicate Code Blocks
- **Severidade:** MEDIUM
- **Sinais:** Funções quase idênticas (`get_pedidos_usuario` vs `get_todos_pedidos`); copy-paste de mapeamento dict repetido 4+ vezes.
- **Detecção:** blocos >15 linhas com estrutura igual mudando só filtro.

### AP-12 — Missing Input Validation
- **Severidade:** MEDIUM
- **Sinais:** POST/PUT sem validar campos obrigatórios; status de pedido aceito sem whitelist; tipos não convertidos com try/except genérico apenas.
- **Contraste:** alguns endpoints validam e outros não no mesmo arquivo.

### AP-13 — Deprecated APIs
- **Severidade:** MEDIUM (ou HIGH se impacto de segurança)
- **Sinais de detecção por stack:**

| Stack | API obsoleta | Substituto moderno |
|-------|--------------|-------------------|
| Node/Express | `req.connection` | `req.socket` |
| Node | `new Buffer(str)` | `Buffer.from(str)` |
| Node | `domain` module | `async_hooks` / Promises |
| Python | `flask.escape` (removido) | `markupsafe.escape` |
| Python | `@app.before_first_request` | `@app.before_request` ou factory pattern |
| Python | `imp.load_source` | `importlib` |
| Express 4+ | `bodyParser` global sem limite | `express.json({ limit })` |
| SQLite via string | concatenação de valores | `?` placeholders |

- **Ação no relatório:** citar API deprecated, arquivo:linha, e equivalente recomendado.

### AP-14 — Magic Numbers / Strings
- **Severidade:** LOW
- **Sinais:** Thresholds numéricos sem constante nomeada (`if faturamento > 10000`, `0.1`, `0.05`); status strings repetidas sem enum.
- **Exemplo:** faixas de desconto em `relatorio_vendas`.

### AP-15 — Debug / Print Logging in Production Path
- **Severidade:** LOW
- **Sinais:** `print("ERRO")`, `print("ENVIANDO EMAIL")`, `console.log` com dados sensíveis; `DEBUG = True` hardcoded.
- **Stacks:** controllers com prints; Express com logs de cache.

### AP-16 — Inconsistent Naming / Response Shape
- **Severidade:** LOW
- **Sinais:** mistura `dados`/`data`, `sucesso`/`success`; nomes em português e inglês no mesmo projeto; funções `get_*` vs `listar_*` sem padrão.

---

## Ordem de varredura recomendada

1. Entry point (`app.py`, `app.js`)
2. Arquivo de maior linhagem (provável God file)
3. `database.py` / conexões
4. Controllers / routes
5. `utils` / config
6. Busca global: `execute("`, `SECRET`, `global`, `print(`, `eval(`, `admin`

## Mapeamento rápido — code-smells-project (referência interna)

Problemas esperados neste projeto de treino (validar linhas no código atual):

| ID | Severidade | Onde procurar |
|----|------------|---------------|
| AP-01 | CRITICAL | `models.py` (~300+ linhas, múltiplos domínios) |
| AP-02 | CRITICAL | `models.py` — concatenação em INSERT/SELECT/UPDATE |
| AP-03 | CRITICAL | `app.py:7`, `controllers.py` health |
| AP-04 | CRITICAL | `app.py` `/admin/query` |
| AP-05 | CRITICAL | `app.py` `/admin/reset-db` sem auth |
| AP-06 | HIGH | `controllers.py` listar_usuarios + health_check |
| AP-09 | MEDIUM | `models.py` get_pedidos_usuario loops |
| AP-14 | LOW | `models.py` relatorio_vendas thresholds |
