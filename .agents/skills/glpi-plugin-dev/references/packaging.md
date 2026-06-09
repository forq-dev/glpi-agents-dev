# Empacotamento, Distribuição E Metadados

## Arquivos Esperados

Para plugin distribuível, validar a necessidade de:

- `README.md`
- `LICENSE`
- `CHANGELOG.md` quando o projeto já usa
- `composer.json`
- `example.xml` ou XML equivalente de marketplace
- `locale/` ou `locales/` com `.pot`, `.po`, `.mo`, conforme branch/tooling local
- `.tx/config` quando o projeto usa Transifex
- `misc/logo.png` e screenshots quando houver distribuição pública
- `tools/HEADER` se o projeto usa cabeçalho padronizado
- `.gitignore` excluindo `dist/`, `vendor/`, tokens e artefatos minificados gerados quando aplicável

## Metadata

- `plugin_version_{pluginkey}()` deve declarar nome, versão, autor, licença, homepage e requisitos GLPI.
- XML de marketplace deve declarar `name`, `key`, `state`, `logo`, descrições, homepage, downloads, issues, autores, versões, compatibilidade, idiomas, licença, tags e screenshots quando aplicável.
- A compatibilidade declarada deve bater com a versão local testada e com o código realmente gerado.

## Tradução

- Usar domínio de tradução do plugin, normalmente o `pluginkey`.
- Preferir `__s()`, `_n()` e helpers de tradução GLPI conforme o core local.
- Não hardcodar textos públicos se o plugin precisa ser traduzível.

## Release

- Não commitar nem taguear sem pedido explícito do usuário.
- Validar instalação, upgrade e uninstall antes de sugerir release.
- Se houver pacote zip, garantir que a raiz interna seja o diretório alfanumérico do plugin.
- Não incluir arquivos temporários, caches, `.git/`, `vendor/` desnecessário ou artefatos locais não intencionais.
- Se usar CI GLPI oficial, preferir `glpi-project/plugin-ci-workflows` e `glpi-project/plugin-translation-workflows` quando o repositório já segue esse padrão.
