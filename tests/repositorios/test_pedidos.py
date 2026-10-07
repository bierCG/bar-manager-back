import pytest
from datetime import date, datetime, timedelta, time, timezone
from sqlalchemy.exc import IntegrityError

from app.repositories.pedidos import PedidoRepository
from tests.conftest import session

data = date.today()
intervalo =  {
        "inicio": datetime.combine(data, time(7), tzinfo=timezone.utc),
        "fim": datetime.combine(data + timedelta(days=1), time(6), tzinfo=timezone.utc)
    }

# ------------------------------------------------------------------------------------------
#
# ### OPERAÇÕES SUCESSO ###
#
# ------------------------------------------------------------------------------------------

def test_get_pedidos_filtra_por_data(session):
    resultado = PedidoRepository(session).get_ultimos_pedidos(
        intervalo["inicio"],
        intervalo["fim"]
    )

    assert all(
        intervalo["inicio"] <= pedido.criado_em <= intervalo["fim"]
        for pedido in resultado
    )

def test_get_pedidos_garcom(session):
    resultado = PedidoRepository(session).get_bartender_ultimos_pedidos(
        1,
        intervalo['inicio'],
        intervalo['fim']
    )

    assert all(pedido.vendedor_id == 1 for pedido in resultado)

def test_create_pedido(session):
    pedido = {
        "drink": "Cosmopolitan",
        "cliente_nome": "Any Randy"
    }

    resultado = PedidoRepository(session).create(pedido, 1, "ABERTO")

    assert resultado.vendedor_id == 1
    assert resultado.status == "ABERTO"
    assert resultado.drink == "Cosmopolitan"
    assert resultado.cliente_nome == "Any Randy"

def test_update_status(session):
    resultado = PedidoRepository(session).update_status_pedido(1, 'PRONTO')

    assert resultado.id == 1
    assert resultado.status == "PRONTO"

# ------------------------------------------------------------------------------------------
#
# ### CONSULTAS VAZIAS ###
#
# ------------------------------------------------------------------------------------------

def test_get_pedidos_vazio(session):
    resultado = PedidoRepository(session).get_ultimos_pedidos(
        datetime.now(),
        datetime.now()
    )

    assert resultado == []

def test_get_pedidos_garcom_vazio(session):
    resultado = PedidoRepository(session).get_bartender_ultimos_pedidos(
        99,
        datetime.now(),
        datetime.now()
    )

    assert resultado == []

# ------------------------------------------------------------------------------------------
#
# ### INTEGRIDADE DE DADOS ###
#
# ------------------------------------------------------------------------------------------

def test_create_pedido_foreign_key_violation(session):
    pedido = {
        "drink": "Cosmopolitan 4",
        "cliente_nome": "Any Randy 4"
    }

    with pytest.raises(IntegrityError):
        PedidoRepository(session).create(pedido, 99, "ABERTO")

def test_update_status_pedido_inexistente(session):
    assert PedidoRepository(session).update_status_pedido(99, "PRONTO") is None