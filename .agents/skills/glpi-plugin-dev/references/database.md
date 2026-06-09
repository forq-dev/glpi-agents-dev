# Banco De Dados E Migrations

## Regras Obrigatórias

- Plugin nunca altera tabelas do core GLPI.
- Plugin cria, atualiza e remove apenas suas próprias tabelas.
- Usar a classe `Migration` do GLPI para instalação e atualização.
- Declarar lógica de instalação/atualização em `plugin_{pluginkey}_install()` no `hook.php`.
- Declarar limpeza em `plugin_{pluginkey}_uninstall()` no `hook.php`.

## Convenção De Tabelas

- Usar `glpi_plugin_{pluginkey}_{items}`.
- `pluginkey` deve ser a chave/diretório alfanumérica do plugin.
- Usar plural coerente para a entidade da tabela, por exemplo:
  - `glpi_plugin_myplugin_equipments`
  - `glpi_plugin_myplugin_equipmenttickets`
  - `glpi_plugin_myplugin_configs`

## Install E Upgrade

- A função de install também deve ser capaz de atualizar uma instalação existente.
- Antes de criar tabela, verificar com `$DB->tableExists($tableName)`.
- Antes de adicionar campo ou índice, validar o estado atual com APIs do `$DB`/`Migration` disponíveis no core local.
- Executar `$migration->executeMigration()` ao final.
- Não escrever SQL manual se uma API GLPI local resolver o caso com clareza.
- Quando SQL manual for necessário, usar charset/collation/primary key sign do GLPI local (`DBConnection::getDefaultCharset()`, `getDefaultCollation()`, `getDefaultPrimaryKeySignOption()` quando existirem) e executar com erro explícito (`queryOrDie()` ou padrão local equivalente). Nunca concatenar entradas diretamente na query; utilizar prepared statements (`$DB->prepare()`) ou escapar os dados via `$DB->escape()`.

## Uninstall

- Remover todas as tabelas criadas pelo plugin.
- Remover configurações, diretórios de dados, filas, relações e estados criados pelo plugin.
- Não remover dados de core ou de outros plugins.
- Se houver risco de perda de dados do usuário, explicar claramente e manter comportamento alinhado ao padrão GLPI para uninstall.

## Antes De Gerar Código

Inspecionar no código local:

- `Migration` e usos em plugins existentes.
- Métodos disponíveis em `$DB` no GLPI alvo.
- Padrões atuais para charset, collation, engine, índices e chaves.
- Implementações de install/uninstall em plugins similares.
- Uso de `ProfileRight`, `Config`, `CronTask` e notificações no install/uninstall quando o plugin cria direitos, configs, tarefas ou eventos.

Se o padrão oficial/local não estiver claro, parar e propor alternativas antes de gerar a migration.
