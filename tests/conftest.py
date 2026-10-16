"""Configuração compartilhada dos testes HTTP da API."""

import socket
import threading
import time

import pytest
import requests
import uvicorn

from credito.credito_api import app


@pytest.fixture(scope="session", name="api_url")
def fixture_api_url():
    """Inicia a API local e encerra o servidor ao finalizar os testes."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conexao:
        conexao.bind(("127.0.0.1", 0))
        porta = conexao.getsockname()[1]
        endereco = f"http://127.0.0.1:{porta}"

        configuracao = uvicorn.Config(
            app,
            host="127.0.0.1",
            port=porta,
            log_level="warning",
            timeout_graceful_shutdown=3,
        )
        servidor = uvicorn.Server(configuracao)

        tarefa = threading.Thread(
            target=servidor.run,
            kwargs={"sockets": [conexao]},
            daemon=True,
        )

        tarefa.start()

        try:
            limite = time.monotonic() + 10

            with requests.Session() as cliente:
                cliente.trust_env = False

                while time.monotonic() < limite:
                    if not tarefa.is_alive():
                        pytest.fail("O servidor encerrou durante a inicialização.")

                    if servidor.started:
                        try:
                            resposta = cliente.get(
                                f"{endereco}/health",
                                timeout=0.5,
                            )
                            if resposta.status_code == 200:
                                break
                        except requests.exceptions.RequestException:
                            pass

                    time.sleep(0.05)
                else:
                    pytest.fail("A API não iniciou dentro de 10 segundos.")

            yield endereco

        finally:
            servidor.should_exit = True
            tarefa.join(timeout=5)

            if tarefa.is_alive():
                pytest.fail("O servidor não encerrou após os testes.")


@pytest.fixture(name="cliente_http")
def fixture_cliente_http():
    """Cria um cliente HTTP independente para cada teste."""
    with requests.Session() as cliente:
        cliente.trust_env = False
        yield cliente
