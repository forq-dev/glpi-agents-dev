outros mcps para adicionar.

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.devin.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# DeepWiki MCP

> How to use the official DeepWiki MCP server

The DeepWiki MCP server provides programmatic access to DeepWiki's public repository documentation and search capabilities (Ask Devin).

## What is MCP?

The [Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) is an open standard that enables AI apps to securely connect to MCP-compatible data sources and tools. You can think of MCP like a USB-C port for AI applications - a standardized way to connect AI apps to different services.

## DeepWiki MCP Server

The DeepWiki MCP server is a free, remote, no-authentication-required service that provides access to public repositories.

**Base Server URL:** `https://mcp.deepwiki.com/`

### Available Tools

The DeepWiki MCP server offers three main tools:

1. **`read_wiki_structure`** - Get a list of documentation topics for a GitHub repository
2. **`read_wiki_contents`** - View documentation about a GitHub repository
3. **`ask_question`** - Ask any question about a GitHub repository and get an AI-powered, context-grounded response

### Wire Protocols

The DeepWiki MCP server supports two wire protocols:

#### Streamable HTTP - `/mcp`

* **URL:** `https://mcp.deepwiki.com/mcp`
* Works with Cloudflare, OpenAI, and Claude
* **Recommended for most integrations**

#### SSE (Server-Sent Events) - `/sse`

* **URL:** `https://mcp.deepwiki.com/sse`
* Legacy protocol, being deprecated

<Note>
  The `/mcp` endpoint is recommended as SSE is being deprecated.
</Note>

## Setup Instructions

The field name for the server URL depends on the client: Devin Desktop uses `serverUrl`, while most other clients use the standard `url` field. Using the wrong field name causes the MCP server to be silently ignored.

### For Devin Desktop:

```json theme={null}
{
  "mcpServers": {
    "deepwiki": {
      "serverUrl": "https://mcp.deepwiki.com/mcp"
    }
  }
}
```

### For most other clients (e.g. Cursor):

```json theme={null}
{
  "mcpServers": {
    "deepwiki": {
      "url": "https://mcp.deepwiki.com/mcp"
    }
  }
}
```

### For Claude Code:

```bash theme={null}
claude mcp add -s user -t http deepwiki https://mcp.deepwiki.com/mcp
```

## Related Resources

* **[Devin's MCP Marketplace](/work-with-devin/mcp)**
* **[Connecting remote MCP servers to Claude](https://support.anthropic.com/en/articles/11175166-about-custom-integrations-using-remote-mcp)**
* **[OpenAI's docs for using the DeepWiki MCP server](https://platform.openai.com/docs/guides/tools-remote-mcp)**
* **[DeepWiki](/work-with-devin/deepwiki)**
* **[Ask Devin](/work-with-devin/ask-devin)**

<Note>
  Want DeepWiki capabilities for private repositories? Sign up for a Devin account at [Devin.ai](https://devin.ai/) and use the [Devin MCP server](/work-with-devin/devin-mcp) with your Devin API key.
</Note>


claude mcp add -s user -t http deepwiki https://mcp.deepwiki.com/mcp

Chrome DevTools para agentes
npm chrome-devtools-mcp package

O Chrome DevTools para agentes (chrome-devtools-mcp) permite que seu agente de codificação (como Antigravity, Claude, Cursor ou Copilot) controle e inspecione um navegador Chrome ativo. Ele atua como um servidor Model-Context-Protocol (MCP), dando ao seu assistente de codificação de IA acesso a todo o poder do Chrome DevTools para automação confiável, depuração aprofundada e análise de desempenho. Uma CLI também é fornecida para uso sem MCP.

Referência de ferramentas | Registro de alterações | Contribuindo | Solução de problemas | Princípios de design
Principais recursos
Obtenha insights de desempenho: Usa o Chrome DevTools para gravar rastreamentos e extrair insights de desempenho acionáveis.
Depuração avançada do navegador: Analise solicitações de rede, faça capturas de tela e verifique as mensagens do console do navegador (com stack traces mapeadas na fonte).
Automação confiável. Usa o puppeteer para automatizar ações no Chrome e aguardar automaticamente os resultados das ações.
Avisos legais
chrome-devtools-mcp expõe o conteúdo da instância do navegador aos clientes MCP, permitindo que eles inspecionem, depurem e modifiquem quaisquer dados no navegador ou DevTools. Evite compartilhar informações sensíveis ou pessoais que você não deseja compartilhar com clientes MCP.

chrome-devtools-mcp oferece suporte oficial apenas ao Google Chrome e ao Chrome for Testing. Outros navegadores baseados em Chromium podem funcionar, mas isso não é garantido, e você pode encontrar comportamento inesperado. Use por sua própria conta e risco. Estamos comprometidos em fornecer correções e suporte para a versão mais recente do Chrome Estável Estendido.

As ferramentas de desempenho podem enviar URLs de rastreamento para a API Google CrUX para buscar dados de experiência do usuário real. Isso ajuda a fornecer uma visão holística do desempenho, apresentando dados de campo juntamente com dados de laboratório. Esses dados são coletados pelo https://developer.chrome.com/docs/crux. Para desativar isso, execute com a flag --no-performance-crux.

Estatísticas de uso
O Google coleta estatísticas de uso (como taxas de sucesso de invocação de ferramentas, latência e informações do ambiente) para melhorar a confiabilidade e o desempenho do Chrome DevTools MCP.

A coleta de dados está ativada por padrão. Você pode optar por não participar passando a flag --no-usage-statistics ao iniciar o servidor:

"args": ["-y", "chrome-devtools-mcp@latest", "--no-usage-statistics"]
O Google trata esses dados de acordo com a Política de Privacidade do Google.

A coleta de estatísticas de uso do Google para o Chrome DevTools MCP é independente das estatísticas de uso do navegador Chrome. Optar por não participar das métricas do Chrome não o exclui automaticamente desta ferramenta, e vice-versa.

A coleta é desativada se as variáveis de ambiente CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS ou CI estiverem definidas.

Verificações de atualização
Por padrão, o servidor verifica periodicamente o registro npm em busca de atualizações e registra uma notificação quando uma versão mais recente está disponível. Você pode desativar essas verificações de atualização definindo a variável de ambiente CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS.

Requisitos
Node.js versão LTS.
Chrome versão estável atual ou mais recente.
npm
Primeiros passos
Adicione a seguinte configuração ao seu cliente MCP:

{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
[!NOTE] Usar chrome-devtools-mcp@latest garante que seu cliente MCP sempre usará a versão mais recente do servidor Chrome DevTools MCP.

Se você estiver interessado em realizar apenas tarefas básicas do navegador, use o modo --slim:

{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest", "--slim", "--headless"]
    }
  }
}
Consulte a Referência de ferramentas Slim.

claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest

