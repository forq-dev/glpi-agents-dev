# CLAUDE.md — Meta-desenvolvimento do glpi-agents-dev

> Este arquivo orienta o Claude Code quando ele está trabalhando **neste repositório**, ou seja,
> quando o objetivo é evoluir o próprio framework (agents, skills, references) — não quando o
> framework é consumido dentro de um plugin GLPI. Para esse segundo caso, o ponto de entrada é
> `system-prompts/AGENTS.md`, que é o template exportado para projetos consumidores.

---

## O que é este repositório

`glpi-agents-dev` é um sistema de orquestração de IA (Maintainer → subagents → skills) para
desenvolvimento de plugins GLPI. Ele é distribuído para outros projetos via git subtree ou cópia
manual da pasta `.agents/`. Este `CLAUDE.md` não é sobre isso — é sobre manter e melhorar o
sistema em si, que está em evolução constante.

---

## Mapa de arquivos do repositório

```
.
├── CLAUDE.md                   ← este arquivo — meta-desenvolvimento do framework
├── README.md                   ← documentação pública: o que é, como instalar num projeto GLPI
├── mcp.json                    ← MCPs usados no desenvolvimento deste framework
├── notes.md                    ← rascunho de pendências pessoais, não é backlog formal
├── .env / .env.example         ← credenciais do ambiente GLPI local + OpenRouter (nunca commitar .env)
│
├── system-prompts/             ← template exportado para projetos consumidores
│   ├── AGENTS.md                   → regras de orquestração mandatórias (Cursor/Windsurf/genérico)
│   └── CLAUDE.md                   → symlink para AGENTS.md (Claude Code em projetos consumidores)
│
└── .agents/                    ← o framework em si — o que é copiado/subtree para outros projetos
    ├── MAINTAINER.md               → orquestrador central (planeja, delega, valida — nunca escreve código)
    ├── index.md                    → mapa do sistema, espelha a estrutura de .agents/
    ├── agents/                     → subagents especializados (glpi-plugin-*)
    ├── references/                 → contexto vivo POR PROJETO consumidor (vazio/template neste repo)
    └── skills/                     → capacidades reutilizáveis, read-only para os agents
```

Quando mexer neste repositório, a pergunta a fazer sempre é: **isso é sobre o framework em si
(`.agents/`, `system-prompts/`), ou sobre um projeto que consome o framework?** Este repositório
nunca deve acumular `references/` preenchido de um plugin real — isso pertence ao projeto
consumidor, não aqui.

---

## Como criar ou editar subagents

Subagents deste framework seguem, sem exceção, o prefixo **`glpi-plugin-*`** e escopo GLPI —
diferente das skills (ver abaixo), a maioria dos agents é criada por nós, então mantemos a
convenção de nomenclatura e o template já definidos.

Ao criar ou editar um subagent em `.agents/agents/`:

1. Use o modelo obrigatório já documentado em
   [`.agents/MAINTAINER.md`](file:///.agents/MAINTAINER.md) — seção "Modelo para registro de novos
   subagents". Não reinvente a estrutura.
2. Registre o novo subagent na tabela "Subagents disponíveis" em `MAINTAINER.md` e em
   `.agents/index.md` — os dois precisam ficar sincronizados.
3. Se o novo subagent muda quando/como outros subagents são acionados (matriz de decisão), atualize
   a seção correspondente em `MAINTAINER.md`.
4. Verifique se o `README.md` (tabela "Quando acionar cada subagent") também precisa de atualização.

## Como skills são tratadas

Skills em `.agents/skills/` **não seguem uma convenção fixa de origem** — parte é escrita para este
projeto, parte é importada de skills open-source. Por isso:

- Não tente padronizar nome, estrutura interna ou formato das skills.
- Ao adicionar uma skill nova, garanta que ela apareça na tabela de skills em `MAINTAINER.md` com
  uma descrição fiel ao que o `SKILL.md` real faz (não ao que o nome sugere).
- Skills são read-only para os agents em tempo de execução — isso é regra do Maintainer, não deste
  arquivo, mas vale lembrar ao editar: mudanças em skills são feitas por nós, aqui, manualmente.

---

## MCPs deste projeto

Carregados automaticamente pelo Claude Code via [`.mcp.json`](.mcp.json) na raiz (escopo de
projeto — vale para qualquer sessão aberta aqui). O [`mcp.json`](mcp.json) (sem ponto) espelha o
mesmo conteúdo como referência legível fora do Claude Code; mantenha os dois sincronizados ao
adicionar ou alterar um MCP.

Nenhum segredo real fica em nenhum dos dois arquivos — o header do `github` usa expansão de
variável de ambiente (`${GITHUB_TOKEN}`), resolvida pelo Claude Code a partir do shell no momento
em que a sessão inicia. Ver seção "MCPs usados no desenvolvimento deste framework" no
[`README.md`](README.md#mcps-usados-no-desenvolvimento-deste-framework) para o passo a passo de
configurar `GITHUB_TOKEN` a partir do `gh auth token`.

| MCP | Propósito |
|---|---|
| `context7` | Consultar documentação atualizada de bibliotecas (PHP, JS, GLPI) durante a criação/edição de agents e skills |
| `github` | Ler/gerenciar repositórios, issues, PRs e workflow runs do GitHub diretamente — usado no desenvolvimento deste framework (ex: consultar o `pluginsGLPI/example` ao evoluir `glpi-plugin-cicd`). Autentica via `${GITHUB_TOKEN}`, que deve refletir a sessão já autenticada do `gh` (`gh auth token`) |
| `playwright` | Controlar um navegador real (`@playwright/mcp`) para inspecionar/validar interativamente o comportamento de uma UI — usado ao revisar visualmente o resultado de uma implementação de frontend antes de considerá-la concluída. Roda via `npx @playwright/mcp@latest`, sem autenticação |
| `chrome-devtools` | Chrome DevTools completo (`chrome-devtools-mcp`) para captura de traces de performance, inspeção de requisições de rede, screenshots e mensagens de console com stack trace — mais profundo que o `playwright` especificamente para diagnóstico de performance. Roda via `npx chrome-devtools-mcp@latest --no-usage-statistics`, sem autenticação |
| `deepwiki` | Consultar documentação sintetizada por IA de repositórios públicos do GitHub (`read_wiki_structure`, `read_wiki_contents`, `ask_question`) — útil para entender rapidamente um repositório de terceiros sem clonar. Servidor remoto gratuito, sem autenticação |

Ao adicionar um novo MCP necessário para o desenvolvimento deste framework, registre-o em
`.mcp.json` e em `mcp.json`, e adicione uma linha nesta tabela explicando o propósito. MCPs
específicos de um projeto
consumidor (não deste framework) não pertencem aqui.

---

## Regras ao editar este repositório

- **Não trate `.agents/` como conteúdo estático.** Toda mudança em `agents/`, `references/` (templates)
  ou `skills/` se propaga para todo projeto que fizer `git subtree pull` deste repositório —
  pense no impacto em quem consome antes de alterar comportamento existente.
- **`system-prompts/`** é o template exportado — mudanças ali devem ficar coerentes com o que
  `MAINTAINER.md` promete fazer. Se um mudar, revise o outro.
- **`.agents/references/`** neste repositório deve permanecer como template/vazio — nunca preencher
  com contexto de um plugin real aqui.
- Sem processo formal de versionamento/changelog por enquanto — ao fazer mudanças que quebram
  compatibilidade com quem já consome o framework, sinalize isso explicitamente na mensagem de commit.
