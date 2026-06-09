# Controllers, Rotas E Twig

## Regra De Versão

A documentação oficial master validada por `curl` informa que controllers de plugin exigem GLPI >= 11.0.

Para tarefas cujo alvo é GLPI 10.x:

- Não gerar controllers Symfony como solução padrão.
- Usar `front/*.php`, hooks, classes em `src/`, templates/padrões locais disponíveis e APIs GLPI 10.x.
- Explicar ao usuário quando a solução pedida depende de controllers GLPI 11+.

Para tarefas cujo alvo é GLPI 11+:

- Revalidar a página oficial de controllers com `curl`.
- Inspecionar controllers no core local.
- Confirmar `GLPI_VERSION` local e mostrar a evidência de arquivo/linha ao usuário.
- Criar controller em `src/Controller/`.
- Usar namespace `GlpiPlugin\Pluginkey\Controller`.
- Estender `Glpi\Controller\AbstractController` ou implementar `Glpi\DependencyInjection\PublicService`.
- Declarar rota com atributo `Route`; não incluir o prefixo `/plugins/{pluginkey}` no atributo.
- Retornar `Symfony\Component\HttpFoundation\Response`.
- Usar Twig com prefixo `@pluginkey` quando aplicável.
- Saber que controllers em `src/Controller/` são descobertos automaticamente.
- Para GLPI < 11.0.7, evitar rota apenas `POST`/`PUT`/`DELETE`/`PATCH`; a documentação indica workaround com `GET` + checagem manual do método.

## Acesso Não Autenticado

Se o usuário pedir endpoint público ou API:

- Validar no core local os mecanismos de sessão/firewall.
- Para stateless, registrar caminho com `SessionManager::registerPluginStatelessPath()` quando a versão local suportar.
- Para página pública com sessão, validar `Glpi\Security\Attribute\SecurityStrategy` e `Glpi\Http\Firewall::STRATEGY_NO_CHECK` no core local.
- Não desativar autenticação global do GLPI.
- Não criar rota pública sem explicar o modelo de autenticação.

## Compatibilidade

- Nunca copiar exemplo de controllers GLPI 11 para GLPI 10.x sem prova no core local.
- Se a documentação master divergir da versão local, priorizar a versão instalada para implementação e explicar a diferença.
