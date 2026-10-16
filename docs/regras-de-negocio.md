# API de análise de crédito — Regras de negócio

## Objetivo

Documentar os comportamentos esperados da API educacional
de análise de crédito em Python.

A API e suas regras são fictícias, sem vínculo com empresas
ou políticas reais de concessão de crédito.

## Endpoint de análise

```http
POST /analises-credito
Content-Type: application/json
```

O corpo da requisição deve ser um objeto JSON.

## Dados de entrada

| Campo | Tipo esperado | Obrigatório |
| --- | --- | --- |
| `idade` | Número inteiro | Sim |
| `rendaMensal` | Número monetário | Sim |
| `valorSolicitado` | Número monetário | Sim |

Exemplo:

```json
{
  "idade": 30,
  "rendaMensal": 3000.00,
  "valorSolicitado": 10000.00
}
```

## Validação dos dados

### Campos obrigatórios

Os três campos devem estar presentes e não podem ser nulos.

Dados ausentes ou nulos devem retornar HTTP 400.

### Idade

- Deve ser um número inteiro entre 0 e 120, inclusive.
- Textos e booleanos não são aceitos.
- Valores escritos com parte decimal, como `18.0`, não são aceitos
  pela implementação atual.

Uma idade válida para processamento não implica aprovação:
idades inferiores a 18 anos são reprovadas pela regra de negócio.

### Valores monetários

- Renda mensal e valor solicitado devem ser maiores que zero.
- Devem ser enviados como números JSON, sem aspas.
- Não são aceitos textos, booleanos, listas ou objetos.
- Devem respeitar o máximo de duas casas decimais.
- São representados internamente com `Decimal`.

Na implementação atual, a precisão considera o expoente do Decimal:
um valor como `3000.000` é rejeitado por conter três casas decimais,
mesmo que a terceira seja zero.

### Formato da requisição

- JSON malformado deve retornar HTTP 400.
- O corpo deve ser um objeto JSON; listas e valores isolados são rejeitados.
- Constantes como `NaN` e `Infinity` são rejeitadas como JSON inválido.
- Content-Type ausente ou diferente de `application/json`
  deve retornar HTTP 415.
- O tipo `application/json` pode incluir parâmetros,
  como `charset=UTF-8`.

Campos adicionais não utilizados pelas regras são ignorados
pela implementação atual.

## Critérios de aprovação

Uma solicitação será aprovada quando atender a todos os critérios:

1. Idade igual ou superior a 18 anos.
2. Renda mensal igual ou superior a R$ 2.000,00.
3. Valor solicitado menor ou igual a cinco vezes a renda mensal.

Exemplo:

- Idade: 30 anos.
- Renda mensal: R$ 3.000,00.
- Limite calculado: R$ 15.000,00.
- Valor solicitado: R$ 10.000,00.
- Resultado: APROVADO.

## Resultado da análise

Solicitações com dados válidos retornam HTTP 200,
mesmo quando reprovadas.

### Aprovação

```json
{
  "status": "APROVADO",
  "motivos": []
}
```

### Reprovação

Quando um ou mais critérios não forem atendidos:

```json
{
  "status": "REPROVADO",
  "motivos": [
    "Solicitante deve ter pelo menos 18 anos."
  ]
}
```

Todos os motivos aplicáveis devem ser retornados nesta ordem:

1. Idade inferior a 18 anos.
2. Renda inferior ao mínimo.
3. Valor solicitado superior ao limite.

### Mensagens de reprovação

| Critério não atendido | Mensagem |
| --- | --- |
| Idade mínima | Solicitante deve ter pelo menos 18 anos. |
| Renda mínima | Renda mensal inferior a R$ 2.000,00. |
| Limite solicitado | Valor solicitado superior a cinco vezes a renda mensal. |

## Dados inválidos e reprovação

| Situação | HTTP | Comportamento |
| --- | --- | --- |
| Idade 17, demais dados válidos | 200 | Análise REPROVADA |
| Idade -1 | 400 | Entrada rejeitada |
| Renda 1999.99, demais dados válidos | 200 | Análise REPROVADA |
| Renda zero | 400 | Entrada rejeitada |

A reprovação significa que a análise foi realizada,
mas os critérios de aprovação não foram atendidos.

Dados inválidos impedem a realização da análise.

## Disponibilidade

```http
GET /health
```

Resposta HTTP 200:

```json
{
  "status": "UP"
}
```

O endpoint verifica a disponibilidade da aplicação,
sem consultar dependências externas.

## Respostas HTTP

| Código | Comportamento esperado |
| --- | --- |
| 200 | Disponibilidade consultada ou análise realizada |
| 400 | Dados ou JSON inválidos |
| 404 | Endpoint inexistente |
| 405 | Método não permitido para a rota |
| 415 | Content-Type não aceito |

Em respostas HTTP 405, o cabeçalho `Allow` deve indicar
o método permitido.

## Cobertura automatizada atual

### Testes unitários — 25 casos

- 4 casos de aprovação, incluindo valores de fronteira.
- 3 casos de reprovação por um critério.
- 1 caso com todos os motivos de reprovação.
- 17 casos de entradas inválidas.

### Testes HTTP — 8 casos

- Consulta de disponibilidade.
- Aprovação.
- Reprovação por idade.
- Idade inválida.
- JSON malformado.
- Content-Type incorreto.
- Método não permitido.
- Endpoint inexistente.

A documentação descreve mais comportamentos do que os oito
cenários HTTP atualmente automatizados. Não representa
cobertura exaustiva da API.

## Limitações

- Sem autenticação.
- Sem banco de dados ou histórico das solicitações.
- Sem consulta a informações reais de clientes.
- Sem avaliação de risco real.
- Sem testes de carga nesta suíte.
- Sem garantia de cobertura total do código.
