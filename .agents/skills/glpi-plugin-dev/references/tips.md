# Menus, Tabs, Dropdowns, CronTasks, Massive Actions, Notificações, JavaScript E Testes

## Menus E Configuração

- Procurar padrões locais de `getMenuContent()`, `$PLUGIN_HOOKS['menu_toadd']`, `config_page` e classes registradas.
- Preferir integração nativa do GLPI a HTML manual.
- Validar permissões antes de mostrar ações administrativas.

## Tabs

- Para adicionar abas em objetos core, procurar no core local `getTabNameForItem()` e `displayTabContentForItem()`.
- Registrar a classe do plugin com `Plugin::registerClass()` quando necessário para tabs.
- Não editar a classe core do item para adicionar a aba.

## Dropdowns

- Verificar classes GLPI de dropdown e padrões de plugins existentes antes de criar objeto próprio.
- Usar helpers GLPI para renderizar campos, autocompletes e selects quando disponíveis.

## Search Options

- Usar o Search engine do GLPI para listagens.
- Declarar opções de busca no método esperado pela versão local, validando assinaturas e campos no core.
- Não montar listagens SQL/HTML próprias se `Search::show()` e search options resolvem.

## CronTasks

- Atualizar `plugins/crontasks.html` com `curl` antes de implementar.
- Inspecionar `CronTask` e exemplos locais.
- Implementar a ação automática em um itemtype do plugin, seguindo o padrão core `cron{Name}` e `cronInfo()` quando existir na versão local.
- Registrar a tarefa no install/upgrade com `CronTask::Register()` ou padrão local equivalente.
- GLPI limpa tarefas do plugin em clean/uninstall, mas ainda verificar efeitos colaterais e dados auxiliares criados pela tarefa.
- A rotina deve ser idempotente, registrar erros de forma explícita e não mascarar falhas externas.

## Massive Actions

- Atualizar `plugins/massiveactions.html` com `curl`.
- Declarar uso de massive actions no `setup.php` conforme a documentação e a versão local.
- Implementar subform/processamento usando `MassiveAction`, `CommonDBTM` e métodos esperados pelo core.
- Reportar sucesso/falha item a item com APIs de `MassiveAction`.

## Notificações

- Atualizar `plugins/notifications.html` com `curl`.
- Antes de criar modo novo, verificar se eventos/templates/core notifications existentes resolvem.
- Usar classes e interfaces oficiais como `NotificationSetting`, `NotificationEventInterface`, `NotificationEventAbstract`, `NotificationInterface` apenas quando existirem na versão local.
- Registrar configs no install e remover no uninstall.

## JavaScript

- Atualizar `plugins/javascript.html` com `curl`.
- Inspecionar como a versão local carrega assets JS em plugins.
- Preferir hooks do GLPI para incluir scripts e CSS, como constantes `Hooks::ADD_JAVASCRIPT`, `Hooks::ADD_CSS` e variantes para páginas anônimas quando existirem na versão local.
- Colocar assets públicos em `public/` quando esse for o padrão do plugin/core local.
- Para Vue, seguir a documentação core primeiro; usar `window.Vue.components`, configurar `externals` para não empacotar Vue novamente e namespacer componentes em `js/src/Plugin/{Yourplugin}` para evitar colisão.
- Não injetar JavaScript em arquivos core.

## Testes E Validação

- Respeitar a estratégia existente do projeto/plugin.
- Preferir validação real: PHP lint, coding standard GLPI, instalação do plugin em GLPI local, smoke test de telas, execução de migrations e uninstall.
- Quando o plugin tiver tooling similar ao exemplo oficial, usar `glpi-project/tools`, `phpstan.neon`, `psalm.xml` e comandos Composer existentes em vez de criar comandos novos.
- Usar testes unitários apenas quando a documentação/projeto exigir ou quando houver transformação pura e estável.
- Validar pelo menos:
  - plugin aparece na tela de plugins;
  - requisitos de versão estão corretos;
  - install cria tabelas/configs;
  - uninstall remove tabelas/configs/dados criados;
  - listagem e formulário respeitam permissões;
  - hooks são chamados no evento real;
  - nenhuma mudança foi feita fora da pasta do plugin alvo.
