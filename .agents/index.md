# .agents — Índice do sistema

Sistema de orquestração de IA para desenvolvimento de plugins GLPI.

> **Entry point obrigatório:** sempre comece por `MAINTAINER.md`. Ele lê o contexto, planeja e delega. Nunca invoque subagents diretamente sem passar pelo Maintainer.

---

## Estrutura completa

```
.agents/
├── MAINTAINER.md               ← orquestrador — carregue sempre primeiro
├── index.md                    ← este arquivo
├── agents/                     ← subagents especializados
│   ├── glpi-plugin-backend.md
│   ├── glpi-plugin-frontend.md
│   ├── glpi-plugin-database.md
│   ├── glpi-plugin-security.md
│   ├── glpi-plugin-qa.md
│   ├── glpi-plugin-context.md
│   ├── glpi-plugin-docs.md
│   ├── glpi-plugin-api.md
│   ├── glpi-plugin-ux.md
│   └── glpi-plugin-performance.md
├── references/                 ← contexto vivo do projeto (gerenciado por glpi-plugin-context)
│   ├── context.md              ← identidade do projeto — preenchido via bootstrap
│   ├── examples/               ← scripts e integrações existentes como referência
│   │   ├── README.md
│   │   ├── _template/          ← template para novos exemplos
│   │   └── nome-da-integracao/
│   │       ├── README.md       ← fluxo, APIs, mapeamento para GLPI
│   │       └── src/            ← código-fonte original
│   ├── tasks.md                ← o que fazer agora
│   ├── backlog.md              ← o que fazer depois
│   ├── decisions.md            ← por que as coisas são como são
│   ├── plugin-context.md       ← estado atual do plugin (gerado por inspeção)
│   ├── glpi-context.md         ← ambiente GLPI local (versão, paths)
│   ├── inspection-notes.md     ← alertas e achados das inspeções
│   ├── design-patterns-glpi.md ← padrões de código e UI validados
│   └── security-audits.md      ← histórico de auditorias de segurança
└── skills/                     ← biblioteca de capacidades (read-only — nunca modificar)
    └── [ver README.md para lista completa]
```

---

## Subagents disponíveis

| Agente | Arquivo | Responsabilidade |
|--------|---------|-----------------|
| Backend | `agents/glpi-plugin-backend.md` | Controllers PHP, hooks, migrations, direitos, CronTask |
| Frontend | `agents/glpi-plugin-frontend.md` | JavaScript, CSS, HTML inline de abas, polling |
| Database | `agents/glpi-plugin-database.md` | Schema, índices, queries, migrations |
| Security | `agents/glpi-plugin-security.md` | XSS, CSRF, IDOR, permissões, uploads |
| QA | `agents/glpi-plugin-qa.md` | Planos de validação, testes automatizados |
| Context | `agents/glpi-plugin-context.md` | Arquivos de referência interna em `.agents/references/` |
| Docs | `agents/glpi-plugin-docs.md` | Documentação do produto (`docs/`, `README.md`) |
| API | `agents/glpi-plugin-api.md` | GLPI REST API externa, itemtypes, automação |
| UX | `agents/glpi-plugin-ux.md` | Fluxos de interação, feedback visual, acessibilidade |
| Performance | `agents/glpi-plugin-performance.md` | Queries, polling, assets, N+1, crescimento de tabelas |

---

## Fluxo típico de uma sessão

**Primeira sessão — bootstrap de contexto:**
```
1. Maintainer carrega MAINTAINER.md
2. Detecta references/context.md vazio → executa Protocolo de Bootstrap
3. grill-me: entrevista estruturada (objetivo, público, escopo, fluxo, restrições, metas)
4. brainstorming: aprofunda trade-offs e decisões de produto
5. Maintainer grava references/context.md → aguarda confirmação do usuário
6. glpi-plugin-context registra decisões em references/decisions.md
7. Desenvolvimento começa apenas após confirmação
```

**Sessões seguintes:**
```
1. Maintainer lê references/context.md + references/*
2. grill-me → alinha escopo da task
3. Maintainer planeja → delega para o subagent certo
4. Subagent executa com as skills indicadas
5. glpi-plugin-security → auditoria obrigatória antes de qualquer merge
6. Maintainer valida e integra
7. glpi-plugin-context atualiza references/
8. glpi-plugin-docs atualiza docs/ e README.md (quando aplicável)
```

---

## References — quando atualizar cada arquivo

> Todos os arquivos em `references/` são gerenciados exclusivamente pelo agente `glpi-plugin-context`. O Maintainer os lê — nunca os edita diretamente.

| Arquivo | Atualizar quando |
|---------|-----------------|
| `context.md` | Bootstrap inicial; quando o escopo ou objetivo do projeto mudar |
| `examples/` | Ao adicionar novo script ou integração de referência |
| `tasks.md` | Início de qualquer trabalho novo; ao concluir uma task |
| `backlog.md` | Surgir algo que não entra na task atual |
| `decisions.md` | Qualquer escolha de design, tecnologia ou padrão for feita |
| `plugin-context.md` | Após inspeção do código (não editar manualmente) |
| `glpi-context.md` | Mudança de versão do GLPI ou do ambiente |
| `inspection-notes.md` | Após inspeção — alertas, dívidas técnicas, inconsistências |
| `design-patterns-glpi.md` | Novo padrão de código ou UI confirmado por inspeção no core |
| `security-audits.md` | Ao finalizar auditoria de segurança de qualquer feature |
