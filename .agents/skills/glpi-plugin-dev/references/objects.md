# Objetos CommonDBTM, CRUD E Front-End

## Quando Usar

Use `CommonDBTM` quando o plugin precisa persistir e gerenciar um tipo de item próprio com CRUD, permissões, listagem, formulário, histórico, busca ou relações.

Antes de criar um objeto novo, verificar se já existe um tipo de item core, dropdown, relação ou classe GLPI que resolva o caso.

## Classe Do Objeto

Para GLPI 10.x/11.x com PSR-4, criar classes em `src/`, por exemplo:

```php
<?php

namespace GlpiPlugin\Myplugin;

use CommonDBTM;

class Equipment extends CommonDBTM
{
    public static $rightname = 'plugin_myplugin_equipment';

    public static function getTypeName($nb = 0): string
    {
        return _n('Equipment', 'Equipment', $nb, 'myplugin');
    }
}
```

Completar apenas o que a necessidade exigir:

- `$rightname` para permissões.
- `getTypeName()` para rótulo traduzível.
- Assinaturas herdadas do GLPI devem ser preservadas. Não remover defaults como `$nb = 0` ou `array $options = []` quando o core espera essa assinatura.
- `canCreate()`, `canDelete()`, `canPurge()` somente quando o padrão herdado não basta.
- `prepareInputForAdd()` e `prepareInputForUpdate()` para validação/normalização antes de persistir.
- `showForm()` quando a UI padrão precisa ser customizada.
- `rawSearchOptions()` ou método equivalente do GLPI local para listagem/pesquisa.

## CRUD

Preferir métodos herdados:

- `getFromDB()`
- `add()`
- `update()`
- `delete()`
- `check()`
- `redirectToList()`
- `showFormHeader()`
- `showFormButtons()`

Não criar um repositório, service ou wrapper CRUD se `CommonDBTM` já cobre o caso.

## Front Files

Para listagem:

- Criar `front/equipment.php`.
- Incluir `../../../inc/includes.php`.
- Verificar plugin instalado/ativo.
- Verificar permissões com métodos do item.
- Exibir `Html::displayNotFoundError()` ou `Html::displayRightError()` quando plugin/direito falhar, seguindo o padrão local.
- Usar `Html::header()`, `Search::show()` e `Html::footer()` quando for o padrão local.

Para formulário e ações:

- Criar `front/equipment.form.php`.
- Instanciar o objeto.
- Usar `check()` antes de `add`, `update`, `delete`, `purge` e `restore`.
- Redirecionar com helpers GLPI (`Html::redirect()`, `Html::back()`, `redirectToList()`).
- Usar `Toolbox::getItemTypeFormURL()` ou helpers equivalentes para URLs quando possível, evitando paths hardcoded.

## Validação De Entrada

- Validar em `prepareInputForAdd()` e `prepareInputForUpdate()` quando a regra pertence ao objeto.
- Lançar ou exibir erro de forma explícita usando mecanismos do GLPI local.
- Não mutar parâmetros de entrada; montar e retornar novo array quando possível.
- Não esconder falhas com catch genérico.

## Relações E Tabs

- Para relacionar item do plugin com item core, procurar padrões locais de relação em classes `Item_*`, tabs e `getTabNameForItem()`.
- Para dispositivos/itens relacionados, verificar se classes core como `CommonDevice`, `Item_Devices`, `CommonDropdown`, `Profile`, `NotificationTarget` ou relações `Item_*` resolvem antes de criar abstrações próprias.
- Preferir tabs e relações oficiais a alteração de formulário core.
- Para adicionar conteúdo em objetos core, usar hooks/tabs disponíveis; nunca editar `front/computer.form.php`, `src/Ticket.php` ou similares.
