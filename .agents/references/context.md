# context.md — Identidade do Projeto

> Este arquivo define o objetivo, escopo, metas e contexto do projeto sendo desenvolvido neste clone.
> Deve ser preenchido antes de qualquer sessão de desenvolvimento.
> O Maintainer deve ler este arquivo **antes** de qualquer arquivo em `.agents/references/`.

---

## O que é este projeto

<!-- Descreva em 2–3 frases o que este projeto constrói.
     Exemplo: "Plugin GLPI que integra o GLPI com a plataforma Pandape, sincronizando candidatos e processos seletivos como Tickets." -->

---

## Objetivo principal

<!-- O que este plugin resolve? Qual dor elimina ou qual processo automatiza?
     Seja específico: para quem é útil, em que contexto, qual o ganho concreto. -->

---

## Metas do projeto

<!-- Lista de metas mensuráveis. Exemplos:
     - Sincronizar candidatos do Pandape como usuários no GLPI automaticamente
     - Criar Tickets de onboarding vinculados ao processo seletivo
     - Eliminar o script Python manual de importação -->

---

## Público-alvo

<!-- Quem vai usar este plugin?
     Exemplos: equipe de RH, técnicos de TI, gestores de chamados, usuários finais -->

---

## Escopo — o que está dentro

<!-- O que este projeto vai fazer. Seja explícito para nortear o desenvolvimento. -->

---

## Escopo — o que está fora (non-goals)

<!-- O que este projeto NÃO vai fazer. Evita scope creep e mantém o foco.
     Exemplos: não vai substituir o sistema de RH, não vai criar portal externo para candidatos -->

---

## Tecnologias envolvidas

| Camada | Tecnologia |
|--------|-----------|
| Plugin GLPI | PHP 8.x, Tabler CSS (GLPI 11.x) |
| Integração externa | — |
| Testes | — |
| Ambiente local | GLPI 11.x, Apache/Nginx, MySQL/MariaDB |

---

## Origem da lógica de negócio

<!-- De onde vem a lógica que o plugin vai implementar?
     Se existe um script anterior (Python, Shell, etc.), descreva aqui e aponte para examples/.
     
     Exemplo:
     - Script Python de integração Pandape → GLPI (ver examples/pandape-glpi-sync/)
     - Processo manual documentado em Notion
     - API externa documentada em examples/ -->

---

## Restrições e decisões iniciais

<!-- Qualquer restrição técnica, de produto ou de processo já conhecida antes de começar.
     Exemplos:
     - Deve funcionar sem modificar o GLPI core
     - Deve suportar multi-entidade
     - Credenciais da API externa via configuração no painel do GLPI (não hardcoded) -->

---

## Links e referências externas

<!-- APIs, documentações, portais de parceiros, dashboards ou qualquer recurso externo relevante. -->

| Recurso | URL |
|---------|-----|
| Documentação GLPI Developer | https://glpi-developer-documentation.readthedocs.io/en/master/ |
| | |

---

## Status do projeto

<!-- Em qual fase está este projeto?
     Exemplos: discovery, prototipagem, desenvolvimento ativo, manutenção -->

- Fase atual: —
- Iniciado em: —
- Última atualização deste arquivo: —
