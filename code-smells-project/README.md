# code-smells-project (Refatorado - MVC)

API de E-commerce em Python/Flask refatorada para o padrão MVC como parte do desafio `refactor-arch`.

## Arquitetura
O projeto foi reestruturado para seguir o padrão Model-View-Controller:
- `src/models/`: Persistência e consultas ao banco (SQLite) com queries parametrizadas.
- `src/views/`: Definição de rotas e Blueprints.
- `src/controllers/`: Orquestração de requisições e lógica de controle.
- `src/services/`: Lógica de negócio e serviços externos (notificações).
- `src/config/`: Configurações e variáveis de ambiente.
- `src/database/`: Gerenciamento da conexão com o banco de dados.

## Melhorias Realizadas
- **Segurança**: Fixação de vulnerabilidades de SQL Injection e remoção de endpoints administrativos inseguros (`/admin/*`).
- **Privacidade**: Proteção de dados sensíveis (o campo `senha` não é mais retornado em listagens).
- **Manutenibilidade**: Separação clara de responsabilidades seguindo o padrão MVC.
- **Performance**: Resolução de problemas de N+1 queries em pedidos usando SQL JOINs.

## Como rodar

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute a aplicação:
```bash
python app.py
```

A aplicação subirá em **`http://localhost:5005`**. O banco SQLite (`loja.db`) é criado automaticamente no primeiro boot, já com produtos e usuários de exemplo.

## Endpoints Principais
- `GET /produtos`: Listagem de produtos.
- `GET /produtos/busca?q=termo`: Busca avançada.
- `POST /login`: Autenticação de usuários.
- `POST /pedidos`: Criação de novos pedidos.
- `GET /relatorios/vendas`: Relatório de estatísticas de vendas.
- `GET /health`: Check de saúde da API.

---
*Este projeto foi refatorado automaticamente pelo Gemini CLI usando a skill `refactor-arch`.*
