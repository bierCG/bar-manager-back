from sqlalchemy.orm import Session

from app.core.database.models import Usuario
from app.schemas.usuarios import CreateRequest
from app.core.exceptions.exceptions import RoleDesconhecida
from app.repositories.usuarios import UsuarioRepository

from app.core.security.password import hash_senha

class UsuarioService():
    def __init__(self, session: Session):
        self.repo = UsuarioRepository(session)

    def cadastrar_usuario(self, cadastro: CreateRequest) -> Usuario:
        if cadastro.role not in ["bartender", "cozinha", "expositor"]:
            raise RoleDesconhecida

        usuario = Usuario(
            **cadastro.model_dump(exclude={"senha"}),
            senha = hash_senha(cadastro.senha)
        )

        return self.repo.create(usuario)