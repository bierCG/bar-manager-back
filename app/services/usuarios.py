from sqlalchemy.orm import Session

from app.schemas.schemas import UsuarioCreate
from app.exceptions.exceptions import RoleDesconhecida
from app.repositories.usuarios import UsuarioRepository

from app.security.password import hash_senha

class UsuarioService():
    def __init__(self, session: Session):
        self.session = session
        self.repo = UsuarioRepository(session)


    def listar_usuarios(self):
        return self.repo.get_all()


    def criar_usuario(self, dados_usuario: UsuarioCreate):
        if dados_usuario.role not in ["bartender", "cozinha", "pv"]:
            raise RoleDesconhecida

        dados = dados_usuario.model_dump()
        dados["senha"] = hash_senha(dados["senha"])

        return self.repo.create(dados)