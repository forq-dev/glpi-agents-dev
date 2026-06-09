# Matriz Arquitetural De Plugin

Use esta matriz antes de criar código. A regra é escolher primeiro o mecanismo GLPI existente e só criar lógica própria quando o core/local não resolver.

## Mapeamento De Necessidades

- Novo tipo de dado com CRUD: criar classe `CommonDBTM`, tabela `glpi_plugin_{pluginkey}_{items}`, `front/{item}.php`, `front/{item}.form.php`, search options e direitos.
- Lista/pesquisa: usar `Search::show()` e search options. Não montar tabela HTML/SQL própria por padrão.
- Configuração do plugin: usar `Config`, `Config::setConfigurationValues()`, front/config e tab em `Config` quando o padrão local indicar.
- Direitos por perfil: usar `$rightname`, `ProfileRight::addProfileRights()`, `ProfileRight::deleteProfileRights()`, matriz de direitos e tabs em `Profile`.
- Campo extra em item core: não alterar tabela core; usar tabela do plugin relacionada ao item, hook de formulário/tab, ou relação `Item_*` conforme padrão local.
- Relação com item core: preferir tabela plugin-owned, classes `Item_*`, tabs e APIs de relação existentes.
- Dropdown simples: verificar `CommonDropdown` antes de criar `CommonDBTM` completo.
- Dispositivo/asset relacionado: verificar `CommonDevice`, `Item_Devices` e device types antes de modelar do zero.
- Menu lateral/configuração: usar `Plugin::registerClass()`, `menu_toadd`, `config_page`, `getMenuContent()` ou padrão local.
- Aba em objeto core/plugin: usar `Plugin::registerClass(..., ['addtabon' => ...])`, `getTabNameForItem()` e `displayTabContentForItem()`.
- Evento de item: usar hooks `pre_item_*`, `item_*`, `post_prepareadd` etc., validando assinatura local.
- Validação antes de salvar: preferir `prepareInputForAdd()`, `prepareInputForUpdate()` ou hook `pre_*` quando o dado vem de item core.
- Processamento periódico: usar `CronTask` no itemtype do plugin e registrar no install/upgrade.
- Ação em massa: usar Massive Actions do core e reportar resultado por item.
- Notificação: verificar eventos/templates existentes; usar `NotificationTarget` ou modo de notificação oficial quando necessário.
- JavaScript/CSS: usar hooks de header/assets e organização esperada pela versão local.
- Tela web GLPI 10.x: usar `front/*.php`.
- Tela web GLPI 11.x: considerar controller/Twig se a versão local confirmar; `front/*.php` ainda é válido quando mais simples.
- Endpoint público: escolher entre sessão sem auth check e stateless path conforme GLPI 11 docs/core; em GLPI 10, validar mecanismo local antes de gerar.

## Critério De Parada

Pare e explique antes de codar quando:

- O mecanismo GLPI correto não estiver claro.
- A solução exige alterar core ou tabela core.
- A documentação `master` mostra recurso GLPI 11, mas o alvo é GLPI 10.
- O branch local do plugin `example` não corresponde à versão alvo.
- O usuário pede compatibilidade dupla sem aceitar restrições de menor denominador comum.
