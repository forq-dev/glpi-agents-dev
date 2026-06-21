# Tradução de Plugins GLPI (gettext / i18n)

> Fonte primária: inspeção do plugin `pluginsGLPI/example` (commit atual, Abril 2026), CHANGELOG do GLPI core e workflow oficial `glpi-project/plugin-translation-workflows`.
> Validar com `curl` antes de qualquer implementação de mecanismo novo de tradução.

---

## Como o GLPI carrega traduções de plugins

O GLPI usa **GNU gettext** com arquivos `.po` (texto editável) e `.mo` (binário compilado). O carregamento é automático — **o plugin não precisa chamar nenhuma função de inicialização**. O GLPI detecta e carrega os arquivos da pasta `locales/` do plugin com base no idioma ativo do usuário.

O único requisito é que:
1. Os arquivos estejam na pasta correta com o nome correto.
2. As strings PHP usem o **domínio do plugin** como segundo argumento.

---

## Estrutura de pastas obrigatória

```
plugins/{pluginkey}/
└── locales/
    ├── {pluginkey}.pot      ← template de tradução (source of truth)
    ├── pt_BR.po             ← tradução PT-BR (texto editável)
    ├── pt_BR.mo             ← tradução PT-BR (binário compilado, gerado por msgfmt)
    ├── en_GB.po
    ├── en_GB.mo
    ├── fr_FR.po
    └── fr_FR.mo
```

**Naming obrigatório:**
- O `.pot` usa o nome do plugin: `{pluginkey}.pot`
- Os `.po`/`.mo` usam o código de locale: `{ll_CC}.po` (ex: `pt_BR.po`, `fr_FR.po`, `en_GB.po`)
- O `pluginkey` deve ser o mesmo nome alfanumérico da pasta do plugin (sem hífens, sem underscores no nome de pasta — mas o domínio de tradução no PHP é o `pluginkey`)

---

## Helpers de tradução PHP

Sempre passar o `pluginkey` como **segundo argumento**. Sem isso, a string vai para o domínio do GLPI core e não será encontrada pelo plugin.

### `__($str, $domain)` — string simples

```php
echo __('My plugin label', 'myplugin');
```

### `__s($str, $domain)` — string simples com escape HTML

Usar em contextos de atributos HTML (`value=`, `placeholder=`, `title=`), onde a string será embutida em HTML sem processamento adicional de escape.

```php
echo '<input placeholder="' . __s('Search...', 'myplugin') . '">';
```

### `_n($str_singular, $str_plural, $n, $domain)` — plural

```php
echo _n('%d item found', '%d items found', $count, 'myplugin');
```

O GLPI usa as regras de plural do próprio arquivo `.po` (campo `Plural-Forms`), respeitando idiomas com múltiplas formas plurais (ex: polonês, russo).

### `_x($context, $str, $domain)` — com contexto para tradutores

Usar quando a mesma string tem significados diferentes dependendo do contexto (ex: "Open" pode ser "Abrir" ou "Aberto").

```php
echo _x('verb', 'Open', 'myplugin');   // "Abrir"
echo _x('adjective', 'Open', 'myplugin'); // "Aberto"
```

O contexto aparece no `.po` como `msgctxt` e ajuda tradutores a distinguir os usos.

### `_nx($context, $str_singular, $str_plural, $n, $domain)` — plural com contexto

```php
echo _nx('ticket', '%d open ticket', '%d open tickets', $count, 'myplugin');
```

### Equivalentes JavaScript (disponíveis desde GLPI 9.5)

O GLPI expõe as mesmas funções no contexto do browser:

```javascript
__('My plugin label', 'myplugin');
_n('%d item found', '%d items found', count, 'myplugin');
_x('verb', 'Open', 'myplugin');
_nx('ticket', '%d open ticket', '%d open tickets', count, 'myplugin');
```

> ⚠️ As strings JS precisam estar no mesmo `.po`/`.mo` que as strings PHP. O GLPI carrega as traduções do plugin automaticamente para o JS também — não há registro separado.

---

## Regras obrigatórias para strings traduzíveis

### Strings sempre literais — nunca variáveis

O extrator de strings (`xgettext`) analisa o código estaticamente. Strings em variáveis não serão extraídas:

```php
// ❌ Não extraído pelo xgettext
$label = 'My label';
echo __($label, 'myplugin');

// ✅ Correto
echo __('My label', 'myplugin');
```

### Interpolação com sprintf — não concatenação

```php
// ❌ Não traduzível corretamente
echo __('Found', 'myplugin') . ' ' . $count . ' ' . __('items', 'myplugin');

// ✅ Correto — tradutores podem reordenar os placeholders
echo sprintf(__('Found %d items', 'myplugin'), $count);

// Para múltiplos parâmetros, usar numeração explícita
// O .po deve conter: "CLASS=%1$s ID=%2$d"
echo sprintf(__('CLASS=%1$s ID=%2$d', 'myplugin'), $classname, $id);
```

Anotar o tipo dos parâmetros como comentário no código para os tradutores — o extrator inclui a linha no `.po`:

```php
//TRANS: %1$s is the item class name, %2$d is the item ID
echo sprintf(__('CLASS=%1$s ID=%2$d', 'myplugin'), $classname, $id);
```

Esse comentário aparece no `.pot`/`.po` como:
```
#. TRANS: %1$s is the item class name, %2$d is the item ID
```

### Nunca hardcodar texto público

Toda string visível ao usuário (labels, mensagens de erro, títulos de abas, nomes de CronTask, descrições de direitos) deve passar por um helper de tradução. A única exceção são strings internas de debug ou logs que nunca chegam à interface.

---

## Estrutura do arquivo `.pot`

O `.pot` é o template — mantido em inglês, com `msgstr ""` vazio. Exemplo real do plugin `example`:

```po
# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
# This file is distributed under the same license as the PACKAGE package.
#
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\n"
"POT-Creation-Date: 2026-04-30 03:32+0000\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"

#: src/Example.php:78
msgid "Test link"
msgstr ""

#. TRANS: %1$s is a class name, %2$d is an item ID
#: src/Example.php:294
#, php-format
msgid "Plugin example CLASS=%1$s"
msgstr ""
```

**Campos obrigatórios no cabeçalho do `.po` de tradução:**
```po
"Language: pt_BR\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\n"
"Content-Type: text/plain; charset=UTF-8\n"
```

---

## Compilação: `.po` → `.mo`

O GLPI só carrega arquivos `.mo`. O `.po` é para humanos; o `.mo` é para o PHP.

```bash
# Compilar um arquivo
msgfmt locales/pt_BR.po -o locales/pt_BR.mo

# Compilar todos de uma vez
for po in locales/*.po; do
    msgfmt "$po" -o "${po%.po}.mo"
done
```

> ⚠️ O `.mo` deve estar presente e atualizado. Editar o `.po` sem recompilar não tem efeito. Em desenvolvimento local, recompilar sempre após editar traduções.

---

## Extração de strings: gerando/atualizando o `.pot`

```bash
# Extrair strings de todos os arquivos PHP do plugin
find . -name "*.php" | xgettext \
    --files-from=- \
    --language=PHP \
    --keyword=__ \
    --keyword=__s \
    --keyword=_n:1,2 \
    --keyword=_x:2 \
    --keyword=_nx:2,3 \
    --add-comments=TRANS \
    --from-code=UTF-8 \
    --output=locales/myplugin.pot

# Atualizar um .po existente a partir do .pot atualizado
msgmerge --update locales/pt_BR.po locales/myplugin.pot
```

**Flags importantes do `xgettext`:**
- `--keyword=__` — captura `__('string', 'domain')`
- `--keyword=_n:1,2` — captura singular e plural de `_n()`
- `--keyword=_x:2` — captura a string (2º arg) de `_x()`
- `--add-comments=TRANS` — inclui comentários `//TRANS:` no `.pot`

---

## Override de traduções pelo administrador GLPI

Administradores podem sobrescrever traduções do plugin sem editar os arquivos do plugin. O GLPI verifica primeiro o diretório de override:

```
files/_locales/{pluginkey}/{ll_CC}.po
```

Exemplo: para sobrescrever strings PT-BR do plugin `myplugin`:
```
files/_locales/myplugin/pt_BR.po
```

> Isso é relevante para documentar no `README.md` do plugin — administradores que precisam customizar labels sem esperar uma nova versão podem usar esse mecanismo.

---

## Integração com Transifex (CI/CD oficial)

O projeto oficial `glpi-project/plugin-translation-workflows` fornece GitHub Actions prontos:

### Push do `.pot` para o Transifex (ao fazer push no `main`)

```yaml
# .github/workflows/push-locales.yml
name: "Update locales sources"
on:
  push:
    branches: ["main"]
jobs:
  push-sources-on-transifex:
    uses: "glpi-project/plugin-translation-workflows/.github/workflows/transifex-push-sources.yml@v1"
    secrets:
      transifex-token: "${{ secrets.TRANSIFEX_TOKEN }}"
```

### Pull das traduções do Transifex (cron diário + PR automático)

```yaml
# .github/workflows/sync-locales.yml
name: "Synchronize locales"
on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:
jobs:
  sync-with-transifex:
    uses: "glpi-project/plugin-translation-workflows/.github/workflows/transifex-sync.yml@v1"
    secrets:
      github-token: "${{ secrets.LOCALES_SYNC_TOKEN }}"
      transifex-token: "${{ secrets.TRANSIFEX_TOKEN }}"
```

O workflow de sync cria um PR automático com as traduções atualizadas e os `.mo` compilados.

---

## Checklist antes de entregar

- [ ] Toda string pública usa `__()`, `__s()`, `_n()`, `_x()` ou `_nx()` com o `pluginkey` como segundo argumento
- [ ] Nenhuma string está hardcoded em HTML, labels de abas, nomes de CronTask, descrições de direitos, mensagens de erro
- [ ] Strings com parâmetros usam `sprintf()` com placeholders numerados (`%1$s`, `%2$d`)
- [ ] Parâmetros de strings têm comentário `//TRANS:` explicando o tipo de cada placeholder
- [ ] O `.pot` está atualizado (rodou `xgettext`)
- [ ] Os arquivos `.mo` estão compilados e atualizados a partir dos `.po`
- [ ] A pasta `locales/` inclui pelo menos `en_GB.po` e `pt_BR.po` com `.mo` correspondentes
- [ ] Strings JS também usam os helpers `__()`, `_n()`, etc. com o domínio do plugin

---

## Antipadrões a rejeitar

```php
// ❌ Sem domínio — vai para o core do GLPI, não para o plugin
echo __('My label');

// ❌ Concatenação quebra a unidade de tradução
echo __('Found', 'myplugin') . ' ' . $count . ' items';

// ❌ String em variável — não extraída pelo xgettext
$msg = 'Save changes';
echo __($msg, 'myplugin');

// ❌ HTML hardcoded dentro de string traduzível
echo __('<strong>Warning:</strong> not found', 'myplugin');
// HTML deve ficar fora da string traduzível:
echo '<strong>' . __('Warning', 'myplugin') . ':</strong> ' . __('not found', 'myplugin');

// ❌ .mo ausente ou desatualizado — tradução não aparece mesmo com .po correto
```
