# Template de Relatório de Auditoria (Fase 2)

Reproduza **exatamente** a estrutura abaixo. Substitua placeholders com dados reais do projeto analisado.

Após montar o relatório, **persista** conforme [report-persistence.md](report-persistence.md) em `../reports/audit-project-{1|2|3}.md`.

---

## Metadados do arquivo persistido (obrigatório no topo do .md salvo)

```markdown
---
generated_by: refactor-arch
phase: 2
project_dir: <code-smells-project|ecommerce-api-legacy|task-manager-api>
audit_file: audit-project-<1|2|3>.md
generated_at: <ISO-8601>
stack: <Language> + <Framework>
---
```

## Resumo Fase 1 (obrigatório no arquivo persistido)

Inclua o bloco completo gerado na Fase 1:

```
================================
PHASE 1: PROJECT ANALYSIS
================================
...
================================
```

## Cabeçalho obrigatório

```
================================
ARCHITECTURE AUDIT REPORT
================================
Project: <nome-do-diretório-ou-projeto>
Stack:   <Language> + <Framework>
Files:   <N> analyzed | ~<LOC> lines of code
```

## Summary (obrigatório)

```
## Summary
CRITICAL: <n> | HIGH: <n> | MEDIUM: <n> | LOW: <n>
```

Contagens devem bater com a quantidade de findings listados.

## Findings (obrigatório)

Para **cada** achado, use este bloco (ordem: CRITICAL → HIGH → MEDIUM → LOW):

```
### [<SEVERITY>] <Título curto do problema>
File: <caminho/arquivo.py:linha-início-linha-fim>
Description: <o que o código faz de errado, 1-3 frases>
Impact: <consequência prática: manutenção, segurança, performance>
Recommendation: <ação concreta alinhada ao playbook MVC>
```

### Regras de formatação

| Regra | Detalhe |
|-------|---------|
| Arquivo | Caminho relativo à raiz do projeto |
| Linhas | Intervalo real após leitura do arquivo; use linha única se for 1 linha (`app.py:7`) |
| Título | Nome do anti-pattern do catálogo (ex.: "God Class / God File") |
| Mínimo | 5 findings no total |
| CRITICAL/HIGH | Pelo menos 1 finding nestes níveis |
| Deprecated | Se encontrado, título deve incluir "Deprecated API" e Recommendation deve citar substituto |

### Exemplo de finding completo

```
### [CRITICAL] Hardcoded Credentials
File: app.py:7
Description: SECRET_KEY definida como literal 'minha-chave-super-secreta-123' no código-fonte.
Impact: Chave versionada no repositório; comprometimento de sessões se o repo vazar.
Recommendation: Mover para variável de ambiente em config/settings.py e carregar via os.environ.
```

### Finding de API deprecated (quando aplicável)

```
### [MEDIUM] Deprecated API — req.connection
File: src/middleware.js:12
Description: Uso de req.connection, removido em favor de req.socket no Node moderno.
Impact: Quebra em versões futuras do Node; warnings em runtime.
Recommendation: Substituir por req.socket conforme documentação Express/Node.
```

## Rodapé obrigatório

```
================================
Total: <N> findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

## Rodapé de persistência (apenas no arquivo salvo)

Após o total de findings, antes da pergunta `[y/n]`:

```markdown
---
**Persistido em:** `../reports/audit-project-<N>.md`
```

## Qualidade mínima

Antes de finalizar, verifique:

- [ ] Summary com 4 contadores corretos
- [ ] Findings ordenados por severidade
- [ ] Cada finding tem File, Description, Impact, Recommendation
- [ ] Pelo menos 5 findings
- [ ] Pelo menos 1 CRITICAL ou HIGH
- [ ] APIs deprecated documentadas se existirem no código
- [ ] Arquivo salvo em `../reports/audit-project-{1|2|3}.md` com metadados + Fase 1 + Fase 2
- [ ] Número do arquivo correto para o projeto (1=code-smells, 2=ecommerce-api-legacy, 3=task-manager-api)
- [ ] Chat confirma caminho: `Relatório de auditoria persistido em: ../reports/audit-project-<N>.md`
- [ ] Mensagem de confirmação `[y/n]` presente no chat e no arquivo
- [ ] Código-fonte do projeto **não** foi modificado nesta fase (apenas `../reports/`)
