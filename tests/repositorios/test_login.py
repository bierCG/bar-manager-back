import pytest

from app.repositories.login import LoginRepository


# ------------------------------------------------------------------------------------------
#
# ### CONSULTAS COM RESULTADO ###
#
# ------------------------------------------------------------------------------------------

def test_get_user(session):
    resultado = LoginRepository(session).get_user("user@email.com")

    assert resultado is not None
    assert resultado.email == "user@email.com"


# ------------------------------------------------------------------------------------------
#
# ### CONSULTAS VAZIAS ###
#
# ------------------------------------------------------------------------------------------

def test_get_user_inexistente(session):
    resultado = LoginRepository(session).get_user("naoexiste@email.com")

    assert resultado is None