import pytest
from sqlalchemy.exc import IntegrityError

from tests.conftest import session
from app.repositories.usuarios import UsuarioRepository

# ------------------------------------------------------------------------------------------
#
# ### OPERAÇÕES DE SUCESSO ###
#
# ------------------------------------------------------------------------------------------

def test_create_usuario(session):
    usuario = {
        "nome": "Fulano de Tal",
        "email": "fulano@email.com",
        "role": "bartender",
        "senha": "123456"
    }

    resultado = UsuarioRepository(session).create(usuario)

    assert resultado.id is not None
    assert resultado.nome == "Fulano de Tal"
    assert resultado.email == "fulano@email.com"
    assert resultado.role == "bartender"
    assert resultado.senha == "123456"


# ------------------------------------------------------------------------------------------
#
# ### INTEGRIDADE DE DADOS ###
#
# ------------------------------------------------------------------------------------------

def test_create_usuario_email_duplicado(session):
    usuario = {
        "nome": "Fulano de Tal",
        "email": "fulano@email.com",
        "role": "bartender",
        "senha": "123456"
    }

    UsuarioRepository(session).create(usuario)

    with pytest.raises(IntegrityError):
        UsuarioRepository(session).create(usuario)


def test_create_usuario_nome_nulo(session):
    usuario = {
        "nome": None,
        "email": "fulano@email.com",
        "role": "bartender",
        "senha": "123456"
    }

    with pytest.raises(IntegrityError):
        UsuarioRepository(session).create(usuario)


def test_create_usuario_email_nulo(session):
    usuario = {
        "nome": "Fulano de Tal",
        "email": None,
        "role": "bartender",
        "senha": "123456"
    }

    with pytest.raises(IntegrityError):
        UsuarioRepository(session).create(usuario)


def test_create_usuario_role_nulo(session):
    usuario = {
        "nome": "Fulano de Tal",
        "email": "fulano@email.com",
        "role": None,
        "senha": "123456"
    }

    with pytest.raises(IntegrityError):
        UsuarioRepository(session).create(usuario)


def test_create_usuario_senha_nula(session):
    usuario = {
        "nome": "Fulano de Tal",
        "email": "fulano@email.com",
        "role": "bartender",
        "senha": None
    }

    with pytest.raises(IntegrityError):
        UsuarioRepository(session).create(usuario)