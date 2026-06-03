# Task Manager API - Refactored (MVC)

API de Task Manager em Python/Flask, refatorada para seguir o padrão **MVC (Model-View-Controller)** com separação clara de responsabilidades e melhorias de segurança.

## Arquitetura Atual

O projeto agora segue uma estrutura organizada em camadas:
- **Models**: Persistência de dados e lógica de entidade (Argon2 para senhas).
- **Views (Routes)**: Definição de endpoints e roteamento (Blueprints).
- **Controllers**: Orquestração da lógica de negócio.
- **Config**: Gerenciamento de configurações e variáveis de ambiente.
- **Middlewares**: Tratamento de erros centralizado.

## Configuração

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   pip install passlib argon2-cffi python-dotenv
   ```
2. Configure o arquivo `.env` (baseado no `.env.example`).
3. Popule o banco de dados (SQLite):
   ```bash
   python seed.py
   ```

## Como Rodar

```bash
python app.py
```

A aplicação sobe em **`http://localhost:5005`**.

## Endpoints Principais

- `GET /health`: Status da API e banco de dados.
- `POST /login`: Autenticação de usuário.
- `GET /tasks`: Listagem de tarefas.
- `GET /reports/summary`: Resumo estatístico do sistema.
