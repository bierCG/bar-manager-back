from sqlalchemy.orm import Session

from app.schemas.usuarios import CadastroUsuarioRequest
# from app.core.exceptions.exceptions import RoleDesconhecida --- Descontinuar Classe
from app.core.exceptions.exceptions import UsuarioDuplicado
from app.repositories.usuarios import UsuarioRepository
from app.core.database.models import Usuario

from app.core.security.password import hash_senha

class UsuarioService():
    def __init__(self, session: Session):
        self.repo = UsuarioRepository(session)

    def cadastrar_usuario(self, cadastro: CadastroUsuarioRequest) -> Usuario:
        if self.repo.get_by_username(cadastro.usuario):
            raise UsuarioDuplicado()

        usuario = Usuario(
            **cadastro.model_dump(exclude={"senha"}),
            senha = hash_senha(cadastro.senha)
        )
        
        return self.repo.create(usuario)