# Frankenstein LMS API

API de um Sistema de Gestão de Aprendizagem (LMS) com fluxo de checkout, refatorada de uma arquitetura legada para o padrão **MVC**.

## 🚀 Como Rodar

### 1. Instalar dependências
```bash
npm install
```

### 2. Configurar variáveis de ambiente
A aplicação utiliza o `dotenv` para gerenciar configurações. Um arquivo `.env` foi gerado na raiz com valores padrão. Você pode customizar a porta e o token de administração:

```env
PORT=3000
ADMIN_TOKEN=super-secret-admin-token
PAYMENT_GATEWAY_KEY=pk_live_...
```

### 3. Iniciar o servidor
```bash
npm start
```

A aplicação subirá em `http://localhost:3000`. O banco de dados SQLite é executado **em memória** e populado automaticamente a cada inicialização.

---

## 🏗️ Estrutura do Projeto (MVC)

O projeto foi reestruturado para separar responsabilidades:

- `src/config`: Configurações globais e variáveis de ambiente.
- `src/database`: Conexão e inicialização do banco de dados.
- `src/models`: Abstração de acesso aos dados (Queries SQL parametrizadas).
- `src/controllers`: Orquestração da lógica de cada rota.
- `src/services`: Lógica de negócio complexa (ex: relatórios, integrações).
- `src/routes`: Definição de endpoints e aplicação de middlewares.
- `src/middlewares`: Tratamento de erros e autenticação.

---

## 🛠️ API Endpoints

### Checkout (Público)
`POST /api/checkout`
- **Body**: `{"usr": "nome", "eml": "email@exemplo.com", "pwd": "123", "c_id": 1, "card": "4111"}`
- **Nota**: Cartões que começam com "4" são aprovados automaticamente.

**Exemplo cURL:**
```bash
curl -X POST http://localhost:3000/api/checkout \
-H "Content-Type: application/json" \
-d '{"usr": "Jose", "eml": "jose@email.com", "pwd": "123", "c_id": 1, "card": "4111"}'
```

### Relatório Financeiro (Admin)
`GET /api/admin/financial-report`
- **Header**: `Authorization: <ADMIN_TOKEN>`
- **Descrição**: Retorna o faturamento por curso e lista de alunos.

**Exemplo cURL:**
```bash
curl -H "Authorization: super-secret-admin-token" \
http://localhost:3000/api/admin/financial-report
```

### Deletar Usuário (Admin)
`DELETE /api/users/:id`
- **Header**: `Authorization: <ADMIN_TOKEN>`

**Exemplo cURL:**
```bash
curl -X DELETE http://localhost:3000/api/users/1 \
-H "Authorization: super-secret-admin-token"
```

---

## 🛡️ Melhorias Implementadas (Refatoração)
- **Fim da God Class**: `AppManager.js` foi decomposto em múltiplas camadas.
- **Segurança**: Senhas e chaves de API removidas do código e movidas para `.env`.
- **Performance**: Resolvido problema de **N+1 queries** no relatório financeiro usando `SQL JOIN`.
- **Proteção de Rotas**: Adicionado middleware de autenticação para rotas administrativas.
- **Prevenção de SQL Injection**: Todas as queries agora utilizam placeholders/parâmetros.

---

## C) Resultados
**Status**: Execução completa no projeto `ecommerce-api-legacy` (Projeto 2). Fases 1-3 finalizadas e arquitetura MVC implementada.

### Relatórios de auditoria (Fase 2)
Arquivos gerados automaticamente pela skill em `reports/`:

| Projeto | Arquivo | Status |
| :--- | :--- | :--- |
| code-smells-project | `../reports/audit-project-1.md` | ⏳ Pendente execução |
| **ecommerce-api-legacy** | `../reports/audit-project-2.md` | ✅ Concluído |
| task-manager-api | `../reports/audit-project-3.md` | ⏳ Pendente execução |

### Resumo de findings (preencher após execução):

| Projeto | CRITICAL | HIGH | MEDIUM | LOW | Total |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Projeto 1 | — | — | — | — | — |
| **Projeto 2** | 2 | 3 | 2 | 1 | **8** |
| Projeto 3 | — | — | — | — | — |

---

### Comparação antes/depois da estrutura
| Antes (Legado) | Depois (MVC) |
| :--- | :--- |
| `src/app.js` (Config + Boot) | `src/app.js` (Composition Root) |
| `src/AppManager.js` (God Object: DB + Rotas + Lógica) | `src/models/`, `src/controllers/`, `src/services/` |
| `src/utils.js` (Secrets + Helpers) | `src/config/`, `src/services/cryptoService.js`, `.env` |
