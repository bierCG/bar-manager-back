import pytest

from app.core.exceptions.exceptions import LoginInvalido
from app.services.login import LoginService
from tests.conftest import session


# ------------------------------------------------------------------------------------------
#
# ### LOGIN COM SUCESSO ###
#
# ------------------------------------------------------------------------------------------

def test_logar_sucesso(session):
    resultado = LoginService(session).logar(
        "user@email.com",
        "123456"
    )

    assert "token" in resultado
    assert resultado["token"]
    assert resultado["username"] == "Usuario 1"


# ------------------------------------------------------------------------------------------
#
# ### LOGIN INVÁLIDO ###
#
# ------------------------------------------------------------------------------------------

def test_logar_usuario_inexistente(session):
    with pytest.raises(LoginInvalido):
        LoginService(session).logar(
            "naoexiste@email.com",
            "123456"
        )


def test_logar_senha_invalida(session):
    with pytest.raises(LoginInvalido):
        LoginService(session).logar(
            "admin@email.com",
            "senha_errada"
        )