# QA Crédito API — Python

[![Testes Python](https://github.com/LeticiaGBrito/qa-credito-api-python/actions/workflows/testes.yml/badge.svg?branch=main)](https://github.com/LeticiaGBrito/qa-credito-api-python/actions/workflows/testes.yml)

Projeto educacional de automação de testes de uma API fictícia
de análise de crédito, desenvolvido com Python, FastAPI,
pytest e Requests.

A aplicação e suas regras não representam políticas reais
de concessão de crédito e não possuem vínculo com empresas.

## Acesse a API

A aplicação está hospedada no Render:

- [Swagger UI — testar a API pelo navegador](https://qa-credito-api-python.onrender.com/docs)
- [Disponibilidade da aplicação](https://qa-credito-api-python.onrender.com/health)
- [Especificação OpenAPI](https://qa-credito-api-python.onrender.com/openapi.json)

No plano gratuito, o serviço pode ficar inativo quando não recebe
acessos. A primeira requisição após esse período pode demorar.

Utilize somente dados fictícios.

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
| Render | Hospedagem da API e configuração de deploy após os checks da CI |

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
- Acesso público à API hospedada no Render.

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
| `.python-version` | Define a linha Python 3.13 para a hospedagem |
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

Na CI, os testes HTTP utilizam uma instância criada no próprio runner.
Eles não executam requisições contra a API pública do Render.

## Pré-requisitos

Para executar localmente:

- Python 3.13 instalado.
- pip disponível.
- Acesso à internet para instalar as dependências.

O projeto foi executado localmente no Windows com Python 3.13.5
e no ambiente Linux do GitHub Actions com Python 3.13.

Para utilizar somente o Swagger público, não é necessário
instalar o projeto.

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

### Ambiente público

- [Swagger UI](https://qa-credito-api-python.onrender.com/docs)
- [Especificação OpenAPI](https://qa-credito-api-python.onrender.com/openapi.json)

### Ambiente local

Com o servidor em execução:

- [Swagger UI local](http://127.0.0.1:8000/docs)
- [Especificação OpenAPI local](http://127.0.0.1:8000/openapi.json)

A raiz `/` não possui endpoint e retorna HTTP 404.
Utilize `/health` para consultar a disponibilidade
ou `/docs` para acessar o Swagger.

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

Os critérios fictícios de aprovação são:

- Idade igual ou superior a 18 anos.
- Renda mensal igual ou superior a R$ 2.000,00.
- Valor solicitado menor ou igual a cinco vezes a renda mensal.

Todos os critérios devem ser atendidos para aprovação.

Consulte as validações e os comportamentos detalhados em
[Regras de negócio](docs/regras-de-negocio.md).

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

## Hospedagem e deploy — Render

A API utiliza o ambiente nativo Python do Render.

| Configuração | Valor |
| --- | --- |
| Repositório | `LeticiaGBrito/qa-credito-api-python` |
| Branch | `main` |
| Runtime | Python 3 |
| Versão do Python | Linha 3.13, definida em `.python-version` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python -m uvicorn credito.credito_api:app --host 0.0.0.0 --port $PORT` |
| Health Check Path | `/health` |
| Auto-Deploy | `After CI Checks Pass` |

O endereço `0.0.0.0` permite que a plataforma encaminhe
requisições à aplicação. A variável `PORT` fornece a porta
utilizada pelo serviço.

### Fluxo configurado de CI/CD

1. Uma alteração é enviada à branch `main`.
2. O GitHub Actions instala as dependências e executa os testes.
3. O Render aguarda os checks detectados para aquele commit.
4. Se os checks forem aprovados conforme os critérios da plataforma,
   o Render inicia o build e o deploy.
5. O Render verifica `/health` para avaliar a disponibilidade
   da nova instância.

Uma falha em um check detectado impede o deploy automático
daquele commit.

A primeira publicação do serviço é iniciada durante sua criação.
Ela não comprova, sozinha, o acionamento automático após a CI.

### Acompanhamento

- **GitHub Actions:** resultados dos testes, logs da CI e relatórios.
- **Render:** instalação, inicialização, health checks e status do deploy.

A conclusão da CI e a conclusão da publicação são acompanhadas
separadamente. O workflow atual não aguarda o término do deploy.

O selo no README representa o resultado do workflow de testes;
não representa a disponibilidade da API pública.

### Escopo das verificações

A suíte HTTP automatizada testa uma instância local no runner.
O health check do Render verifica o endpoint `/health`.

Ainda não há testes funcionais automatizados contra o endereço
público após a publicação.

## Limites do projeto

- Aplicação educacional com regras fictícias.
- Sem autenticação ou persistência em banco de dados.
- Não utiliza dados reais de clientes.
- Não possui integração com serviços financeiros externos.
- Não implementa uma política real de concessão de crédito.
- Testes aprovados não significam cobertura total do código.
- Os tempos dos testes não representam um teste de carga.
- Hospedagem gratuita sujeita a inatividade e demora no primeiro acesso.
- Sem testes funcionais automatizados contra o ambiente público após o deploy.
- O workflow de CI não acompanha a conclusão da publicação no Render.

## Autora

Letícia Gonçalves Garcia — QA Sênior

[Portfólio](https://leticiagbrito.github.io/)
