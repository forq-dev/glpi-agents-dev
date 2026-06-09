# Prontidão Corporativa

Use este checklist para plugins que serão usados em ambiente corporativo.

## Manutenção E Upgrade

- Declarar requisitos reais de GLPI, PHP, extensões e plugins dependentes em `plugin_version_{pluginkey}()`.
- Escrever install idempotente: a mesma função deve suportar instalação e upgrade.
- Versionar migrations de forma rastreável e validar upgrade a partir de uma instalação anterior.
- Preservar dados do usuário em upgrade; remover dados apenas em uninstall/clean quando esse for o comportamento esperado.
- Manter changelog e versionamento semântico quando o plugin será distribuído.

## Segurança E Auditoria

- Todos os fluxos de leitura/escrita devem validar sessão, perfil, entidade e direito.
- Respeitar entidades do GLPI quando o objeto ou relação for multi-entidade.
- Não expor configs sensíveis em API, tela, log ou debug.
- Declarar `secured_fields`/`secured_configs` quando usar criptografia do GLPI.
- Logs devem permitir rastrear falhas sem vazar segredo.
- Endpoints públicos exigem modelo de autenticação documentado.

## Operação

- CronTasks devem ser idempotentes, reexecutáveis e observáveis por logs/volume/status.
- Massive Actions devem reportar sucesso/falha por item e não parar lote inteiro sem necessidade.
- Notificações devem usar filas/templates/modos GLPI em vez de envio direto quando isso se encaixa no caso.
- Configurações devem ser editáveis pela UI do plugin quando administradores precisam operar sem deploy.

## Qualidade

- Rodar validações existentes: PHP lint, coding standard GLPI, análise estática, instalação, upgrade, uninstall e smoke test das telas.
- Usar CI oficial GLPI/plugin quando o repositório adotar esse padrão.
- Não adicionar dependência externa sem justificar por que o core GLPI ou PHP padrão não resolve.
- Evitar código didático em produção: exemplos devem ser adaptados, enxutos e validados.
