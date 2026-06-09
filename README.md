# .agents — Sistema de Agentes, Subagents e Skills

Sistema de orquestração de IA para desenvolvimento do plugin GLPI, baseado em três camadas: **Maintainer** (orquestrador), **Subagents** (especialistas) e **Skills** (capacidades reutilizáveis).

---

## Arquitetura de 3 Camadas

```
MAINTAINER.md          ← Orquestrador central (não escreve código)

agents/                ← Subagents especializados (7 workers)
├── glpi-plugin-backend.md     → PHP, controllers, hooks, migrations
├── glpi-plugin-frontend.md    → JavaScript, CSS, HTML inline, DOM
├── glpi-plugin-database.md    → Schema, índices, queries, migrations
├── glpi-plugin-security.md    → XSS, CSRF, IDOR, permissões, uploads
├── glpi-plugin-qa.md          → Testes, planos de validação, E2E
├── glpi-plugin-docs.md        → Documentação, referências, README
└── glpi-plugin-api.md         → REST API externa, itemtypes, mock data

skills/                ← Capacidades reutilizáveis pelos agents
├── glpi-plugin-dev/           → Desenvolvimento GLPI (obrigatória para backend)
├── php-pro/                   → PHP idiomático e performático
├── javascript-pro/            → JavaScript moderno e async
├── frontend-security-coder/   → Segurança de DOM e XSS
├── frontend-design/           → Design visual intencional
├── design-taste-frontend/     → Critério estético e responsividade
├── animejs-animation/         → Animações de alta fidelidade
├── minimalist-ui/             → UI editorial limpa (Notion/Linear)
├── gpt-taste/                 → Landing pages com GSAP (marketing)
├── database-architect/        → Design de schema do zero
├── database-design/           → Princípios de modelagem
├── database-optimizer/        → Tuning de queries e índices
├── security-audit/            → Auditoria formal multi-fase
├── python-pro/                → Python 3.12+ idiomático
├── python-testing-patterns/   → Testes com pytest e fixtures
├── brainstorming/             → Design estruturado antes de implementar
└── grill-me/                  → Entrevista incansável de escopo

references/            ← Contexto vivo do projeto (gerado por inspeção)
├── tasks.md                   → O que está em execução agora
├── backlog.md                 → O que está planejado para depois
├── decisions.md               → Decisões técnicas já tomadas
├── plugin-context.md          → Estrutura atual do plugin
├── glpi-context.md            → Ambiente GLPI local
├── inspection-notes.md        → Alertas e dívidas técnicas
├── design-patterns-glpi.md    → Padrões de código e UI validados
└── security-audits.md         → Histórico de auditorias de segurança
```

---

## Conceitos Fundamentais

### Maintainer (Orquestrador)

O `MAINTAINER.md` é o ponto de entrada obrigatório. Ele **não escreve código** — sua função é:

- Entender completamente a task antes de qualquer delegação
- Reunir contexto via inspeção técnica e perguntas ao usuário
- Identificar quais subagents acionar e em que ordem
- Preparar briefings completos usando o template padrão
- Revisar o trabalho dos subagents antes de considerar a task concluída
- Identificar riscos e registrar decisões
- Garantir a **Filosofia de Integração Nativa** (Look & Feel GLPI)

### Subagents (Especialistas)

Cada subagent em `agents/` é um worker especializado com:

- **Propósito**: O que faz em uma frase
- **Responsabilidades**: Capacidades concretas, não intenções genéricas
- **Limites**: O que não faz, o que delega a outro agente
- **Skills associadas**: Quais skills deve carregar para executar seu trabalho
- **Entradas esperadas**: O que o Maintainer deve fornecer no briefing
- **Saída esperada**: Formato e nível de detalhe da resposta
- **Validações obrigatórias**: Checklist antes de entregar

### Skills (Capacidades)

Skills em `skills/` são módulos de conhecimento reutilizáveis que os agents carregam sob demanda. Cada skill define um domínio específico (PHP, segurança, design, banco de dados) e é estritamente **read-only** — agents nunca criam, modificam ou excluem arquivos de skills.

---

## Fluxo de Trabalho Padrão

```
1. MAINTAINER.md é carregado
      │
2. Maintainer lê references/* (tasks, decisions, plugin-context, etc.)
      │
3. Maintainer usa grill-me para alinhar escopo com o usuário
      │
4. Maintainer gera briefings formais para cada subagent
      │
5. Maintainer dispara subagents em paralelo ou sequencial:
      │
      ├── glpi-plugin-backend    (lógica PHP)
      ├── glpi-plugin-frontend   (UI/JavaScript)
      ├── glpi-plugin-database   (schema/índices)
      └── glpi-plugin-api        (REST API externa, se aplicável)
      │
6. glpi-plugin-qa cria plano de testes e cenários de validação
      │
7. glpi-plugin-security audita todas as mudanças de código
      │
8. Maintainer revisa e integra as propostas aprovadas
      │
9. glpi-plugin-docs atualiza references/ e documentação
      │
10. Maintainer valida resultado final e atualiza tasks.md
```

---

## Gatilhos de Delegação Obrigatória

O Maintainer **deve** acionar subagents quando a task envolver:

1. Alteração em **mais de 1 arquivo**
2. Refatoração estrutural ou lógica de negócio complexa
3. Criação ou modificação de testes automatizados
4. Áreas críticas de segurança, controllers, uploads, autenticação ou permissões

A implementação direta pelo Maintainer só é permitida em mudanças pontuais de 1 arquivo e baixíssimo risco.

---

## Subagents — Resumo

| Agent | Quando acionar |
|---|---|
| **Backend** | Controllers PHP, hooks, funções, migrations, direitos, CronTask, notificações, abas |
| **Frontend** | JavaScript, CSS, HTML inline de abas, polling, renderização de mensagens |
| **Database** | Schema de tabelas, índices, queries, migrations, análise de crescimento |
| **Security** | **Sempre obrigatório** para novas features/refatorações — XSS, CSRF, IDOR, permissões |
| **QA** | Planos de validação, cenários de teste, scripts de teste (PHP/Python), regressão |
| **Docs** | Manutenção de `references/`, criação de docs em `docs/`, atualização do `README.md` |
| **API** | GLPI REST API externa, modelo de dados, itemtypes, automação e mock data |

---

## Template de Briefing

Todo subagent recebe um briefing do Maintainer neste formato:

```
## Briefing para [nome do subagent]

**Objetivo da solicitação** — uma frase objetiva
**Contexto funcional** — fluxo de uso esperado
**Contexto técnico** — estado atual do plugin relevante para a task
**Motivo** — por que este subagent especificamente
**Arquivos a analisar** — lista explícita de arquivos do plugin e GLPI core
**Documentação a consultar** — URLs específicas da doc oficial
**Restrições obrigatórias** — o que não pode ser feito
**Decisões já tomadas** — referência a decisions.md
**Perguntas ainda abertas** — o que ainda não foi decidido
**Riscos conhecidos** — riscos identificados pelo Maintainer
**O que deve fazer** — lista de responsabilidades
**O que não deve fazer** — limites de escopo
**Critérios de aceite** — o que precisa ser verdade para aprovação
**Validações esperadas** — como verificar o próprio trabalho
**Formato esperado de resposta** — estrutura da entrega
```

---

## Filosofia de Integração Nativa

Todo o sistema de agentes segue o princípio de que o plugin deve ser visualmente e funcionalmente **nativo** ao GLPI:

- **UI e Dados**: Usar abas (Tabs) integradas em objetos core, menus nativos, não criar telas isoladas
- **Permissões**: Direitos registrados na matriz nativa de perfis do GLPI
- **CSS e Temas**: Usar classes nativas Tabler/Bootstrap, variáveis CSS do GLPI, proibido hardcodar cores
- **Banco**: Tabelas com prefixo `glpi_plugin_{key}_*`, foreign keys lógicas para tabelas core

---

## Regra Contra Overengineering

O Maintainer rejeita soluções que:
- Adicionem tabelas sem necessidade clara
- Introduzam bibliotecas JS pesadas quando vanilla resolve
- Criem abstrações genéricas para problemas específicos
- Aumentem o tempo de carregamento do GLPI sem benefício mensurável
- Fujam dos padrões estabelecidos do GLPI sem justificativa registrada

---

## Version Detection Gate

Todo subagent de backend, frontend ou database **deve obrigatoriamente**:
1. Confirmar `GLPI_VERSION` com evidência de arquivo e linha
2. Reportar APIs/hooks/helpers do GLPI core confirmados na versão detectada

O Maintainer rejeita propostas que não cumpram este requisito.

---

## Auditoria de Segurança Mandatória

Toda nova feature, refatoração ou modificação de código deve passar por auditoria do `glpi-plugin-security` **antes** de ser integrada. O relatório é registrado em `references/security-audits.md` com status final: APROVADO, REJEITADO ou APROVADO COM RESSALVAS.

---

## Arquivos de Referência

Os arquivos em `references/` são o contexto vivo do projeto — atualizados por inspeção real do código, nunca por suposição:

| Arquivo | Quando atualizar |
|---|---|
| `tasks.md` | Início de qualquer trabalho novo; ao concluir uma task |
| `backlog.md` | Surgir algo que não entra na task atual |
| `decisions.md` | Qualquer escolha de design, tecnologia ou padrão |
| `plugin-context.md` | Após inspeção do código (não editar manualmente) |
| `glpi-context.md` | Mudança de versão do GLPI ou do ambiente |
| `inspection-notes.md` | Após inspeção — alertas, dívidas técnicas |
| `security-audits.md` | Ao finalizar auditoria de segurança de qualquer feature |
| `design-patterns-glpi.md` | Novo padrão confirmado por evidência no core |

---

## Hierarquia de Fontes

Ao analisar qualquer solicitação, a ordem de precedência é:

1. **Código real do GLPI core** (`dev-glpi/glpi`)
2. **Documentação oficial do GLPI** (`glpi-developer-documentation.readthedocs.io`)
3. **Respostas e decisões explícitas do usuário**

O código do plugin e os arquivos de `references/` são fontes complementares obrigatórias, mas não podem contradizer o core ou a documentação oficial.
