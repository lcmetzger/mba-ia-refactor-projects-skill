# Persistência de Relatórios de Auditoria (Fase 2)

Ao concluir a Fase 2, **persistir obrigatoriamente** o relatório completo em disco. A persistência ocorre **antes** de pedir confirmação para a Fase 3.

## Caminho de destino

| Caminho | Descrição |
|---------|-----------|
| `../reports/` | Pasta na **raiz do monorepo** (um nível acima do projeto analisado) |
| Criação | Se `../reports/` não existir, crie o diretório |

Exemplo de layout do repositório:

```
mba-ia-refactor-projects-skill/   ← raiz do monorepo
├── reports/
│   ├── audit-project-1.md
│   ├── audit-project-2.md
│   └── audit-project-3.md
├── code-smells-project/          ← cwd ao executar projeto 1
├── ecommerce-api-legacy/         ← cwd ao executar projeto 2
└── task-manager-api/             ← cwd ao executar projeto 3
```

## Mapeamento projeto → arquivo

Identifique o projeto pela **raiz de trabalho** (diretório atual ou nome da pasta do projeto). Use o primeiro match:

| Ordem | Identificador do projeto | Arquivo de saída |
|-------|--------------------------|------------------|
| 1 | Pasta ou path contendo `code-smells-project` | `../reports/audit-project-1.md` |
| 2 | Pasta ou path contendo `ecommerce-api-legacy` | `../reports/audit-project-2.md` |
| 3 | Pasta ou path contendo `task-manager-api` | `../reports/audit-project-3.md` |

**Regra:** o número no nome do arquivo (`1`, `2`, `3`) segue a ordem fixa dos projetos do desafio, **não** a ordem de execução na sessão.

### Heurísticas de identificação (fallback)

Se o nome da pasta não bater exatamente, use sinais secundários:

| Arquivo de saída | Sinais no código |
|------------------|------------------|
| `audit-project-1.md` | Flask + `loja.db` / rotas `/produtos`, `/pedidos`; monolito `models.py` + `controllers.py` na raiz |
| `audit-project-2.md` | `package.json` com Express + `AppManager.js`; LMS/checkout; `utils.js` com `paymentGatewayKey` |
| `audit-project-3.md` | Flask + pastas `routes/`, `services/`, `models/task.py`; domínio Task Manager |

Se nenhum match for possível, pergunte ao usuário qual número (1–3) usar **antes** de salvar.

## Conteúdo do arquivo

O arquivo `.md` salvo deve conter **todo** o relatório da Fase 2, nesta ordem:

1. **Metadados** (frontmatter em comentário ou bloco inicial):

```markdown
---
generated_by: refactor-arch
phase: 2
project_dir: <nome-da-pasta-do-projeto>
audit_file: audit-project-<N>.md
generated_at: <ISO-8601, ex: 2026-06-02T14:30:00>
stack: <Language> + <Framework>
---

```

2. **Resumo da Fase 1** (copiar o bloco `PHASE 1: PROJECT ANALYSIS` gerado na mesma sessão)
3. **Relatório de auditoria** completo (template `audit-report-template.md`), incluindo Summary, Findings e rodapé com total
4. **Rodapé de persistência** (após o relatório, antes da pergunta interativa):

```markdown
---
**Persistido em:** `../reports/audit-project-<N>.md`
```

A linha `Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]` deve aparecer:
- **No arquivo salvo** (no final)
- **No chat** (para o usuário responder)

## Procedimento obrigatório

```
1. Gerar relatório completo (Fase 1 resumo + Fase 2 audit)
2. Resolver N ∈ {1, 2, 3} pelo mapeamento acima
3. mkdir -p ../reports   (se necessário)
4. Escrever ../reports/audit-project-{N}.md (sobrescrever se já existir)
5. Confirmar no chat: "Relatório salvo em ../reports/audit-project-{N}.md"
6. Imprimir: Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
7. PARAR e aguardar confirmação
```

## Restrições

- **Permitido na Fase 2:** criar/alterar apenas arquivos em `../reports/`
- **Proibido na Fase 2:** alterar código-fonte do projeto analisado (`app.py`, `src/`, etc.)
- Não salvar relatório em outro path (ex.: `./reports/` dentro do projeto) — use sempre `../reports/`

## Mensagens de confirmação no chat

Após salvar com sucesso:

```
Relatório de auditoria persistido em: ../reports/audit-project-<N>.md

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

Se falhar a escrita, informe o erro e ainda exiba o relatório no chat; tente corrigir o path e salvar novamente antes de pedir confirmação.
