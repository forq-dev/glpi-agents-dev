# security-audits.md — Histórico de auditorias de segurança

> Gerenciado por `glpi-plugin-context`. Não editar manualmente.
> Registrado pelo subagent `glpi-plugin-security` após cada auditoria.
> Nunca remover entradas existentes.

---

## Formato de entrada

```
## YYYY-MM-DD — [Feature ou componente auditado]

**Status:** APROVADO | APROVADO COM RESSALVAS | REJEITADO

### Escopo da auditoria
[O que foi auditado — arquivos, endpoints, fluxos]

### Superfícies de ataque analisadas
[Lista das superfícies verificadas: endpoints, uploads, manipulação de DOM, queries, sessões, etc.]

### Vetores verificados
| Vetor | Status | Observação |
|-------|--------|-----------|
| XSS | ✅ OK / ⚠️ Ressalva / ❌ Falha | [detalhe] |
| CSRF | ✅ OK / ⚠️ Ressalva / ❌ Falha | [detalhe] |
| IDOR | ✅ OK / ⚠️ Ressalva / ❌ Falha | [detalhe] |
| SQLi | ✅ OK / ⚠️ Ressalva / ❌ Falha | [detalhe] |
| Permissões | ✅ OK / ⚠️ Ressalva / ❌ Falha | [detalhe] |

### Ressalvas e pendências
[Itens com status APROVADO COM RESSALVAS — o que foi identificado e como deve ser tratado]

### Itens rejeitados
[Itens com status REJEITADO — o que deve ser corrigido antes da integração]
```

---

<!-- Auditorias abaixo desta linha, em ordem cronológica reversa -->
