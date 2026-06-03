# Guidelines de Arquitetura MVC Alvo

A refatoração (Fase 3) deve convergir para esta estrutura, adaptando nomes de pastas à stack.

## Princípio central

**Separação de responsabilidades:** cada camada tem um motivo para mudar.

| Camada | Responsabilidade | Pode | Não pode |
|--------|------------------|------|----------|
| **Model** | Dados, persistência, queries, entidades | SQL parametrizado, validação de schema, métodos CRUD por entidade | HTTP, jsonify, req/res, prints de notificação |
| **View** | Rotas, mapeamento URL → handler, serialização HTTP | Blueprints/Routers, registrar endpoints, status codes | Regras de negócio, SQL direto |
| **Controller** | Orquestração do caso de uso | Validar entrada, chamar models/services, montar resposta | SQL inline, secrets, lógica de desconto complexa sem extrair |
| **Config** | Settings, env vars, constantes | `SECRET_KEY`, `DEBUG`, paths de DB | Lógica de negócio |
| **Middleware** | Cross-cutting: errors, auth, logging | `@app.errorhandler`, middleware Express | Domínio específico de produto |

## Estrutura alvo — Python/Flask

```
src/                          # ou raiz se projeto minúsculo
├── config/
│   └── settings.py           # load_dotenv, os.environ
├── models/
│   ├── produto_model.py
│   ├── usuario_model.py
│   └── pedido_model.py
├── controllers/
│   ├── produto_controller.py
│   ├── usuario_controller.py
│   └── pedido_controller.py
├── views/
│   └── routes.py               # Blueprint com url_prefix
├── middlewares/
│   └── error_handler.py
├── database/
│   └── connection.py         # get_db, migrations opcionais
└── app.py                      # composition root: create_app()
```

### Composition root (`app.py`)

- Criar app Flask
- Carregar config de `config/settings.py`
- Registrar Blueprint de `views/routes.py`
- Registrar error handlers
- `if __name__ == "__main__"` apenas para dev server

### Models

- Uma classe ou módulo por agregado de domínio
- Métodos: `find_by_id`, `find_all`, `create`, `update`, `delete`
- Queries sempre com placeholders: `cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))`

### Controllers

- Funções finas: parse request → chamar model → `return jsonify(...), status`
- Validação de entrada (campos obrigatórios, tipos)
- Sem `print` de notificação; delegar a `services/notification_service.py` se necessário

### Views

- Apenas wiring: `bp.route("/produtos", methods=["GET"])(produto_controller.listar)`
- Admin/destrutivo: proteger com decorator de auth ou remover em produção

## Estrutura alvo — Node.js/Express

```
src/
├── config/
│   └── index.js                # process.env via dotenv
├── models/
│   ├── CourseModel.js
│   └── OrderModel.js
├── controllers/
│   ├── checkoutController.js
│   └── courseController.js
├── routes/
│   └── index.js                # monta routers por domínio
├── middlewares/
│   ├── errorHandler.js
│   └── auth.js
├── services/                   # opcional: regras complexas
│   └── checkoutService.js
└── app.js                      # express(), middlewares, listen
```

### Regras Express

- `AppManager` monolítico → dividir em models + controllers + routes
- `utils.js` com secrets → `config/index.js` + `.env.example`
- Estado global (`globalCache`, `totalRevenue`) → injeção ou módulo singleton testável

## Estrutura alvo — Flask parcialmente organizado (task-manager-api)

Evoluir sem reescrever do zero:

| Existente | Evolução |
|-----------|----------|
| `routes/*.py` | Mantém como Views; remove lógica de negócio |
| `models/*.py` | Reforça: só persistência |
| `services/*.py` | Regras de negócio e notificações |
| Falta `controllers/` | Criar controllers que orquestram services + models |
| `utils/helpers.py` | Segredos → config; helpers puros apenas |

## Configuração e segurança

```python
# config/settings.py (Python)
import os
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
DATABASE_PATH = os.environ.get("DATABASE_PATH", "loja.db")
```

```javascript
// config/index.js (Node)
require('dotenv').config();
module.exports = {
  port: process.env.PORT || 3000,
  dbUser: process.env.DB_USER,
  dbPass: process.env.DB_PASS,
};
```

Criar `.env.example` sem valores reais.

## Error handling centralizado

**Flask:**
```python
def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"erro": "Recurso não encontrado", "sucesso": False}), 404
    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"erro": "Erro interno", "sucesso": False}), 500
```

**Express:**
```javascript
app.use((err, req, res, next) => {
  res.status(err.status || 500).json({ erro: err.message, sucesso: false });
});
```

## Preservação de contratos API

- Manter paths e métodos HTTP originais
- Manter shape JSON quando possível (`dados`, `sucesso`, `erro`)
- Health check: remover campos sensíveis, manter contagens úteis

## Checklist pós-refatoração

- [ ] Config extraída (sem secrets hardcoded)
- [ ] Models abstraem dados
- [ ] Views/Routes só roteiam
- [ ] Controllers orquestram
- [ ] Error handling centralizado
- [ ] Entry point claro
- [ ] Queries parametrizadas
- [ ] Endpoints originais respondem
