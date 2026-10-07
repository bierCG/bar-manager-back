import pytest

from sqlalchemy.exc import IntegrityError

from app.schemas.schemas import UsuarioCreate
from app.exceptions.exceptions import RoleDesconhecida
from app.services.usuarios import UsuarioService
from tests.conftest import session

from app.security.password import validar_senha


# ------------------------------------------------------------------------------------------
#
# ### LISTAGEM ###
#
# ------------------------------------------------------------------------------------------

def test_listar_usuarios(session):
    resultado = UsuarioService(session).listar_usuarios()

    assert resultado
    assert all(usuario.id is not None for usuario in resultado)


# ------------------------------------------------------------------------------------------
#
# ### CRIAÇÃO ###
#
# ------------------------------------------------------------------------------------------

def test_criar_usuario(session):
    dados = UsuarioCreate(
        nome="Novo Usuario",
        email="novo@email.com",
        role="bartender",
        senha="123456"
    )

    resultado = UsuarioService(session).criar_usuario(dados)

    assert resultado.id is not None
    assert resultado.nome == "Novo Usuario"
    assert resultado.email == "novo@email.com"
    assert resultado.role == "bartender"

    assert resultado.senha != "123456"
    assert validar_senha("123456", resultado.senha)


# ------------------------------------------------------------------------------------------
#
# ### REGRAS DE NEGÓCIO ###
#
# ------------------------------------------------------------------------------------------

def test_criar_usuario_role_invalida(session):
    dados = UsuarioCreate(
        nome="Novo Usuario",
        email="novo@email.com",
        role="gerente",
        senha="123456"
    )

    with pytest.raises(RoleDesconhecida):
        UsuarioService(session).criar_usuario(dados)


# ------------------------------------------------------------------------------------------
#
# ### INTEGRIDADE DO BANCO ###
#
# ------------------------------------------------------------------------------------------

def test_criar_usuario_email_duplicado(session):
    dados = UsuarioCreate(
        nome="Usuario Duplicado",
        email="user@email.com",
        role="bartender",
        senha="123456"
    )

    with pytest.raises(IntegrityError):
        UsuarioService(session).criar_usuario(dados)