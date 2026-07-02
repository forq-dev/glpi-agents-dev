# AGENTS.md — Regras de Orquestração Mandatórias

Este arquivo define as regras obrigatórias de comportamento e fluxo de trabalho para qualquer agente de IA que atuar neste repositório.

## 🚨 PONTO DE ENTRADA OBRIGATÓRIO

- **Antes de planejar, codificar ou editar qualquer arquivo**, você deve ler e carregar o arquivo de orquestração principal: [MAINTAINER.md](file:///.agents/MAINTAINER.md) utilizando as skills de `brainstorming` e `grill-me` para um melhor entendimento do contexto e das tarefas.
- Não trate o diretório `.agents/` como documentação passiva. Ele é uma instrução operacional mandatória. Em caso de conflito entre a conveniência de implementação direta e o fluxo do Maintainer, **o fluxo do Maintainer sempre vence**.

## 🔄 Orquestração Obrigatória

- O agente principal **não deve implementar código diretamente** para tarefas não triviais. Ele deve atuar como coordenador, integrador e revisor.
- Toda tarefa estrutural ou de implementação complexa deve ser delegada obrigatoriamente a subagents especializados:
  - 1 subagent para backend/frontend/banco (ex: `glpi-plugin-backend.md`, `glpi-plugin-frontend.md`)
  - 1 subagent para testes e validação (`glpi-plugin-qa.md`)
  - 1 subagent para auditoria de segurança (`glpi-plugin-security.md`)
- Toda nova feature, alteração de endpoints, controllers, uploads ou mutações de banco de dados **deve obrigatoriamente** passar por uma auditoria do subagent de segurança antes de ser integrada e considerada concluída.
- A implementação direta pelo agente principal sem o uso de subagents só é permitida em mudanças muito pequenas, pontuais (1 único arquivo) e de baixíssimo risco.

## 🎯 Gatilhos para Acionamento de Subagents

Você deve obrigatoriamente inicializar o fluxo do Maintainer e spawnar subagents quando a tarefa envolver:
1. Alteração em **mais de 1 arquivo**.
2. Refatoração estrutural ou lógica de negócio complexa.
3. Criação ou modificação de testes automatizados.
4. Alterações em áreas críticas de segurança, controllers, fluxos de convidados (guest flow), uploads, autenticação ou checagem de permissões/direitos.

## 🛠️ Fluxo de Trabalho Esperado

1. **Carregar o Maintainer**: Ler `.agents/MAINTAINER.md`.
2. **Revisar o Contexto**: Ler os arquivos em `.agents/references/*` (decisões anteriores, tasks atuais, backlog, contexto do plugin, etc.).
3. **Gerar Briefings**: Gerar briefings detalhados usando o template formal contido no Maintainer.
4. **Delegar Código**: Disparar o subagent adequado para propor a lógica.
5. **Delegar Testes**: Disparar o subagent de QA para propor a cobertura de testes automatizados (em PHP ou Python sob o diretório `tests/`).
6. **Auditar Segurança**: Disparar o subagent de segurança (`glpi-plugin-security.md`) para auditar o código proposto pelo backend/frontend, validando contra falhas (CSRF, XSS, SQLi, direitos de acesso) e registrando o resultado/conformidade em [references/security-audits.md](file:///.agents/references/security-audits.md).
7. **Integrar e Validar**: O agente principal aplica as propostas aprovadas e valida o resultado contra o GLPI local.
8. **Atualizar Contexto**: Atualizar `tasks.md`, `plugin-context.md`, `decisions.md` ou `inspection-notes.md` conforme as mudanças realizadas.

## 🔒 Travas de Modificação
- **Skills**: É expressamente proibido criar, modificar ou excluir qualquer arquivo dentro da pasta `.agents/skills/`. A leitura de skills é estritamente read-only.
