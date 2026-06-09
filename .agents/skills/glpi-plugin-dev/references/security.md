# Segurança, Permissões E Formulários

## Regras De Acesso

- Todo front file deve incluir `../../../inc/includes.php` e validar sessão/direito antes de exibir ou modificar dados.
- Todo front file deve verificar se o plugin alvo está instalado e ativo quando a tela depende disso.
- Usar mecanismos GLPI como `Session::checkLoginUser()`, `Session::checkRight()`, `Session::haveRight()`, `canView()`, `canCreate()`, `canUpdate()`, `canDelete()` e `check()` conforme o tipo de operação.
- Não confiar em parâmetros `$_GET` ou `$_POST` sem passar pelo fluxo do objeto GLPI.
- Não criar endpoint público sem autenticação/modelo de autorização explícito.

## Formulários

- Preferir helpers GLPI para formulários, campos, botões, redirects e URLs.
- Usar `Html::closeForm()` quando o padrão local faz controle de token/form.
- Não criar forms HTML crus se o objeto GLPI ou helpers locais já cuidam de token, URL, botão, redirect e validação.
- Em ações de criação/edição/exclusão, chamar `check()` no objeto antes de `add()`, `update()`, `delete()`, `purge()` ou `restore()`.
- Redirecionar com helpers GLPI (`Html::redirect()`, `Html::back()`, `redirectToList()`) em vez de headers manuais quando possível.

## Dados E Erros

- Validar/normalizar entrada em `prepareInputForAdd()` e `prepareInputForUpdate()` quando a regra pertence ao objeto.
- Erros devem ser explícitos e acionáveis.
- Não usar catch genérico para esconder erro.
- Logs devem usar contexto estruturado quando o logger/local pattern suportar.
- Dados sensíveis devem usar mecanismos GLPI de configuração/campos seguros quando disponíveis; se usar `secured_fields` ou `secured_configs`, declarar corretamente para rotação de chave.

## SQL Injection E CSRF

- **Prevenção de SQL Injection**: Nunca concatenar variáveis ou dados do usuário diretamente em queries SQL. Sempre utilizar a API estruturada do `$DB` (como `$DB->request()`), prepared statements com `$DB->prepare()`, ou escapar dados usando `$DB->escape()` se uma consulta crua for estritamente necessária.
- **Validação de CSRF**: Para qualquer ação que altere dados (mutações via POST, PUT, DELETE ou chamadas AJAX), garantir a validação de token de sessão via `Session::checkCSRF()` ou equivalente da versão local. O plugin deve declarar `$PLUGIN_HOOKS['csrf_compliant']['pluginkey'] = true` em `setup.php` apenas quando garantir que todas as mutações passam por essa checagem.

## Limite De Mutação

- Modificar somente dados e arquivos pertencentes ao plugin alvo.
- Não alterar permissões de diretórios core para resolver problema de escrita.
- Não escrever arquivos runtime dentro da pasta do plugin; usar diretórios de dados do GLPI quando aplicável.
