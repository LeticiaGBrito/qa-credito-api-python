# QA Crédito API — Python

[![Testes Python](https://github.com/LeticiaGBrito/qa-credito-api-python/actions/workflows/testes.yml/badge.svg?branch=main)](https://github.com/LeticiaGBrito/qa-credito-api-python/actions/workflows/testes.yml)

Projeto educacional de automação de testes de uma API fictícia
de análise de crédito, desenvolvido com Python, FastAPI,
pytest e Requests.

A aplicação e suas regras não representam políticas reais
de concessão de crédito e não possuem vínculo com empresas.

## Objetivo

Demonstrar a transformação de requisitos em testes automatizados,
com validação de regras de negócio, valores de fronteira,
entradas inválidas e respostas HTTP.

O projeto separa as regras de crédito da camada HTTP, permitindo
testar o serviço isoladamente e também por requisições reais à API.

## Tecnologias e finalidade

| Tecnologia | Finalidade |
| --- | --- |
| Python | Implementação da aplicação e dos testes |
| FastAPI | Definição dos endpoints HTTP e documentação OpenAPI |
| Uvicorn | Execução do servidor da API |
| Decimal | Representação dos valores monetários sem conversão para float |
| pytest | Organização e execução dos testes |
| Requests | Envio de requisições HTTP nos testes automatizados |
| pytest-html | Geração do relatório HTML |
| JUnit XML | Formato de relatório para integração com ferramentas de CI |
| GitHub Actions | Execução automática dos testes e armazenamento dos relatórios |

As dependências diretas estão registradas em `requirements.txt`
e `requirements-dev.txt`.

## Funcionalidades

- Consulta de disponibilidade da API.
- Análise de crédito com critérios fictícios de idade,
  renda mensal e valor solicitado.
- Retorno dos motivos de reprovação.
- Validação de campos obrigatórios, tipos e valores permitidos.
- Rejeição de JSON malformado.
- Validação do Content-Type.
- Documentação interativa no Swagger UI.
- Execução automática dos testes com GitHub Actions.
- Geração de relatórios HTML e JUnit XML.

## Organização dos arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `credito/__init__.py` | Identifica o pacote Python da aplicação |
| `credito/analise_credito_service.py` | Implementa a validação dos dados, as regras de crédito e o resultado da análise |
| `credito/credito_api.py` | Recebe requisições HTTP, interpreta o JSON e chama o serviço |
| `tests/conftest.py` | Disponibiliza as fixtures do servidor local e do cliente HTTP |
| `tests/test_analise_credito_service.py` | Testa as regras de negócio diretamente, sem requisições HTTP |
| `tests/test_credito_api.py` | Testa os endpoints por requisições HTTP reais |
| `docs/regras-de-negocio.md` | Documenta os dados de entrada e os comportamentos esperados |
| `.github/workflows/testes.yml` | Configura a execução dos testes e o envio dos relatórios no GitHub Actions |
| `pytest.ini` | Configura a descoberta dos testes e a geração dos relatórios |
| `requirements.txt` | Registra as dependências diretas da aplicação |
| `requirements-dev.txt` | Inclui as dependências da aplicação e acrescenta as ferramentas de testes |
| `cspell.json` | Configura o corretor ortográfico do editor |
| `.gitignore` | Exclui do versionamento ambientes locais, caches e relatórios gerados |

### Classes principais

| Classe | Finalidade |
| --- | --- |
| `AnaliseCreditoService` | Valida os dados e aplica os critérios fictícios de aprovação |
| `ResultadoAnalise` | Representa o status e os motivos da análise em uma dataclass imutável |

## Estratégia de testes

A suíte atual possui **33 testes**:

| Camada | Quantidade |
| --- | ---: |
| Testes unitários das regras de negócio | 25 |
| Testes HTTP com Requests | 8 |
| **Total** | **33** |

### Testes unitários

Contemplam:

- Aprovação com dados válidos.
- Valores de fronteira dos critérios de aprovação.
- Reprovação por idade, renda ou valor solicitado.
- Retorno de múltiplos motivos de reprovação.
- Campos obrigatórios ausentes ou nulos.
- Idades inválidas, incluindo valores fracionários e booleanos.
- Valores monetários ausentes, iguais a zero, negativos
  ou com precisão inválida.
- Tipos incorretos e valores não finitos.

### Testes HTTP

Contemplam:

- Disponibilidade da API.
- Aprovação de solicitação válida.
- Reprovação por idade mínima.
- Rejeição de idade inválida.
- Rejeição de JSON malformado.
- Rejeição de Content-Type incorreto.
- Método HTTP não permitido.
- Endpoint inexistente.

A fixture inicia uma instância local da API em uma porta disponível
e solicita seu encerramento ao final da sessão de testes.

Não é necessário iniciar a aplicação manualmente para executar a suíte.
Os testes não dependem de uma API externa.

## Pré-requisitos

- Python 3.13 instalado.
- pip disponível.
- Acesso à internet para instalar as dependências.

O projeto foi executado localmente no Windows com Python 3.13.5
e no ambiente Linux do GitHub Actions com Python 3.13.

## Preparar o ambiente

Execute os comandos na raiz do projeto.

### Windows PowerShell

Crie o ambiente virtual:

```powershell
py -3.13 -m venv .venv
```

Instale as dependências da aplicação e dos testes:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Não é necessário ativar o ambiente virtual quando seu executável
é utilizado explicitamente nos comandos.

### Linux ou macOS

Com Python 3.13 disponível:

```bash
python3.13 -m venv .venv
./.venv/bin/python -m pip install -r requirements-dev.txt
```

## Executar os testes

### Windows PowerShell

```powershell
.\.venv\Scripts\python.exe -m pytest
```

### Linux ou macOS

```bash
./.venv/bin/python -m pytest
```

O pytest exibe o resultado de cada cenário e gera os relatórios
configurados no `pytest.ini`.

## Relatórios

| Arquivo | Finalidade |
| --- | --- |
| `reports/relatorio-testes.html` | Visualização dos resultados no navegador |
| `reports/resultados.xml` | Processamento dos resultados por ferramentas compatíveis com JUnit XML |

Para abrir o HTML no Windows PowerShell:

```powershell
Start-Process .\reports\relatorio-testes.html
```

O relatório HTML inclui resultados, duração dos testes e informações
do ambiente de execução.

A mensagem `No log output captured` indica que não houve saída
capturada para aquele teste; não significa falha.

Os corpos das requisições e respostas não são anexados
automaticamente ao relatório.

Os relatórios locais são sobrescritos a cada execução
e não são versionados no Git.

## Executar a API manualmente

### Windows PowerShell

```powershell
.\.venv\Scripts\python.exe -m uvicorn credito.credito_api:app --host 127.0.0.1 --port 8000
```

### Linux ou macOS

```bash
./.venv/bin/python -m uvicorn credito.credito_api:app --host 127.0.0.1 --port 8000
```

Endereço local:

```text
http://127.0.0.1:8000
```

Para encerrar, pressione `Ctrl + C` no terminal.

## Documentação interativa

Com o servidor em execução:

- [Swagger UI](http://127.0.0.1:8000/docs)
- [Especificação OpenAPI](http://127.0.0.1:8000/openapi.json)

Esses endereços são locais e dependem da aplicação em execução.

A raiz `/` não possui endpoint e retorna HTTP 404.

## Endpoints

### Consultar disponibilidade

```http
GET /health
```

Resposta HTTP 200:

```json
{
  "status": "UP"
}
```

Esse endpoint informa a disponibilidade da aplicação.
Não verifica banco de dados ou serviços externos.

### Analisar uma solicitação

```http
POST /analises-credito
Content-Type: application/json
```

Exemplo de entrada:

```json
{
  "idade": 30,
  "rendaMensal": 3000.00,
  "valorSolicitado": 10000.00
}
```

Resposta HTTP 200:

```json
{
  "status": "APROVADO",
  "motivos": []
}
```

Uma solicitação válida que não atende aos critérios também retorna
HTTP 200, com status `REPROVADO` e os respectivos motivos.

Exemplo de entrada para reprovação por idade:

```json
{
  "idade": 17,
  "rendaMensal": 3000.00,
  "valorSolicitado": 10000.00
}
```

Resposta HTTP 200:

```json
{
  "status": "REPROVADO",
  "motivos": [
    "Solicitante deve ter pelo menos 18 anos."
  ]
}
```

Exemplo de erro HTTP 400 para idade negativa:

```json
{
  "erro": "Idade deve ser um número inteiro entre 0 e 120."
}
```

## Respostas HTTP

| Código | Situação |
| --- | --- |
| 200 | Consulta de disponibilidade ou análise realizada |
| 400 | JSON ou dados de entrada inválidos |
| 404 | Endpoint não encontrado |
| 405 | Método HTTP não permitido |
| 415 | Content-Type não aceito |

Os erros tratados pela aplicação usam o campo `erro`.
As respostas padrão de roteamento do FastAPI, como 404 e 405,
utilizam o campo `detail`.

## Regras de negócio

Consulte [Regras de negócio](docs/regras-de-negocio.md).

## Integração contínua — GitHub Actions

O workflow [testes.yml](.github/workflows/testes.yml) executa
a suíte automaticamente:

- A cada push, em qualquer branch.
- Nos pull requests direcionados à branch `main`.
- Manualmente, pela opção `Run workflow` na aba Actions.

### Etapas da execução

1. Download do código do repositório.
2. Configuração do Python 3.13 em um ambiente Linux.
3. Restauração do cache do pip, quando disponível.
4. Instalação das dependências.
5. Verificação da compatibilidade das dependências com `pip check`.
6. Execução dos testes e geração dos relatórios.
7. Disponibilização dos relatórios como artefato para download.

Uma falha nos testes faz a execução da CI ser sinalizada como falha.

O passo de envio dos relatórios também é executado após falhas,
desde que o fluxo não tenha sido cancelado. Apenas os arquivos
efetivamente gerados podem ser enviados.

### Consultar as execuções

Acesse [GitHub Actions](https://github.com/LeticiaGBrito/qa-credito-api-python/actions).

Selecione uma execução para consultar as etapas e os logs.

### Baixar os relatórios

No resumo da execução:

1. Localize a seção `Artifacts`.
2. Baixe `relatorios-testes-python`.
3. Extraia o arquivo ZIP.
4. Abra `relatorio-testes.html` no navegador.

Os artefatos têm retenção configurada de 14 dias.

O arquivo `resultados.xml` também está incluído para uso
por ferramentas compatíveis com JUnit XML.

### Escopo da automação

Esta configuração implementa **integração contínua (CI)**:
o código enviado é verificado automaticamente pela suíte.

A publicação da API e o deploy automático ainda não estão
configurados nesta versão.

## Limites do projeto

- Aplicação educacional executada localmente e durante os testes da CI.
- Sem autenticação ou persistência em banco de dados.
- Não utiliza dados reais de clientes.
- Não possui integração com serviços financeiros externos.
- Não implementa uma política real de concessão de crédito.
- Testes aprovados não significam cobertura total do código.
- Os tempos dos testes não representam um teste de carga.
- Sem hospedagem pública da API ou deploy automático nesta versão.

## Autora

Letícia Gonçalves Garcia — QA Sênior

[Portfólio](https://leticiagbrito.github.io/)
