# Hooks E Eventos

## Regras Gerais

- Declarar hooks em `setup.php` no array global `$PLUGIN_HOOKS`.
- Implementar funções em `hook.php` ou métodos estáticos em classes do plugin, conforme o tipo de hook.
- Confirmar o nome e a assinatura do hook na documentação oficial atual via `curl` e no core local.
- Conferir versão mínima do hook no core/documentação. Exemplos: hooks anônimos de assets aparecem em GLPI 10.0.18; `pre_itil_info_section` e `post_itil_info_section` aparecem em GLPI 11.
- Não usar hook para alterar estado core de forma implícita quando existir API específica.

## Formas De Declaração

Função em `hook.php`:

```php
$PLUGIN_HOOKS['hook_name']['myplugin'] = 'plugin_myplugin_handle_hook';
```

Método estático:

```php
$PLUGIN_HOOKS['hook_name']['myplugin'] = [
    \GlpiPlugin\Myplugin\HookHandler::class,
    'handleHook',
];
```

## Tipos De Hooks

- Sem parâmetros: usados para exibir ou registrar comportamento em pontos globais.
- Com item (`CommonDBTM`) como parâmetro: usados em eventos de item, como add/update/delete/purge/restore.
- Com array de parâmetros: usados em hooks de formulário, tabs, display e transferência.
- Automáticos: chamados quando função `plugin_{pluginkey}_{hookname}` existe, conforme documentação.

## Hooks De Item

Validar no core local antes de usar:

- `pre_item_add`
- `item_add`
- `pre_item_update`
- `item_update`
- `pre_item_delete`
- `item_delete`
- `pre_item_purge`
- `item_purge`
- `pre_item_restore`
- `item_restore`

Preferir hooks `pre_*` para validar ou preparar dados e hooks pós-evento para efeitos derivados.

## Hooks De Display E Formulário

Validar assinatura local para:

- `pre_item_form`
- `post_item_form`
- `pre_show_item`
- `post_show_item`
- `pre_show_tab`
- `post_show_tab`

Usar para adicionar UI plugin-only sem modificar arquivos core.

## Hooks De Menu E Configuração

Validar a documentação e exemplos locais para:

- `menu_toadd`
- `config_page`
- entradas de helpdesk/menu quando aplicável
- hooks específicos de ícone, debug e kanban quando a versão local suportar

## Assets E Header

- Para JS/CSS globais, validar `add_javascript`/`add_css` ou constantes `Hooks::ADD_JAVASCRIPT`/`Hooks::ADD_CSS` no core local.
- Para páginas anônimas, validar disponibilidade de `add_javascript_anonymous_page`, `add_javascript_module_anonymous_page`, `add_css_anonymous_page` e `add_header_tag_anonymous_page` antes de usar.
- Se houver arquivo minificado com nome esperado (`plugin.min.js`, `plugin.min.css`, etc.), o GLPI pode preferi-lo; validar no core local.

## Armadilhas

- Hooks declarados com nome de plugin errado não serão chamados.
- Há inconsistência documental/histórica entre `use_massive_action` e `use_massive_actions`; sempre validar o nome aceito no core local antes de registrar Massive Actions.
- Função declarada em `$PLUGIN_HOOKS` precisa existir e ser carregável.
- Objetos recebidos por hook são objetos PHP; alterações podem afetar o fluxo do core. Não mutar sem necessidade explícita.
- Se a mudança desejada exigir editar core, parar e propor alternativa por hook, tab, front file ou classe do plugin.
