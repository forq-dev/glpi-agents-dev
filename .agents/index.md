# .agents — Índice do sistema

Sistema de agentes para desenvolvimento do plugin **glpichat** (GLPI 11.x).

> **Entry point:** sempre comece por `MAINTAINER.md`. Ele lê o contexto, planeja e delega. Não invoque sub-agentes diretamente sem passar pelo maintainer.

---

## Estrutura

```
.agents/
├── MAINTAINER.md              ← orquestrador — carregue sempre primeiro
├── index.md                   ← este arquivo
├── agents/                    ← workers especializados
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
├── references/                ← contexto vivo do projeto (gerenciado por glpi-plugin-context)
│   ├── tasks.md               ← o que fazer agora
│   ├── backlog.md             ← o que fazer depois
│   ├── decisions.md           ← por que as coisas são como são
│   ├── plugin-context.md      ← estado atual do glpichat (gerado por inspeção)
│   ├── glpi-context.md        ← ambiente GLPI local
│   ├── inspection-notes.md    ← alertas e achados das inspeções
│   ├── design-patterns-glpi.md← padrões de código do projeto
│   └── security-audits.md     ← histórico de auditorias de segurança
└── skills/                    ← biblioteca de capacidades dos agentes
    ├── gsap-core/             ← API central GSAP (tweens, easing, stagger, matchMedia)
    ├── gsap-timeline/         ← sequenciamento de animações
    ├── gsap-performance/      ← performance: transforms, will-change, quickTo, cleanup
    ├── gsap-plugins/          ← Flip, SplitText, Draggable, DrawSVG, MorphSVG, CustomEase…
    ├── gsap-utils/            ← clamp, mapRange, snap, random, selector(scope)…
    ├── gsap-scrolltrigger/    ← scroll-driven animations (uso restrito — ver agent frontend)
    └── [outras skills…]
```

---

## Agentes

### `MAINTAINER.md`
Orquestrador central. Lê contexto, planeja, delega, valida e entrega.
Não executa código diretamente — delega para o agente certo e valida a entrega, garantindo qualidade e boas práticas do projeto.

### Subagents disponíveis

| Agent | Arquivo | Responsabilidade |
|---|---|---|
| Backend | `agents/glpi-plugin-backend.md` | Controllers PHP, hooks, migrations, direitos, CronTask |
| Frontend | `agents/glpi-plugin-frontend.md` | JavaScript, CSS, HTML inline de abas, polling |
| Database | `agents/glpi-plugin-database.md` | Schema, índices, queries, migrations |
| Security | `agents/glpi-plugin-security.md` | XSS, CSRF, IDOR, permissões, uploads |
| QA | `agents/glpi-plugin-qa.md` | Planos de validação, testes automatizados |
| Context | `agents/glpi-plugin-context.md` | Arquivos de referência interna em `.agents/references/` |
| Docs | `agents/glpi-plugin-docs.md` | Documentação do produto (`docs/`, `README.md`) |
| API | `agents/glpi-plugin-api.md` | GLPI REST API externa, itemtypes, automação |
| UX | `agents/glpi-plugin-ux.md` | Fluxos de interação, feedback visual, acessibilidade básica |
| Performance | `agents/glpi-plugin-performance.md` | Queries, polling, assets, N+1, crescimento de tabelas |

---

## References — quando atualizar cada arquivo

> Todos os arquivos em `references/` são gerenciados exclusivamente pelo agente `glpi-plugin-context`. O Maintainer os lê — nunca os edita diretamente.

| Arquivo | Atualizar quando |
|---|---|
| `tasks.md` | Início de qualquer trabalho novo; ao concluir uma task |
| `backlog.md` | Surgir algo que não entra na task atual |
| `decisions.md` | Qualquer escolha de design, tecnologia ou padrão for feita |
| `plugin-context.md` | Após inspeção do código (não editar manualmente) |
| `glpi-context.md` | Mudança de versão do GLPI ou do ambiente |
| `inspection-notes.md` | Após inspeção — alertas, dívidas técnicas, inconsistências |
| `design-patterns-glpi.md` | Novo padrão de código ou UI confirmado por inspeção no core |
| `security-audits.md` | Ao finalizar auditoria de segurança de qualquer feature ou modificação |

---

## Fluxo típico de uma sessão

```
1. Carrega MAINTAINER.md
2. Maintainer lê tasks.md + inspection-notes.md + glpi-context.md + plugin-context.md + decisions.md
3. Usuário confirma/define o foco da sessão
4. Maintainer planeja → delega para o agente certo
5. Agente executa com as skills indicadas
6. Maintainer valida coerência entre camadas
7. glpi-plugin-context atualiza references/ (tasks.md, decisions.md, etc.)
8. glpi-plugin-docs atualiza docs/ e README.md (quando aplicável)
```

---

## Convenções do projeto

- Tabelas: `glpi_plugin_glpichat_*`
- Direitos: `plugin_glpichat_*`
- Rotas: atributo `#[Route(...)]` (padrão GLPI 11.x)
- Assets: `public/js/` e `public/css/`
- Paths guest: registrados via `SessionManager::registerPluginStatelessPath`