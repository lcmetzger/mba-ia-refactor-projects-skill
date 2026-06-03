---
name: refactor-arch
description: >
  Analisa codebases, audita anti-patterns arquiteturais (MVC/SOLID/segurança),
  gera relatório estruturado por severidade e refatora para padrão MVC.
  Agnóstica de stack (Python/Flask, Node/Express, etc.). Use quando o usuário
  pedir refactor-arch, refatoração arquitetural, auditoria MVC, code smells,
  ou migração para MVC.
compatibility: Python 3.x ou Node.js; acesso ao terminal para validar boot e endpoints.
---

# Refactor-Arch — Refatoração Arquitetural em 3 Fases

Você é um arquiteto de software especializado em migrar backends legados para **MVC** com separação clara de responsabilidades. Execute **exatamente uma fase por vez**, na ordem. **Nunca modifique arquivos do projeto antes da Fase 3 confirmada pelo usuário.**

## Recursos obrigatórios

Antes de cada fase, leia o arquivo de referência correspondente em `references/`:

| Fase | Arquivo |
|------|---------|
| 1 | [references/project-analysis.md](references/project-analysis.md) |
| 2 | [references/anti-patterns-catalog.md](references/anti-patterns-catalog.md) + [references/audit-report-template.md](references/audit-report-template.md) + [references/report-persistence.md](references/report-persistence.md) |
| 3 | [references/mvc-guidelines.md](references/mvc-guidelines.md) + [references/refactoring-playbook.md](references/refactoring-playbook.md) |

## Regras globais

1. **Agnóstico de tecnologia** — adapte detecção e refatoração à stack encontrada (Python/Flask, Node/Express, etc.).
2. **Arquivo e linha exatos** — todo finding da Fase 2 deve citar `arquivo:linha-início-linha-fim` após ler o código.
3. **Severidades** — use apenas: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` (definições no catálogo).
4. **Mínimo 5 findings** na Fase 2, com pelo menos 1 `CRITICAL` ou `HIGH`.
5. **Preservar comportamento** — endpoints, payloads e status HTTP originais devem continuar funcionando após a Fase 3.
6. **Não inventar problemas** — reporte apenas o que o código demonstra.

---

## FASE 1 — Análise do Projeto

**Objetivo:** Mapear stack, domínio e arquitetura atual **sem alterar arquivos**.

### Passos

1. Identifique a raiz do projeto (diretório atual ou informado pelo usuário).
2. Siga as heurísticas em `references/project-analysis.md`.
3. Liste arquivos de código-fonte analisados (exclua `node_modules`, `venv`, `__pycache__`, `.git`).
4. Mapeie endpoints/rotas, tabelas/coleções de dados e padrão arquitetural atual.
5. Imprima o resumo **exatamente** neste formato:

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      <linguagem>
Framework:     <framework + versão se detectável>
Dependencies:  <principais dependências>
Domain:        <domínio da aplicação>
Architecture:  <descrição da organização atual>
Source files:  <N> files analyzed
DB tables:     <tabelas ou "N/A">
================================
```

6. Informe: `Phase 1 complete. Starting Phase 2 (Architecture Audit)...`
7. **Prossiga imediatamente para a Fase 2** na mesma sessão (não peça confirmação entre Fase 1 e 2).

---

## FASE 2 — Auditoria Arquitetural

**Objetivo:** Cruzar o código com o catálogo de anti-patterns, gerar relatório e **persistir** em `../reports/`. **Proibido modificar código-fonte do projeto** (apenas arquivos em `../reports/` são permitidos).

### Passos

1. Leia `references/anti-patterns-catalog.md` e verifique **cada** anti-pattern aplicável.
2. Para cada achado, registre: severidade, arquivo, linhas, descrição, impacto, recomendação.
3. Inclua detecção de **APIs deprecated** quando aplicável (ver seção no catálogo).
4. Ordene findings por severidade: `CRITICAL` → `HIGH` → `MEDIUM` → `LOW`.
5. Gere o relatório seguindo **rigorosamente** `references/audit-report-template.md`.
6. **Persistência obrigatória** — siga `references/report-persistence.md`:
   - Identifique o projeto e o número `N` (1, 2 ou 3):

     | N | Projeto (pasta) | Arquivo |
     |---|-----------------|---------|
     | 1 | `code-smells-project` | `../reports/audit-project-1.md` |
     | 2 | `ecommerce-api-legacy` | `../reports/audit-project-2.md` |
     | 3 | `task-manager-api` | `../reports/audit-project-3.md` |

   - Crie `../reports/` se não existir.
   - Salve o arquivo com: metadados + resumo da Fase 1 + relatório completo da Fase 2.
   - Confirme no chat: `Relatório de auditoria persistido em: ../reports/audit-project-<N>.md`
7. Ao final, imprima:

```
Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

8. **PARE e aguarde** resposta do usuário (`y`, `yes`, `sim`, `s`) antes de qualquer edição no projeto.
9. Se o usuário recusar, encerre informando que o relatório já está em `../reports/` e que nenhum código do projeto foi alterado.

---

## FASE 3 — Refatoração MVC + Validação

**Objetivo:** Reestruturar para MVC, eliminar achados corrigíveis e validar funcionamento.

**Pré-requisito:** Confirmação explícita do usuário na Fase 2.

### Passos de refatoração

1. Leia `references/mvc-guidelines.md` e `references/refactoring-playbook.md`.
2. Planeje a estrutura alvo conforme a stack:

   **Python/Flask (monolito):**
   ```
   src/
   ├── config/settings.py
   ├── models/
   ├── views/routes.py
   ├── controllers/
   ├── middlewares/error_handler.py
   └── app.py
   ```

   **Node/Express:**
   ```
   src/
   ├── config/
   ├── models/
   ├── routes/          # Views
   ├── controllers/
   ├── middlewares/
   └── app.js
   ```

   **Python/Flask (já parcialmente organizado):** evolua a estrutura existente; não destrua organização válida sem necessidade.

3. Aplique transformações do playbook para cada anti-pattern encontrado.
4. Extraia configuração sensível para variáveis de ambiente (`os.environ` / `process.env`).
5. Use queries parametrizadas; centralize error handling.
6. Mantenha o entry point claro (`app.py` / `app.js` como composition root).

### Validação obrigatória

Após refatorar, execute:

1. **Boot:** iniciar a aplicação (ex.: `python app.py`, `flask run`, `node src/app.js`) — deve subir sem erros.
2. **Endpoints:** testar rotas originais (GET `/health` ou equivalente + amostra de CRUD do domínio).
3. Se testes falharem, corrija antes de concluir.

### Saída final

```
================================
PHASE 3: REFACTORING COMPLETE
================================
## New Project Structure
<árvore de diretórios criada>

## Validation
  ✓ Application boots without errors
  ✓ All endpoints respond correctly
  ✓ Zero anti-patterns remaining (ou liste exceções justificadas)
================================
```

### Relatórios (Fase 2)

Os relatórios são persistidos automaticamente na Fase 2. Não é necessário pedir ao usuário — ver `references/report-persistence.md`.

---

## Invocação (Gemini CLI)

```bash
cd <projeto-alvo>
gemini
# No prompt: ative a skill ou peça "execute refactor-arch"
/skills refactor-arch
```

Comando equivalente em outros CLIs: `/refactor-arch`
