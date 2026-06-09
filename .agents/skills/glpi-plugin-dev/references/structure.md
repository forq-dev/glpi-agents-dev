# Estrutura E Arquivos Obrigatórios

## Verificação Inicial

- Trabalhar somente dentro da pasta do plugin alvo.
- Exigir código-fonte local do GLPI para inspeção antes de implementar.
- Detectar `GLPI_VERSION` no core local e reportar arquivo/linha antes de escolher padrões GLPI 10.x ou 11.x.
- Atualizar a documentação oficial com `curl` quando houver dúvida ou antes de gerar código detalhado.
- Se `curl` falhar, não seguir por memória: pedir acesso à rede ou pedir ao usuário a documentação atual.
- Não alterar GLPI core para "abrir espaço" para o plugin; usar hooks, classes, front files e APIs oficiais.

## Nome Do Plugin

- A chave/diretório do plugin deve conter apenas letras e números.
- Não usar `-`, `_`, acentos ou caracteres especiais no diretório do plugin.
- Depois de publicado ou instalado, o nome do diretório não deve mudar.
- Para exemplos, usar `myplugin`, não `my-plugin` nem `my_plugin`.

## Estrutura Recomendada Para GLPI 10.x/11.x

```text
myplugin/
├── ajax/
├── front/
├── locale/ ou locales/
├── misc/
├── public/
├── src/
├── tools/
├── composer.json
├── example.xml
├── hook.php
├── README.md
└── setup.php
```

- `front/`: arquivos PHP acessados diretamente para listagem, formulários e telas.
- `ajax/`: endpoints AJAX do plugin, quando necessários e validados no core local.
- `src/`: classes PHP com PSR-4. Para GLPI 10.x/11.x, preferir `src/` em plugins novos.
- `inc/`: legado. Não criar em plugin novo com PSR-4, salvo se o core local ou plugin legado exigir.
- `locale/` ou `locales/`: traduções `.po`, `.mo` e `.pot`. A documentação oficial cita `locale`; o plugin oficial `example` usa `locales`. Detectar o padrão do branch/plugin/tooling local antes de criar.
- `public/`: CSS, JavaScript e assets públicos carregados por hooks do GLPI. Em branches GLPI 10 do `example`, alguns assets ficam na raiz do plugin; validar como o core local resolve assets antes de mover arquivos.
- `misc/`: logo, screenshots e metadados auxiliares do plugin.
- `tools/`: ferramentas auxiliares de desenvolvimento do plugin.
- `setup.php` e `hook.php`: obrigatórios.
- `example.xml`: metadados de marketplace/release quando o plugin será distribuído.

## PSR-4 E Namespace

- Para plugins novos em GLPI 10.x/11.x, colocar classes em `src/`.
- Usar namespace `GlpiPlugin\Pluginkey`, com a parte do plugin em lowercase exceto a primeira letra, conforme documentação oficial.
- Para `myplugin`, usar `GlpiPlugin\Myplugin`; para `myexampleplugin`, usar `GlpiPlugin\Myexampleplugin`. Não usar `GlpiPlugin\MyPlugin` a menos que o core/local autoload prove que esse casing funciona.
- O nome do arquivo deve bater com o nome da classe, por exemplo `src/Equipment.php` para `Equipment`.
- Classes em subpastas usam subnamespaces, por exemplo `src/Service/SyncService.php` com `GlpiPlugin\Myplugin\Service`.

## setup.php

`setup.php` deve conter, conforme a necessidade do plugin:

- Constante de versão, por exemplo `MYPLUGIN_VERSION`.
- Constantes de compatibilidade quando úteis, por exemplo `PLUGIN_MYPLUGIN_MIN_GLPI` e `PLUGIN_MYPLUGIN_MAX_GLPI`.
- `plugin_{pluginkey}_boot()`: somente quando o core local exige inicialização antes da sessão, como caminhos stateless.
- `plugin_init_{pluginkey}()`: registro de classes, hooks e opções.
- `plugin_version_{pluginkey}()`: metadados e requisitos.
- `plugin_{pluginkey}_check_prerequisites()`: checagens explícitas quando necessário.
- `plugin_{pluginkey}_check_config()`: validação de configuração.
- `plugin_{pluginkey}_options()`: opções como `Plugin::OPTION_AUTOINSTALL_DISABLED` quando a versão local suportar.
- `$PLUGIN_HOOKS` quando o plugin usa hooks.
- `Plugin::registerClass()` quando a classe precisa ser conhecida pelo GLPI.

`plugin_version_{pluginkey}()` deve usar `requirements` para GLPI/PHP/extensões/plugins/parâmetros sempre que aplicável. Não usar `minGlpiVersion` em código novo.

## hook.php

`hook.php` deve conter funções chamadas pelo GLPI, especialmente:

- `plugin_{pluginkey}_install()`: criar/atualizar tabelas, configs e diretórios de dados do plugin.
- `plugin_{pluginkey}_uninstall()`: remover dados criados pelo plugin.
- Funções de hook declaradas em `$PLUGIN_HOOKS`, quando forem funções e não métodos estáticos.
- Funções automáticas exigidas por alguns recursos, conforme documentação oficial.

## Escrita De Arquivos

- O plugin não deve exigir permissão de escrita no próprio diretório.
- Arquivos gerados em runtime devem usar diretórios próprios de dados do GLPI, como `GLPI_PLUGIN_DOC_DIR/{pluginkey}` quando aplicável.
- Criar diretórios de dados no install e removê-los no uninstall.

## Caminhos E URLs Dinâmicos

- Nunca assumir que o plugin está instalado no diretório `/plugins/{pluginkey}/`. Em instalações modernas do GLPI 10.x/11.x, os plugins podem ser instalados sob o diretório `/marketplace/{pluginkey}/`.
- Para obter o caminho físico (filesystem) correto do plugin, usar a API core `Plugin::getPhpDir('{pluginkey}')`.
- Para obter a URL pública (web) correta do plugin, usar a API core `Plugin::getWebDir('{pluginkey}')`.
- Evitar o uso de caminhos hardcoded como `/plugins/` ou caminhos relativos longos (como `__DIR__ . '/../../'`) para referenciar assets ou endpoints do próprio plugin.

## Composer E Padrões

- Preferir dependências via `composer.json` do plugin, nunca instalação global.
- Antes de adicionar dependência, verificar se o GLPI core já fornece o recurso.
- Seguir PSR-12 para GLPI 10+ e o coding standard oficial do GLPI quando configurado.
- Usar `glpi-project/coding-standard` ou `glpi-project/tools` quando o projeto/plugin já adotar esse tooling.
