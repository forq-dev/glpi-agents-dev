# Antipadrões Que Devem Bloquear A Implementação

Pare, explique o problema e proponha alternativa quando a solução exigir:

- Editar GLPI core (`src/`, `inc/`, `front/`, `ajax/`, `templates/` fora do plugin).
- Editar outro plugin.
- Alterar `vendor/` ou dependências instaladas manualmente.
- Criar tabela fora da convenção `glpi_plugin_{pluginkey}_{items}`.
- Alterar tabela core para adicionar campo customizado.
- Criar helper/utilitário próprio sem antes procurar API GLPI equivalente.
- Copiar código do plugin `example` sem validar versão e assinatura local.
- Usar controller Symfony em GLPI 10.x sem prova no core local e documentação oficial.
- Gerar código sem detectar `GLPI_VERSION`.
- Usar hook sem confirmar nome, assinatura e disponibilidade no core local.
- Criar endpoint sem autenticação/autorização clara.
- Fazer SQL manual quando `CommonDBTM`, `Migration`, `Search`, dropdowns ou helpers GLPI resolvem.
- Escrever arquivo runtime dentro do diretório do plugin.
- Mascarar erro com `try/catch` genérico, retorno falso silencioso ou fallback não solicitado.
- Prometer compatibilidade 10.x/11.x sem validar ambos os caminhos.

Alternativas preferidas:

- Hooks, tabs, `Plugin::registerClass()`, `CommonDBTM`, `CommonDropdown`, `Migration`, `Search::show()`, front files, controllers somente em GLPI 11+, e diretórios de dados oficiais do GLPI.
