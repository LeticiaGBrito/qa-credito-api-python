"""Testes HTTP da análise de crédito e da documentação da API."""

import pytest


# ========================================
# DISPONIBILIDADE E ANÁLISE DE CRÉDITO
# ========================================

def test_deve_consultar_disponibilidade(api_url, cliente_http):
    """Confirma disponibilidade, código HTTP e formato da resposta."""
    resposta = cliente_http.get(
        f"{api_url}/health",
        timeout=5,
    )

    assert resposta.status_code == 200
    assert resposta.headers["Content-Type"].startswith("application/json")
    assert resposta.json() == {"status": "UP"}


def test_deve_aprovar_solicitacao_via_api(api_url, cliente_http):
    """Aprova uma solicitação válida enviada por HTTP."""
    resposta = cliente_http.post(
        f"{api_url}/analises-credito",
        json={
            "idade": 30,
            "rendaMensal": 3000,
            "valorSolicitado": 10000,
        },
        timeout=5,
    )

    assert resposta.status_code == 200
    assert resposta.json() == {
        "status": "APROVADO",
        "motivos": [],
    }


def test_deve_reprovar_menor_de_idade_via_api(api_url, cliente_http):
    """Retorna HTTP 200 com reprovação por regra de negócio."""
    resposta = cliente_http.post(
        f"{api_url}/analises-credito",
        json={
            "idade": 17,
            "rendaMensal": 3000,
            "valorSolicitado": 10000,
        },
        timeout=5,
    )

    assert resposta.status_code == 200
    assert resposta.json() == {
        "status": "REPROVADO",
        "motivos": [
            "Solicitante deve ter pelo menos 18 anos.",
        ],
    }


def test_deve_rejeitar_idade_invalida_via_api(api_url, cliente_http):
    """Retorna HTTP 400 quando a idade está fora do intervalo."""
    resposta = cliente_http.post(
        f"{api_url}/analises-credito",
        json={
            "idade": -1,
            "rendaMensal": 3000,
            "valorSolicitado": 10000,
        },
        timeout=5,
    )

    assert resposta.status_code == 400
    assert resposta.json() == {
        "erro": "Idade deve ser um número inteiro entre 0 e 120.",
    }


def test_deve_rejeitar_json_malformado(api_url, cliente_http):
    """Rejeita um corpo JSON incompleto com HTTP 400."""
    resposta = cliente_http.post(
        f"{api_url}/analises-credito",
        data='{"idade": 30,',
        headers={"Content-Type": "application/json"},
        timeout=5,
    )

    assert resposta.status_code == 400
    assert resposta.json() == {"erro": "JSON inválido."}


def test_deve_rejeitar_content_type_incorreto(api_url, cliente_http):
    """Exige application/json para analisar uma solicitação."""
    resposta = cliente_http.post(
        f"{api_url}/analises-credito",
        data="conteudo de texto",
        headers={"Content-Type": "text/plain"},
        timeout=5,
    )

    assert resposta.status_code == 415
    assert resposta.json() == {
        "erro": "Utilize Content-Type application/json.",
    }


def test_deve_rejeitar_metodo_nao_permitido(api_url, cliente_http):
    """Rejeita GET no endpoint que aceita apenas POST."""
    resposta = cliente_http.get(
        f"{api_url}/analises-credito",
        timeout=5,
    )

    assert resposta.status_code == 405
    assert "POST" in resposta.headers.get("Allow", "")


def test_deve_retornar_404_para_rota_inexistente(api_url, cliente_http):
    """Retorna HTTP 404 quando o endpoint não existe."""
    resposta = cliente_http.get(
        f"{api_url}/rota-inexistente",
        timeout=5,
    )

    assert resposta.status_code == 404


# ========================================
# DOCUMENTAÇÃO SWAGGER
# ========================================

@pytest.mark.parametrize(
    "caminho",
    [
        pytest.param("/docs", id="sem-barra-final"),
        pytest.param("/docs/", id="com-barra-final"),
    ],
)
def test_deve_disponibilizar_swagger(
    api_url,
    cliente_http,
    caminho,
):
    """Disponibiliza HTML com aviso e configuração do Swagger."""
    resposta = cliente_http.get(
        f"{api_url}{caminho}",
        allow_redirects=False,
        timeout=5,
    )

    assert resposta.status_code == 200
    assert resposta.headers["Content-Type"].startswith("text/html")
    assert "QA Crédito API — Python" in resposta.text
    assert "Projeto educacional." in resposta.text
    assert 'id="swagger-ui"' in resposta.text
    assert 'url: "/openapi.json"' in resposta.text
    assert "SwaggerUIBundle" in resposta.text


def test_deve_documentar_endpoints_e_modelos(api_url, cliente_http):
    """Confere endpoints e referências aos modelos documentados."""
    resposta = cliente_http.get(
        f"{api_url}/openapi.json",
        timeout=5,
    )

    assert resposta.status_code == 200
    assert resposta.headers["Content-Type"].startswith("application/json")

    especificacao = resposta.json()

    assert especificacao["openapi"].startswith("3.1.")
    assert especificacao["info"]["title"] == "QA Crédito API — Python"
    assert any(
        servidor["url"] == "/"
        for servidor in especificacao["servers"]
    )

    caminhos = especificacao["paths"]

    assert "/health" in caminhos
    assert "/analises-credito" in caminhos
    assert "/docs" not in caminhos
    assert "/docs/" not in caminhos

    disponibilidade = caminhos["/health"]["get"]
    analise = caminhos["/analises-credito"]["post"]

    assert disponibilidade["responses"]["200"]["content"][
        "application/json"
    ]["schema"]["$ref"] == "#/components/schemas/Disponibilidade"

    assert analise["requestBody"]["content"][
        "application/json"
    ]["schema"]["$ref"] == "#/components/schemas/SolicitacaoCredito"

    assert analise["responses"]["200"]["content"][
        "application/json"
    ]["schema"]["$ref"] == "#/components/schemas/ResultadoAnalise"

    for codigo in ("400", "415"):
        assert analise["responses"][codigo]["content"][
            "application/json"
        ]["schema"]["$ref"] == "#/components/schemas/Erro"

    modelos = especificacao["components"]["schemas"]

    assert {
        "Disponibilidade",
        "SolicitacaoCredito",
        "ResultadoAnalise",
        "Erro",
    }.issubset(modelos)

    solicitacao = modelos["SolicitacaoCredito"]

    assert set(solicitacao["required"]) == {
        "idade",
        "rendaMensal",
        "valorSolicitado",
    }

    assert solicitacao["properties"]["idade"]["type"] == "integer"
    assert solicitacao["properties"]["idade"]["minimum"] == 0
    assert solicitacao["properties"]["idade"]["maximum"] == 120

    for campo in ("rendaMensal", "valorSolicitado"):
        propriedade = solicitacao["properties"][campo]

        assert propriedade["type"] == "number"
        assert propriedade["exclusiveMinimum"] == 0
        assert propriedade["multipleOf"] == 0.01

    assert set(
        modelos["ResultadoAnalise"]["properties"]["status"]["enum"]
    ) == {"APROVADO", "REPROVADO"}


@pytest.mark.parametrize(
    "caminho",
    [
        pytest.param("/docs", id="swagger"),
        pytest.param("/openapi.json", id="openapi"),
    ],
)
def test_deve_rejeitar_post_na_documentacao(
    api_url,
    cliente_http,
    caminho,
):
    """Rejeita POST nas rotas de documentação que aceitam GET."""
    resposta = cliente_http.post(
        f"{api_url}{caminho}",
        timeout=5,
    )

    assert resposta.status_code == 405
    assert "GET" in resposta.headers.get("Allow", "")


@pytest.mark.parametrize(
    "caminho",
    [
        pytest.param("/docs/inexistente", id="subcaminho-swagger"),
        pytest.param(
            "/openapi.json/inexistente",
            id="subcaminho-openapi",
        ),
    ],
)
def test_deve_rejeitar_subcaminhos_da_documentacao(
    api_url,
    cliente_http,
    caminho,
):
    """Retorna 404 para caminhos não definidos na documentação."""
    resposta = cliente_http.get(
        f"{api_url}{caminho}",
        timeout=5,
    )

    assert resposta.status_code == 404


# ========================================
# EXEMPLOS PUBLICADOS NO SWAGGER
# ========================================

@pytest.mark.parametrize(
    "nome_exemplo,status_esperado,motivos_esperados",
    [
        pytest.param(
            "aprovacao",
            "APROVADO",
            [],
            id="exemplo-aprovacao",
        ),
        pytest.param(
            "limitesExatos",
            "APROVADO",
            [],
            id="exemplo-limites-exatos",
        ),
        pytest.param(
            "reprovacaoPorIdade",
            "REPROVADO",
            [
                "Solicitante deve ter pelo menos 18 anos.",
            ],
            id="exemplo-reprovacao-por-idade",
        ),
        pytest.param(
            "multiplosMotivos",
            "REPROVADO",
            [
                "Solicitante deve ter pelo menos 18 anos.",
                "Renda mensal inferior a R$ 2.000,00.",
                (
                    "Valor solicitado superior a cinco vezes "
                    "a renda mensal."
                ),
            ],
            id="exemplo-multiplos-motivos",
        ),
    ],
)
def test_deve_processar_exemplo_publicado_no_swagger(
    api_url,
    cliente_http,
    nome_exemplo,
    status_esperado,
    motivos_esperados,
):
    """Envia o exemplo da documentação e confere o resultado real."""
    documentacao = cliente_http.get(
        f"{api_url}/openapi.json",
        timeout=5,
    )

    assert documentacao.status_code == 200

    especificacao = documentacao.json()

    exemplos = especificacao["paths"]["/analises-credito"]["post"][
        "requestBody"
    ]["content"]["application/json"]["examples"]

    assert nome_exemplo in exemplos

    dados = exemplos[nome_exemplo]["value"]

    resposta = cliente_http.post(
        f"{api_url}/analises-credito",
        json=dados,
        timeout=5,
    )

    assert resposta.status_code == 200
    assert resposta.headers["Content-Type"].startswith("application/json")
    assert resposta.json() == {
        "status": status_esperado,
        "motivos": motivos_esperados,
    }
