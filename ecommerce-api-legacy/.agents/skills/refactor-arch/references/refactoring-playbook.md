# Playbook de Refatoração — Padrões de Transformação

Aplique na Fase 3 um padrão por anti-pattern encontrado. Mantenha comportamento externo da API.

---

## T-01 — Decompor God Class em Models por domínio

**Anti-pattern:** AP-01 God Class

**Antes (Python):**
```python
# models.py — 300+ linhas
def get_todos_produtos(): ...
def criar_pedido(usuario_id, itens): ...
def relatorio_vendas(): ...
```

**Depois:**
```python
# models/produto_model.py
class ProdutoModel:
    @staticmethod
    def find_all(conn):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos")
        return [dict(row) for row in cursor.fetchall()]

# models/pedido_model.py
class PedidoModel:
    @staticmethod
    def create(conn, usuario_id, itens): ...
```

**Passos:** identificar agregados → criar um arquivo por entidade → mover funções → atualizar imports nos controllers.

---

## T-02 — Eliminar SQL Injection com queries parametrizadas

**Anti-pattern:** AP-02 SQL Injection

**Antes:**
```python
cursor.execute("SELECT * FROM produtos WHERE id = " + str(id))
cursor.execute(
    "INSERT INTO produtos (nome, preco) VALUES ('" + nome + "', " + str(preco) + ")"
)
```

**Depois:**
```python
cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
cursor.execute(
    "INSERT INTO produtos (nome, preco) VALUES (?, ?)",
    (nome, preco)
)
```

**Node (Antes):**
```javascript
db.run(`SELECT * FROM courses WHERE id = ${courseId}`);
```

**Node (Depois):**
```javascript
db.get('SELECT * FROM courses WHERE id = ?', [courseId]);
```

---

## T-03 — Extrair secrets para config + environment

**Anti-pattern:** AP-03 Hardcoded Secrets

**Antes:**
```python
app.config["SECRET_KEY"] = "minha-chave-super-secreta-123"
```

**Depois:**
```python
# config/settings.py
import os
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

# app.py
from config.settings import Config
app.config.from_object(Config)
```

**Node — Antes:** `utils.js` com `dbPass: "senha_..."`  
**Node — Depois:** `config/index.js` lendo `process.env.DB_PASS`

---

## T-04 — Remover ou proteger endpoints perigosos

**Anti-pattern:** AP-04 Arbitrary SQL / AP-05 Missing Auth

**Antes:**
```python
@app.route("/admin/query", methods=["POST"])
def executar_query():
    query = request.get_json().get("sql")
    cursor.execute(query)
```

**Depois (opção A — remover em produção):**
```python
# Endpoint removido; documentar em README que era apenas dev
```

**Depois (opção B — proteger):**
```python
from functools import wraps

def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not validate_admin(token):
            return jsonify({"erro": "Não autorizado"}), 401
        return f(*args, **kwargs)
    return decorated
```

---

## T-05 — Sanitizar exposição de dados sensíveis

**Anti-pattern:** AP-06 Sensitive Data Exposure

**Antes:**
```python
def get_todos_usuarios():
    result.append({"senha": row["senha"], ...})

def health_check():
    return jsonify({"secret_key": "minha-chave...", "debug": True})
```

**Depois:**
```python
def get_todos_usuarios():
    result.append({
        "id": row["id"], "nome": row["nome"],
        "email": row["email"], "tipo": row["tipo"]
    })  # senha omitida

def health_check():
    return jsonify({
        "status": "ok", "database": "connected",
        "counts": {"produtos": n, "usuarios": u, "pedidos": p}
    })
```

---

## T-06 — Extrair lógica de negócio para Services

**Anti-pattern:** AP-07 Business Logic in Controllers

**Antes:**
```python
def criar_pedido():
    resultado = models.criar_pedido(usuario_id, itens)
    print("ENVIANDO EMAIL: Pedido " + str(resultado["pedido_id"]))
    print("ENVIANDO SMS: Seu pedido foi recebido!")
    return jsonify({...}), 201
```

**Depois:**
```python
# services/notification_service.py
def notify_order_created(pedido_id, usuario_id):
    logger.info("order_created", extra={"pedido_id": pedido_id})

# controllers/pedido_controller.py
def criar_pedido():
    resultado = PedidoModel.create(...)
    notify_order_created(resultado["pedido_id"], usuario_id)
    return jsonify({"dados": resultado, "sucesso": True}), 201
```

---

## T-07 — Substituir estado global por injeção de dependência

**Anti-pattern:** AP-08 Global Mutable State

**Antes:**
```python
db_connection = None
def get_db():
    global db_connection
    if db_connection is None:
        db_connection = sqlite3.connect(...)
```

**Depois:**
```python
# database/connection.py
class Database:
    def __init__(self, path):
        self._conn = None
        self.path = path
    def get_connection(self):
        if self._conn is None:
            self._conn = sqlite3.connect(self.path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
        return self._conn

# app.py — composition root
db = Database(settings.DATABASE_PATH)
```

**Node — Antes:** `let globalCache = {}` exportado de utils  
**Node — Depois:** módulo `CacheService` com instância criada em `app.js` e passada aos controllers.

---

## T-08 — Resolver N+1 com JOIN ou batch query

**Anti-pattern:** AP-09 N+1 Query

**Antes:**
```python
for row in rows:
    cursor2.execute("SELECT * FROM itens_pedido WHERE pedido_id = " + str(row["id"]))
    for item in itens:
        cursor3.execute("SELECT nome FROM produtos WHERE id = " + str(item["produto_id"]))
```

**Depois:**
```python
cursor.execute("""
    SELECT p.id, p.usuario_id, p.status, p.total,
           i.produto_id, i.quantidade, i.preco_unitario, pr.nome AS produto_nome
    FROM pedidos p
    LEFT JOIN itens_pedido i ON i.pedido_id = p.id
    LEFT JOIN produtos pr ON pr.id = i.produto_id
    WHERE p.usuario_id = ?
""", (usuario_id,))
# Agrupar resultados em Python por pedido_id
```

---

## T-09 — Centralizar registro de rotas em Views/Blueprints

**Anti-pattern:** AP-10 Fat Entry Point

**Antes:**
```python
# app.py — 15+ add_url_rule
app.add_url_rule("/produtos", "listar_produtos", controllers.listar_produtos, methods=["GET"])
```

**Depois:**
```python
# views/routes.py
from flask import Blueprint
from controllers import produto_controller as pc

bp = Blueprint("api", __name__)
bp.add_url_rule("/produtos", view_func=pc.listar, methods=["GET"])

# app.py
from views.routes import bp
app.register_blueprint(bp)
```

**Express:** `routes/index.js` monta `router.use('/courses', courseRoutes)`.

---

## T-10 — Substituir APIs deprecated

**Anti-pattern:** AP-13 Deprecated APIs

**Antes (Node):**
```javascript
const ip = req.connection.remoteAddress;
const buf = new Buffer(data);
```

**Depois:**
```javascript
const ip = req.socket.remoteAddress;
const buf = Buffer.from(data);
```

**Antes (Flask antigo):**
```python
from flask import escape
```

**Depois:**
```python
from markupsafe import escape
```

---

## T-11 — Extrair magic numbers para constantes

**Anti-pattern:** AP-14 Magic Numbers

**Antes:**
```python
if faturamento > 10000:
    desconto = faturamento * 0.1
elif faturamento > 5000:
    desconto = faturamento * 0.05
```

**Depois:**
```python
# config/constants.py
DISCOUNT_TIERS = [
    (10_000, 0.10),
    (5_000, 0.05),
    (1_000, 0.02),
]

def calcular_desconto(faturamento):
    for threshold, rate in DISCOUNT_TIERS:
        if faturamento > threshold:
            return faturamento * rate
    return 0
```

---

## T-12 — Substituir print por logging estruturado

**Anti-pattern:** AP-15 Debug Logging

**Antes:**
```python
print("ERRO: " + str(e))
print("ENVIANDO EMAIL: Pedido " + str(id))
```

**Depois:**
```python
import logging
logger = logging.getLogger(__name__)

logger.exception("erro ao criar produto")
logger.info("pedido_criado", extra={"pedido_id": id})
```

Configure `logging.basicConfig` no composition root.

---

## Ordem de execução recomendada (Fase 3)

1. Criar `config/` e `.env.example` (T-03)
2. Criar `database/connection` (T-07)
3. Decompor models (T-01, T-02, T-08)
4. Criar controllers (T-06)
5. Criar views/routes (T-09)
6. Middleware de erros (mvc-guidelines)
7. Remover/proteger admin (T-04)
8. Sanitizar health e listagens (T-05)
9. Deprecated APIs (T-10)
10. Constantes e logging (T-11, T-12)
11. Validar boot + endpoints

## Validação por stack

| Stack | Boot | Teste mínimo |
|-------|------|--------------|
| Flask | `python app.py` ou `flask run` | GET `/health`, GET `/produtos`, POST `/login` |
| Express | `node src/app.js` | GET health, GET courses/list conforme api.http |

Se `requirements.txt` / `package.json` existir, não remova dependências usadas.
