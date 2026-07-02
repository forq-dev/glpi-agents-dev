# glpi-agents-dev

Framework de orquestração de IA para criar, instalar e atualizar suporte operacional em plugins GLPI.

Ele entrega um conjunto consistente de:

- `.agents/` com `MAINTAINER.md`, subagents e contexto vivo
- `system-prompts/AGENTS.md` para gerar os arquivos de entrada do projeto consumidor
- `mcp.json` e `.mcp.json` com os MCPs usados no desenvolvimento do framework
- `glpi-agents-sync`, o CLI que instala e atualiza o framework na raiz de um plugin
- `.agents-sync.runtime.json`, a configuração local de ambiente para `gh`, Playwright e Chrome

## Onde instalar

Instale este framework na **raiz do plugin GLPI**

Exemplo real:

- GLPI: `/home/h1d4n/Documents/dev-glpi/glpi`
- Plugin: `/home/h1d4n/Documents/dev-glpi/glpi/plugins/glpichat`

O diretório do plugin pode estar vazio no primeiro bootstrap. O CLI instala o framework e deixa o local pronto para você começar do zero.

## Instalação rápida

1. Clone este repositório em uma máquina com `git` e `python3`.
2. Instale o CLI localmente na raiz deste checkout:

```bash
python3 -m pip install -e .
```

3. Vá para a raiz do plugin que vai receber o framework:

```bash
cd /home/h1d4n/Documents/dev-glpi/glpi/plugins/glpichat
```

4. Faça o bootstrap apontando para este repositório remoto:

```bash
glpi-agents-sync bootstrap \
  --root /home/h1d4n/Documents/dev-glpi/glpi/plugins/glpichat \
  --source https://github.com/msouza10/glpi-agents-dev.git
```

5. Veja o que mudou:

```bash
glpi-agents-sync status --root /home/h1d4n/Documents/dev-glpi/glpi/plugins/glpichat
```

6. Aplique a atualização quando quiser:

```bash
glpi-agents-sync sync --root /home/h1d4n/Documents/dev-glpi/glpi/plugins/glpichat --yes
```

Depois do bootstrap, o plugin passa a ter os arquivos de orquestração do framework na própria raiz.

## O que o bootstrap cria

O bootstrap instala e mantém estes arquivos na raiz do plugin:

- `.agents/`
- `AGENTS.md`
- `CLAUDE.md`
- `mcp.json`
- `.mcp.json`
- `.agents-sync.json`
- `.agents-sync.runtime.json`

O bootstrap não cria estrutura de plugin GLPI. Ele só instala o framework e deixa o diretório pronto para você começar a desenvolver.

## Como a atualização funciona

O `sync` é incremental:

- atualiza arquivos gerenciados que mudaram no repositório-fonte
- cria arquivos novos quando necessário
- preserva arquivos locais que não pertencem ao framework
- só remove algo quando a remoção fica pendente e você confirma com `--yes`

Se você estiver começando do zero em uma pasta vazia, o fluxo continua o mesmo: `bootstrap` instala o framework, e depois você passa a criar o plugin ali dentro.

## Comandos principais

| Comando | O que faz |
|---|---|
| `bootstrap` | Instala o framework pela primeira vez na raiz do plugin |
| `status` | Mostra o que mudou na origem sem aplicar nada |
| `sync` | Aplica as mudanças confirmadas do framework |
| `doctor` | Valida manifesto local, origem e ambiente de runtime |
| `setup` | Gera a config local e prepara Chromium quando solicitado |

## Exemplo com `glpichat`

```bash
cd /home/h1d4n/Documents/dev-glpi/glpi/plugins/glpichat
/caminho/para/glpi-agents-dev/bin/glpi-agents-sync bootstrap \
  --source https://github.com/msouza10/glpi-agents-dev.git
/caminho/para/glpi-agents-dev/bin/glpi-agents-sync status
/caminho/para/glpi-agents-dev/bin/glpi-agents-sync sync --yes
```

Se você instalou o pacote com `pip install -e .`, pode usar `glpi-agents-sync` direto no terminal sem o wrapper.

## Uso sem instalar o pacote

Se preferir, rode o wrapper diretamente a partir da raiz deste repositório:

```bash
./bin/glpi-agents-sync bootstrap --root /home/h1d4n/Documents/dev-glpi/glpi/plugins/glpichat --source https://github.com/msouza10/glpi-agents-dev.git
```

Se você não informar `--ref`, o bootstrap usa a branch padrão do repositório-fonte. Isso evita prender a instalação em `main` quando o remoto usa outra branch, como `master`.

## Ambiente e validação

O CLI verifica o ambiente antes de executar os comandos principais:

- `gh` precisa estar instalado e autenticado
- `node` e `npx` precisam estar disponíveis
- `@playwright/mcp` e `chrome-devtools-mcp` precisam responder ao `--help`
- Chrome/Chromium precisa estar disponível localmente ou no cache do Playwright

Para regenerar a configuração local e, se quiser, baixar Chromium via Playwright:

```bash
glpi-agents-sync setup --root /home/h1d4n/Documents/dev-glpi/glpi/plugins/glpichat
glpi-agents-sync setup --root /home/h1d4n/Documents/dev-glpi/glpi/plugins/glpichat --install-playwright-browsers
```

Se quiser exportar variáveis para a sessão atual do shell:

```bash
eval "$(glpi-agents-sync setup --root /home/h1d4n/Documents/dev-glpi/glpi/plugins/glpichat --print-env)"
```

O arquivo `.agents-sync.runtime.json` controla esse comportamento e pode ser ajustado manualmente se você quiser desativar partes do ambiente ou apontar para outro executável do Chrome.

## MCPs do framework

O arquivo `mcp.json` lista os MCPs usados durante o desenvolvimento deste framework. O `.mcp.json` espelha o mesmo conteúdo para o Claude Code.

| MCP | Para que serve | Como roda |
|---|---|---|
| `context7` | Consultar documentação atualizada de bibliotecas e GLPI | HTTP |
| `github` | Ler e gerenciar repositórios, issues, PRs e runs | HTTP com `${GITHUB_TOKEN}` |
| `playwright` | Inspecionar e validar UI em navegador real | `npx @playwright/mcp@latest` |
| `chrome-devtools` | Traces, rede, console e debugging mais profundo | `npx chrome-devtools-mcp@latest --no-usage-statistics` |
| `deepwiki` | Ler sumarizações de repositórios públicos | HTTP |

Se você usa `github`, defina o token uma vez por máquina:

```bash
gh auth login
export GITHUB_TOKEN="$(gh auth token)"
```

## Arquivos de entrada no plugin

Depois do bootstrap, a raiz do plugin passa a ter:

- `AGENTS.md` para Cursor, Windsurf e editores que leem esse nome
- `CLAUDE.md` para Claude Code
- `.agents/` para o Maintainer, subagents e referências

O template que gera `AGENTS.md` e `CLAUDE.md` vive em `system-prompts/AGENTS.md`.

## Observações

- O framework é instalado na raiz do plugin, não na raiz do GLPI.
- O CLI preserva arquivos locais do plugin que não pertencem ao framework.
- O bootstrap só altera os caminhos gerenciados pelo framework; o resto do plugin continua sob seu controle.
- Se o repositório-fonte mudar, o `sync` mostra o que precisa de confirmação antes de remover qualquer coisa.
