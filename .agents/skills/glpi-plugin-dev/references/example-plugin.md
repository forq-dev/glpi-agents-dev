# Plugin Oficial Example

## Como Usar

Use o plugin oficial `pluginsGLPI/example` como catálogo de padrões práticos quando ele estiver disponível localmente ou puder ser consultado. Ele ajuda a ver como o GLPI espera que plugins organizem estrutura, hooks, direitos, front files, controllers, assets, CronTasks e integração com busca.

Não trate o código do example como verdade absoluta para qualquer versão. O clone local inspecionado declara `PLUGIN_EXAMPLE_MIN_GLPI` como `11.0.0` e compatibilidade `~11.0.0` no `example.xml`; para GLPI 10.x, revalidar a documentação, o core local e tags/branches compatíveis antes de copiar padrões. Para GLPI 11.x, ainda validar o core local antes de reutilizar hooks, controllers ou constantes.

## Padrões Úteis Observados

- Estrutura com `src/`, `front/`, `locales/`, `public/` no branch 11, alguns assets na raiz no branch 10, `misc/`, `tools/`, `setup.php`, `hook.php`, `composer.json`, `README.md` e XML de metadados.
- `setup.php` usa constantes de versão mínima/máxima e declara requisitos em `plugin_version_example()`.
- `setup.php` registra classes com `Plugin::registerClass()` e usa `Glpi\Plugin\Hooks` para constantes de hooks quando disponível.
- Menus e tabs são adicionados por registro de classes e hooks, não por edição de core.
- Assets públicos são carregados por hooks como `ADD_JAVASCRIPT`, `ADD_CSS`, `ADD_HEADER_TAG` e variantes para páginas anônimas.
- `hook.php` centraliza install/uninstall, relações de banco, dropdowns, search hooks, notifications, massive actions e status hooks.
- Install usa `Config::setConfigurationValues()`, `ProfileRight::addProfileRights()`, `Migration`, charset/collation do GLPI e `CronTask::Register()`.
- Uninstall remove configs, direitos, notificações e tabelas criadas pelo plugin.
- Objetos em `src/` herdam classes GLPI como `CommonDBTM`, `CommonDropdown` e `Profile` quando isso é a extensão correta.
- Front files incluem `../../../inc/includes.php`, checam login/direitos, usam `Html::header()`, `Search::show()` e `Html::footer()`.
- Tooling inclui `composer.json`, `glpi-project/tools`, `phpstan.neon`, `psalm.xml`, `rector.php`, `tools/HEADER` e workflows GitHub.
- Há branch `origin/10.0/bugfixes` para padrões GLPI 10 e branch `main` para GLPI 11; escolher o branch compatível antes de copiar qualquer padrão.

## Cuidados Ao Reaproveitar

- Conferir se o hook existe na versão local; algumas constantes de `Glpi\Plugin\Hooks` podem não existir no GLPI 10.x.
- Não copiar exemplos marcados como didáticos ou "not working"; transformar em implementação de produção só depois de validar no core.
- Não copiar defaults de versão do example. Declarar a versão real do plugin e a faixa real do GLPI alvo.
- Não copiar SQL sem revisar APIs atuais de `$DB`, `Migration`, charset, collation e índices no core local.
- Não copiar comentários didáticos excessivos; gerar código de produção com comentários apenas em blocos importantes.
- Não copiar paths fixos `/plugins/example/`; usar helpers GLPI como `Toolbox::getItemTypeFormURL()`, `Html::redirect()` e URLs derivadas do core local quando possível.
