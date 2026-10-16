"""Testes unitários das regras fictícias de análise de crédito."""

from decimal import Decimal

import pytest

from credito.analise_credito_service import AnaliseCreditoService


@pytest.fixture(name="service")
def fixture_service():
    """Disponibiliza uma instância do serviço para cada teste."""
    return AnaliseCreditoService()


@pytest.mark.parametrize(
    "idade,renda,valor",
    [
        pytest.param(30, "3000.00", "10000.00", id="dados-validos"),
        pytest.param(18, "3000.00", "10000.00", id="idade-minima"),
        pytest.param(30, "2000.00", "5000.00", id="renda-minima"),
        pytest.param(30, "3000.00", "15000.00", id="limite-exato"),
    ],
)
def test_deve_aprovar_solicitacao(service, idade, renda, valor):
    """Aprova solicitações válidas, incluindo os limites de aprovação."""
    resultado = service.analisar(
        idade,
        Decimal(renda),
        Decimal(valor),
    )

    assert resultado.status == "APROVADO"
    assert resultado.motivos == ()


@pytest.mark.parametrize(
    "idade,renda,valor,motivo",
    [
        pytest.param(
            17,
            "3000.00",
            "10000.00",
            "Solicitante deve ter pelo menos 18 anos.",
            id="menor-de-idade",
        ),
        pytest.param(
            30,
            "1999.99",
            "5000.00",
            "Renda mensal inferior a R$ 2.000,00.",
            id="renda-abaixo-do-minimo",
        ),
        pytest.param(
            30,
            "3000.00",
            "15000.01",
            "Valor solicitado superior a cinco vezes a renda mensal.",
            id="valor-acima-do-limite",
        ),
    ],
)
def test_deve_reprovar_solicitacao(service, idade, renda, valor, motivo):
    """Reprova por um critério não atendido e informa o motivo exato."""
    resultado = service.analisar(
        idade,
        Decimal(renda),
        Decimal(valor),
    )

    assert resultado.status == "REPROVADO"
    assert resultado.motivos == (motivo,)


def test_deve_retornar_todos_os_motivos_de_reprovacao(service):
    """Retorna os três motivos quando nenhum critério é atendido."""
    resultado = service.analisar(
        17,
        Decimal("1000.00"),
        Decimal("6000.00"),
    )

    assert resultado.status == "REPROVADO"
    assert resultado.motivos == (
        "Solicitante deve ter pelo menos 18 anos.",
        "Renda mensal inferior a R$ 2.000,00.",
        "Valor solicitado superior a cinco vezes a renda mensal.",
    )


@pytest.mark.parametrize(
    "idade,renda,valor,mensagem",
    [
        pytest.param(
            None,
            Decimal("3000.00"),
            Decimal("10000.00"),
            "Idade, renda mensal e valor solicitado são obrigatórios.",
            id="idade-ausente",
        ),
        pytest.param(
            30,
            None,
            Decimal("10000.00"),
            "Idade, renda mensal e valor solicitado são obrigatórios.",
            id="renda-ausente",
        ),
        pytest.param(
            30,
            Decimal("3000.00"),
            None,
            "Idade, renda mensal e valor solicitado são obrigatórios.",
            id="valor-ausente",
        ),
        pytest.param(
            -1,
            Decimal("3000.00"),
            Decimal("10000.00"),
            "Idade deve ser um número inteiro entre 0 e 120.",
            id="idade-negativa",
        ),
        pytest.param(
            121,
            Decimal("3000.00"),
            Decimal("10000.00"),
            "Idade deve ser um número inteiro entre 0 e 120.",
            id="idade-acima-do-maximo",
        ),
        pytest.param(
            18.5,
            Decimal("3000.00"),
            Decimal("10000.00"),
            "Idade deve ser um número inteiro entre 0 e 120.",
            id="idade-fracionaria",
        ),
        pytest.param(
            True,
            Decimal("3000.00"),
            Decimal("10000.00"),
            "Idade deve ser um número inteiro entre 0 e 120.",
            id="idade-booleana",
        ),
        pytest.param(
            30,
            Decimal("0"),
            Decimal("10000.00"),
            "Renda mensal deve ser maior que zero.",
            id="renda-zero",
        ),
        pytest.param(
            30,
            Decimal("-1.00"),
            Decimal("10000.00"),
            "Renda mensal deve ser maior que zero.",
            id="renda-negativa",
        ),
        pytest.param(
            30,
            Decimal("3000.00"),
            Decimal("0"),
            "Valor solicitado deve ser maior que zero.",
            id="valor-zero",
        ),
        pytest.param(
            30,
            Decimal("3000.00"),
            Decimal("-1.00"),
            "Valor solicitado deve ser maior que zero.",
            id="valor-negativo",
        ),
        pytest.param(
            30,
            Decimal("3000.001"),
            Decimal("10000.00"),
            "Renda mensal deve ter no máximo duas casas decimais.",
            id="renda-com-tres-casas",
        ),
        pytest.param(
            30,
            Decimal("3000.00"),
            Decimal("10000.001"),
            "Valor solicitado deve ter no máximo duas casas decimais.",
            id="valor-com-tres-casas",
        ),
        pytest.param(
            30,
            "3000.00",
            Decimal("10000.00"),
            "Renda mensal deve ser informado como Decimal.",
            id="renda-com-tipo-incorreto",
        ),
        pytest.param(
            30,
            Decimal("3000.00"),
            "10000.00",
            "Valor solicitado deve ser informado como Decimal.",
            id="valor-com-tipo-incorreto",
        ),
        pytest.param(
            30,
            Decimal("NaN"),
            Decimal("10000.00"),
            "Renda mensal deve ser um número finito.",
            id="renda-nao-numerica",
        ),
        pytest.param(
            30,
            Decimal("3000.00"),
            Decimal("Infinity"),
            "Valor solicitado deve ser um número finito.",
            id="valor-infinito",
        ),
    ],
)
def test_deve_rejeitar_dados_invalidos(
    service, idade, renda, valor, mensagem
):
    """Rejeita entradas inválidas com ValueError e a mensagem esperada."""
    with pytest.raises(ValueError) as erro:
        service.analisar(idade, renda, valor)

    assert str(erro.value) == mensagem
