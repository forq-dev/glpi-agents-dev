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
│   ├── glpi-plugin-docs.md
│   └── glpi-plugin-api.md
├── references/                ← contexto vivo do projeto
│   ├── tasks.md               ← o que fazer agora
│   ├── backlog.md             ← o que fazer depois
│   ├── decisions.md           ← por que as coisas são como são
│   ├── plugin-context.md      ← estado atual do glpichat (gerado por inspeção)
│   ├── glpi-context.md        ← ambiente GLPI local
│   ├── inspection-notes.md    ← alertas e achados das inspeções
│   ├── design-patterns-glpi.md← padrões de código do projeto
│   └── backlog.md
└── skills/                    ← biblioteca de capacidades dos agentes
```

---

## Agentes

### `MAINTAINER.md`
Orquestrador central. Lê contexto, planeja, delega, valida e entrega.
Não executa código diretamente, ele e pensado para delegar para o agente certo e validar a entrega, pensando sempre em qualidade e boas praticas do projeto.

---

## References — quando atualizar cada arquivo

| Arquivo | Atualizar quando |
|---|---|
| `tasks.md` | Início de qualquer trabalho novo; ao concluir uma task |
| `backlog.md` | Surgir algo que não entra na task atual |
| `decisions.md` | Qualquer escolha de design, tecnologia ou padrão for feita |
| `plugin-context.md` | Após inspeção do código (não editar manualmente) |
| `glpi-context.md` | Mudança de versão do GLPI ou do ambiente |
| `inspection-notes.md` | Após inspeção — alertas, dívidas técnicas, inconsistências |
| `design-patterns-glpi.md` | Padrões de frontend design utilizados no glpi |

---

## Fluxo típico de uma sessão

```
1. Carrega MAINTAINER.md
2. Maintainer lê tasks.md + inspection-notes.md + glpi-context.md + plugin-context.md + decisions.md 
3. Usuário confirma/define o foco da sessão
4. Maintainer planeja → delega para o agente certo
5. Agente executa com as skills indicadas
6. Maintainer valida coerência entre camadas
7. Entrega + atualiza tasks.md e decisions.md
```

---

## Convenções do projeto

- Tabelas: `glpi_plugin_glpichat_*`
- Direitos: `plugin_glpichat_*`
- Rotas: atributo `#[Route(...)]` (padrão GLPI 11.x)
- Assets: `public/js/` e `public/css/`
- Paths guest: registrados via `SessionManager::registerPluginStatelessPath`