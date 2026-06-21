# glpi-agents-dev

Repositório central de orquestração de IA para desenvolvimento de plugins GLPI.

Contém os agentes, subagents, skills e arquivos de referência que guiam todo o processo de desenvolvimento — do planejamento à auditoria de segurança.

---

## O que é isso

Quando você desenvolve um plugin GLPI com IA, o agente precisa de contexto especializado: como o GLPI estrutura controllers, como funcionam hooks, quais padrões de segurança são obrigatórios, como registrar direitos de acesso. Sem isso, o agente gera código genérico que quebra ou não segue as convenções do GLPI.

Este repositório resolve isso com um sistema em três camadas:

- **Maintainer** — orquestrador central que planeja, delega e valida. Nunca escreve código.
- **Subagents** — especialistas por domínio (backend, frontend, segurança, banco, QA, etc.)
- **Skills** — módulos de conhecimento reutilizáveis carregados sob demanda

---

## Estrutura

```
.agents/
├── MAINTAINER.md          ← ponto de entrada obrigatório — leia sempre primeiro
├── index.md               ← mapa do sistema
│
├── agents/                ← subagents especializados
│   ├── glpi-plugin-backend.md      → controllers PHP, hooks, migrations, direitos
│   ├── glpi-plugin-frontend.md     → JavaScript, CSS, HTML inline, polling
│   ├── glpi-plugin-database.md     → schema, índices, queries, migrations
│   ├── glpi-plugin-security.md     → XSS, CSRF, IDOR, permissões, uploads
│   ├── glpi-plugin-qa.md           → testes automatizados, planos de validação
│   ├── glpi-plugin-context.md      → mantém os arquivos de references/ atualizados
│   ├── glpi-plugin-docs.md         → documentação do produto (docs/, README.md)
│   ├── glpi-plugin-api.md          → GLPI REST API externa, itemtypes, automação
│   ├── glpi-plugin-ux.md           → fluxos de interação, feedback visual
│   └── glpi-plugin-performance.md  → queries, polling, assets, N+1
│
├── references/            ← contexto vivo do projeto (específico por plugin)
│   ├── tasks.md                → o que está em execução agora
│   ├── backlog.md              → o que está planejado para depois
│   ├── decisions.md            → decisões técnicas já tomadas
│   ├── plugin-context.md       → estrutura atual do plugin (gerado por inspeção)
│   ├── glpi-context.md         → versão do GLPI e paths do ambiente local
│   ├── inspection-notes.md     → alertas e dívidas técnicas
│   ├── design-patterns-glpi.md → padrões de código e UI validados
│   └── security-audits.md      → histórico de auditorias de segurança
│
└── skills/                ← capacidades reutilizáveis (read-only — nunca modificar)
    │
    ├── # GLPI
    ├── glpi-plugin-dev/        → padrões de desenvolvimento GLPI (obrigatória para backend)
    │
    ├── # PHP / JavaScript / Python
    ├── php-pro/                → PHP idiomático e performático
    ├── javascript-pro/         → JavaScript moderno e async
    ├── python-pro/             → Python 3.12+ idiomático
    ├── python-testing-patterns/→ testes com pytest e fixtures
    │
    ├── # Frontend / Design
    ├── frontend-design/        → design visual intencional
    ├── frontend-security-coder/→ segurança de DOM e XSS
    ├── design-taste-frontend/  → critério estético e responsividade
    ├── minimalist-ui/          → UI editorial limpa (estilo Notion/Linear)
    ├── gpt-taste/              → landing pages com alto padrão visual
    │
    ├── # Animação
    ├── animejs-animation/      → animações com Anime.js
    ├── gsap-core/              → API central GSAP (tweens, easing, stagger)
    ├── gsap-timeline/          → sequenciamento de animações com Timeline
    ├── gsap-performance/       → performance: transforms, will-change, quickTo
    ├── gsap-plugins/           → Flip, SplitText, Draggable, DrawSVG, MorphSVG
    ├── gsap-utils/             → clamp, mapRange, snap, random, selector
    ├── gsap-scrolltrigger/     → animações scroll-driven
    │
    ├── # Banco de dados
    ├── database-architect/     → design de schema do zero
    ├── database-design/        → princípios de modelagem relacional
    ├── database-optimizer/     → tuning de queries e índices
    │
    ├── # Segurança
    ├── security-audit/         → auditoria formal multi-fase
    │
    ├── # Diagramação
    ├── mermaid/                → diagramas técnicos com Mermaid
    │
    └── # Processo / Método
        ├── brainstorming/      → design estruturado antes de implementar
        └── grill-me/           → entrevista incansável de escopo
```

---

## Como usar num projeto

### Opção 1 — Git Subtree (recomendado)

O subtree copia o conteúdo deste repositório para dentro do seu projeto como arquivos normais. Sem dependências externas, sem comandos extras no clone — funciona para qualquer pessoa que clonar o projeto.

**Primeira vez — importar para dentro do projeto:**
```bash
cd /caminho/do/seu/plugin

git subtree add \
  --prefix=.agents \
  https://github.com/seu-user/glpi-agents-dev \
  main \
  --squash
```

**Sincronizar quando este repositório for atualizado:**
```bash
git subtree pull \
  --prefix=.agents \
  https://github.com/seu-user/glpi-agents-dev \
  main \
  --squash
```

**Enviar melhorias feitas no plugin de volta para cá:**
```bash
git subtree push \
  --prefix=.agents \
  https://github.com/seu-user/glpi-agents-dev \
  main
```

O `--squash` condensa toda a história deste repositório em um único commit no projeto — mantém o histórico do plugin limpo.

#### O que acontece com o `references/`

Os arquivos em `references/` são específicos por projeto — o `tasks.md` do glpichat não é o mesmo de outro plugin. Como eles começam vazios (só templates), o comportamento é seguro:

- Na primeira importação: chegam vazios, você os preenche localmente
- Nos pulls seguintes: se você modificou localmente e o template original não mudou, o git não gera conflito
- Se o template mudar (coisa rara): você resolve um merge pontual só nesses arquivos

### Opção 2 — Cópia manual

Se não quiser usar subtree, copie a pasta `.agents/` para dentro do projeto. Não tem sincronização automática — você propaga atualizações na mão.

---

## Compatibilidade por plataforma de IA

Diferentes ferramentas leem o ponto de entrada em lugares diferentes:

| Ferramenta | Arquivo lido | Como configurar |
|---|---|---|
| Claude Code | `CLAUDE.md` na raiz | Criar symlink: `ln -s AGENTS.md CLAUDE.md` |
| Cursor / Windsurf | `AGENTS.md` na raiz | Já existe neste repositório |
| Kiro | `.kiro/steering/*.md` | Copiar ou linkar `MAINTAINER.md` para `.kiro/steering/` |
| Genérico | `.agents/MAINTAINER.md` | Apontar o agente diretamente para este arquivo |

Neste repositório, `CLAUDE.md` já é um symlink para `.agents/MAINTAINER.md`.

Para criar os links num projeto que usa subtree:
```bash
# Claude Code
ln -s AGENTS.md CLAUDE.md

# Kiro
mkdir -p .kiro/steering
ln -s ../../.agents/MAINTAINER.md .kiro/steering/maintainer.md
```

---

## Como o sistema funciona

### Fluxo de uma sessão

```
1. Agente carrega MAINTAINER.md
         │
2. Maintainer lê references/* (tasks, decisions, plugin-context, etc.)
         │
3. Maintainer usa grill-me → alinha escopo com o usuário (1 pergunta por vez)
         │
4. Maintainer usa brainstorming → explora trade-offs se necessário
         │
5. Maintainer gera briefings formais e delega para subagents
         │
         ├── glpi-plugin-backend    (lógica PHP)
         ├── glpi-plugin-frontend   (UI / JavaScript)
         ├── glpi-plugin-database   (schema / índices)
         └── glpi-plugin-api        (REST API, se aplicável)
         │
6. glpi-plugin-qa → plano de testes e cenários de validação
         │
7. glpi-plugin-security → auditoria obrigatória antes de qualquer merge
         │
8. Maintainer revisa e integra as propostas aprovadas
         │
9. glpi-plugin-context → atualiza references/ com decisões e achados
         │
10. glpi-plugin-docs → atualiza docs/ e README.md (quando aplicável)
```

### Regras fundamentais

**O Maintainer não escreve código.** Ele planeja, delega, revisa e valida. Implementação sempre vai para um subagent.

**Auditoria de segurança é mandatória.** Toda feature nova ou refatoração passa pelo `glpi-plugin-security` antes de ser integrada. O resultado vai para `references/security-audits.md`.

**Skills são read-only.** Nenhum agente cria, modifica ou exclui arquivos em `.agents/skills/`.

**Contexto vem dos arquivos, não da memória.** O Maintainer lê `references/` a cada sessão — não assume que lembra do que foi decidido antes.

**Version Detection Gate.** Todo subagent de backend, frontend ou banco deve confirmar `GLPI_VERSION` com evidência de arquivo e linha antes de propor qualquer implementação.

---

## Quando acionar cada subagent

| Subagent | Acionar quando |
|---|---|
| **Backend** | controllers PHP, hooks, migrations, direitos, CronTask, notificações, abas |
| **Frontend** | JavaScript, CSS, HTML inline, polling, renderização |
| **Database** | criação/alteração de tabelas, índices, queries, migrations |
| **Security** | **sempre obrigatório** para novas features ou refatorações |
| **QA** | definir plano de testes, criar scripts automatizados (PHP/Python) |
| **Context** | atualizar qualquer arquivo em `references/` após decisões ou inspeções |
| **Docs** | documentar feature entregue em `docs/` ou `README.md` do plugin |
| **API** | interagir com GLPI via REST — autenticação, CRUD, mock data, automação |
| **UX** | nova tela, novo fluxo de interação, alteração de comportamento visível |
| **Performance** | queries, polling, assets, tabelas com crescimento contínuo |

---

## Princípios de desenvolvimento

**Integração nativa ao GLPI.** O plugin deve parecer parte do GLPI, não um elemento externo colado. Isso significa usar abas nos formulários core, menus nativos, variáveis CSS do Tabler/Bootstrap (`--tblr-body-bg`, `--tblr-body-color`), e direitos gerenciáveis na matriz de perfis do GLPI.

**Sem overengineering.** O Maintainer rejeita tabelas sem necessidade clara, bibliotecas JS pesadas onde vanilla resolve, abstrações genéricas para problemas específicos, e qualquer coisa que aumente o tempo de carregamento sem benefício mensurável.

**Hierarquia de fontes.** Na dúvida, a ordem é: código real do GLPI core → documentação oficial do GLPI → decisões explícitas do usuário. O código do plugin e os `references/` são complementares, não podem contradizer o core.

---

## Convenções do projeto glpichat

Específicas do plugin que originou este sistema — adapte para o seu:

- Tabelas: `glpi_plugin_glpichat_*`
- Direitos: `plugin_glpichat_*`
- Rotas: atributo `#[Route(...)]` (padrão GLPI 11.x)
- Assets: `public/js/` e `public/css/`
- Paths guest: `SessionManager::registerPluginStatelessPath`
