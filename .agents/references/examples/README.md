# examples/ — Referências de Integrações e Scripts Anteriores

Esta pasta contém exemplos de integrações e scripts existentes que servem como referência para o desenvolvimento de plugins GLPI.

---

## Para que serve

Quando você tem um script ou integração que já resolve um problema — mesmo que de forma manual, simplificada ou em outra linguagem — ele é a melhor documentação possível da lógica de negócio real.

A IA usa esses exemplos para:
- Entender **o processo** que deve ser transformado em plugin
- Identificar **quais dados** são consumidos e produzidos
- Mapear **fluxos de autenticação** com APIs externas
- Entender **edge cases** e tratamentos já testados na prática

---

## Como estruturar um exemplo

Cada integração ou script vive em sua própria subpasta com o seguinte padrão:

```
examples/
└── nome-da-integracao/
    ├── README.md          ← contexto obrigatório (leia abaixo)
    ├── src/               ← código-fonte original (Python, Shell, etc.)
    │   └── script.py
    └── docs/              ← documentação adicional (opcional)
        ├── api-reference.md
        └── flow.md
```

### O que o README.md de cada exemplo deve conter

1. **O que este script faz** — em 2–3 frases
2. **Problema que resolve** — qual processo manual ou dor ele elimina
3. **Como funciona** — fluxo passo a passo do que o código executa
4. **APIs e sistemas envolvidos** — quais endpoints, quais autenticações, quais formatos de dados
5. **O que deve virar plugin** — o que deste script deve ser replicado em PHP/GLPI e o que não precisa
6. **Limitações conhecidas** — o que o script não trata, o que quebra, o que foi deixado para depois
7. **Mapeamento para GLPI** — como os dados/ações deste script se traduzem em conceitos GLPI (Tickets, Users, Assets, etc.)

---

## Exemplos disponíveis

| Pasta | Integração | Linguagem original | Status |
|-------|-----------|-------------------|--------|
| — | — | — | — |

<!-- Adicione uma linha aqui quando incluir um novo exemplo -->

---

## Regra para a IA

> Ao analisar um exemplo, a IA deve tratar o código como **fonte de verdade da lógica de negócio**, não como código a ser copiado.
> O objetivo é entender **o que o processo faz**, não reusar a implementação.
> A implementação final deve seguir os padrões GLPI nativos definidos em `.agents/`.
