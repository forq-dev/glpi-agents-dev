# [Nome da Integração] — Referência de Exemplo

> Este exemplo documenta um script/integração existente que será transformado em plugin GLPI.
> A IA deve ler este arquivo antes de ler o código em `src/`.

---

## O que este script faz

<!-- Descreva em 2–3 frases o que este script executa.
     Seja objetivo: qual sistema consulta, o que transforma, onde entrega. -->

---

## Problema que resolve

<!-- Qual processo manual, dor ou gap operacional este script elimina?
     Para quem é útil? Com que frequência é executado? -->

---

## Fluxo de execução

<!-- Descreva passo a passo o que o script faz, em ordem.
     Seja específico o suficiente para que a IA entenda a lógica sem precisar inferir.
     
     Exemplo:
     1. Autentica na API do Pandape com client_id e client_secret
     2. Busca todos os candidatos com status "aprovado" nas últimas 24h
     3. Para cada candidato, verifica se já existe como usuário no GLPI pela API REST
     4. Se não existe, cria o usuário com os campos mapeados (nome, email, telefone)
     5. Cria um Ticket de onboarding vinculado ao usuário criado
     6. Marca o candidato como "processado" no Pandape via PATCH -->

---

## APIs e sistemas envolvidos

| Sistema | Tipo | Autenticação | Endpoints usados |
|---------|------|-------------|-----------------|
| | | | |

---

## Formato dos dados

### Entrada (o que o script consome)

```json
// Exemplo de payload ou estrutura de dados que o script recebe/busca
{
}
```

### Saída (o que o script produz ou envia)

```json
// Exemplo de payload ou estrutura criada pelo script
{
}
```

---

## O que deve virar plugin GLPI

<!-- Quais partes deste script devem ser replicadas em PHP como plugin nativo?
     Quais partes não precisam (ex: autenticação simplificada que será substituída pela config do GLPI)? -->

| Funcionalidade do script | Deve virar plugin? | Observação |
|--------------------------|-------------------|------------|
| | Sim / Não / Parcialmente | |

---

## Mapeamento para conceitos GLPI

<!-- Como os dados e ações deste script se traduzem em objetos e ações nativas do GLPI? -->

| No script | No GLPI |
|-----------|---------|
| | |

---

## Limitações conhecidas do script atual

<!-- O que o script não trata? O que já quebrou? O que foi deixado para depois?
     Esta é a lista do que o plugin deve melhorar. -->

- 

---

## Variáveis de ambiente / configuração necessária

<!-- Quais credenciais, endpoints ou parâmetros o script precisa?
     No plugin, isso vai virar configuração no painel do GLPI — documente aqui para não perder. -->

| Variável | Descrição | Onde configurar no plugin |
|----------|-----------|--------------------------|
| | | |

---

## Notas adicionais para a IA

<!-- Qualquer contexto que não se encaixa nas seções acima mas é importante para o desenvolvimento.
     Regras de negócio implícitas, comportamentos esperados, casos de borda já conhecidos. -->
