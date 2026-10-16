"""Testes HTTP da API fictícia de análise de crédito."""


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
