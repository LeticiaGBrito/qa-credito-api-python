"""API HTTP educacional para análise fictícia de crédito."""

import json
from decimal import Decimal

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from credito.analise_credito_service import AnaliseCreditoService


app = FastAPI(
    title="QA Crédito API",
    description=(
        "API educacional com regras fictícias de análise de crédito. "
        "Não representa políticas reais de concessão de crédito."
    ),
    version="1.0.0",
)

service = AnaliseCreditoService()


def rejeitar_constante_invalida(valor: str) -> None:
    """Rejeita NaN e Infinity, que não são números válidos em JSON."""
    raise ValueError(f"Constante JSON inválida: {valor}.")


def ler_valor_monetario(dados: dict, campo: str) -> Decimal | None:
    """Obtém um número monetário sem aceitar textos ou booleanos."""
    valor = dados.get(campo)

    if valor is None:
        return None

    if isinstance(valor, bool) or not isinstance(valor, (int, Decimal)):
        raise ValueError(f"O campo {campo} deve ser numérico.")

    return Decimal(valor)


@app.get("/health", tags=["Disponibilidade"])
def verificar_disponibilidade() -> dict[str, str]:
    """Informa que a aplicação está disponível."""
    return {"status": "UP"}


@app.post(
    "/analises-credito",
    tags=["Análise de crédito"],
    response_class=JSONResponse,
    responses={
        200: {"description": "Análise realizada: aprovada ou reprovada."},
        400: {"description": "JSON ou dados de entrada inválidos."},
        415: {"description": "Content-Type não aceito."},
    },
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "required": [
                            "idade",
                            "rendaMensal",
                            "valorSolicitado",
                        ],
                        "properties": {
                            "idade": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 120,
                            },
                            "rendaMensal": {
                                "type": "number",
                                "exclusiveMinimum": 0,
                                "multipleOf": 0.01,
                            },
                            "valorSolicitado": {
                                "type": "number",
                                "exclusiveMinimum": 0,
                                "multipleOf": 0.01,
                            },
                        },
                    },
                    "example": {
                        "idade": 30,
                        "rendaMensal": 3000.00,
                        "valorSolicitado": 10000.00,
                    },
                }
            },
        }
    },
)
async def analisar_credito(requisicao: Request) -> JSONResponse:
    """Valida a requisição e executa as regras de análise de crédito."""
    content_type = requisicao.headers.get("content-type", "")
    tipo_midia = content_type.split(";")[0].strip().lower()

    if tipo_midia != "application/json":
        return JSONResponse(
            status_code=415,
            content={"erro": "Utilize Content-Type application/json."},
        )

    corpo = await requisicao.body()

    try:
        dados = json.loads(
            corpo.decode("utf-8"),
            parse_float=Decimal,
            parse_constant=rejeitar_constante_invalida,
        )
    except (ValueError, UnicodeDecodeError):
        return JSONResponse(
            status_code=400,
            content={"erro": "JSON inválido."},
        )

    try:
        if not isinstance(dados, dict):
            raise ValueError(
                "O corpo da requisição deve ser um objeto JSON."
            )

        idade = dados.get("idade")
        renda = ler_valor_monetario(dados, "rendaMensal")
        valor = ler_valor_monetario(dados, "valorSolicitado")

        resultado = service.analisar(idade, renda, valor)

    except ValueError as erro:
        return JSONResponse(
            status_code=400,
            content={"erro": str(erro)},
        )

    return JSONResponse(
        status_code=200,
        content={
            "status": resultado.status,
            "motivos": list(resultado.motivos),
        },
    )
