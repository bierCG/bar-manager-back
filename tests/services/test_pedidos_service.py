import pytest

from app.exceptions.exceptions import (
    PedidoNaoEncontrado,
    CancelamentoInvalido,
    PedidoNaoPodeSerFinalizado
)

from app.schemas.schemas import PedidoCreate
from app.services.pedidos import PedidosService
from tests.conftest import session


# ------------------------------------------------------------------------------------------
#
# ### LISTAGEM ###
#
# ------------------------------------------------------------------------------------------

def test_listar_ultimos_pedidos(session):
    resultado = PedidosService(session).listar_ultimos_pedidos()

    assert resultado
    assert all(pedido.id is not None for pedido in resultado)


def test_listar_pedidos_bartender(session):
    resultado = PedidosService(session).listar_pedidos_bartender(1)

    assert all(pedido.vendedor_id == 1 for pedido in resultado)


# ------------------------------------------------------------------------------------------
#
# ### CRIAÇÃO ###
#
# ------------------------------------------------------------------------------------------

def test_criar_pedido(session):
    pedido = PedidoCreate(
        drink="Caipirinha",
        cliente_nome="Fulano"
    )

    resultado = PedidosService(session).criar_pedido(
        pedido,
        1
    )

    assert resultado.id is not None
    assert resultado.drink == "Caipirinha"
    assert resultado.cliente_nome == "Fulano"
    assert resultado.vendedor_id == 1
    assert resultado.status == "ABERTO"


# ------------------------------------------------------------------------------------------
#
# ### FINALIZAÇÃO ###
#
# ------------------------------------------------------------------------------------------

def test_finalizar_pedido_aberto(session):
    resultado = PedidosService(session).finalizar_pedido(1)

    assert resultado.id == 1
    assert resultado.status == "PRONTO"


def test_finalizar_pedido_inexistente(session):
    with pytest.raises(PedidoNaoEncontrado):
        PedidosService(session).finalizar_pedido(999)


def test_finalizar_pedido_ja_pronto(session):
    with pytest.raises(PedidoNaoPodeSerFinalizado):
        PedidosService(session).finalizar_pedido(2)


def test_finalizar_pedido_cancelado(session):
    with pytest.raises(PedidoNaoPodeSerFinalizado):
        PedidosService(session).finalizar_pedido(3)


# ------------------------------------------------------------------------------------------
#
# ### CANCELAMENTO ###
#
# ------------------------------------------------------------------------------------------

def test_cancelar_pedido_aberto(session):
    resultado = PedidosService(session).cancelar_pedido(1)

    assert resultado.id == 1
    assert resultado.status == "CANCELADO"


def test_cancelar_pedido_pronto(session):
    resultado = PedidosService(session).cancelar_pedido(2)

    assert resultado.id == 2
    assert resultado.status == "CANCELADO"


def test_cancelar_pedido_inexistente(session):
    with pytest.raises(PedidoNaoEncontrado):
        PedidosService(session).cancelar_pedido(999)


def test_cancelar_pedido_cancelado(session):
    with pytest.raises(CancelamentoInvalido):
        PedidosService(session).cancelar_pedido(3)