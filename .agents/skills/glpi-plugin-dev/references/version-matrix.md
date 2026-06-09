# Matriz De Versão GLPI 10.x/11.x

## Regra Principal

Detectar `GLPI_VERSION` no core local e reportar arquivo/linha antes de escolher implementação. Se a versão não estiver clara, parar e pedir confirmação.

## GLPI 10.x

- Usar `front/*.php` para telas e endpoints web tradicionais.
- Usar `setup.php`, `hook.php`, classes em `src/`, hooks e APIs core disponíveis localmente.
- Não gerar controllers Symfony/routing como padrão.
- Usar `Glpi\Plugin\Hooks` somente se a constante/classe existir no core local; caso contrário, usar strings de hooks conforme docs/core da versão.
- Validar todo hook no core local, porque a documentação `master` pode ter recursos de GLPI 11.
- Usar branch/tag compatível do plugin `example`, como `origin/10.0/bugfixes` quando disponível. O branch 10 local declara `PLUGIN_EXAMPLE_MIN_GLPI = 10.0.0`, `PLUGIN_EXAMPLE_MAX_GLPI = 10.0.99` e PHP >= 7.4.
- Validar localização de assets no branch local: parte do example GLPI 10 usa assets na raiz, enquanto o branch principal GLPI 11 usa mais `public/`.

## GLPI 11.x

- Controllers, rotas e Twig podem ser considerados quando a documentação oficial e o core local confirmarem.
- Controllers em `src/Controller/` são descobertos automaticamente no GLPI 11; não registrar manualmente sem evidência local.
- Para GLPI < 11.0.7, rotas com métodos não-GET têm limitação documentada; incluir `GET` e checar método manualmente ou exigir GLPI >= 11.0.7.
- Ainda usar `front/*.php` quando o padrão local ou a simplicidade da tela justificar.
- Preferir constantes e namespaces modernos se existirem no core local.
- O branch principal do `pluginsGLPI/example` local declara GLPI 11 e PHP >= 8.2; pode orientar padrões modernos, mas ainda não deve ser copiado sem adaptação.

## Compatibilidade 10.x + 11.x

- Só prometer compatibilidade dupla quando o usuário pedir explicitamente.
- Implementar pelo menor denominador comum validado no core e nas docs.
- Evitar APIs exclusivas de 11.x quando o plugin precisa rodar em 10.x.
- Declarar requisitos em `plugin_version_{pluginkey}()` com faixa realista.
- Quando houver necessidade de branch por versão, manter a diferença pequena, explícita e documentada no código.
