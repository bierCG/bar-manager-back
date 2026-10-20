from sqlalchemy.orm import Session

from app.core.database.models import Usuario

class UsuarioRepository():
    def __init__(self, session: Session):
        self.session = session

    def get_by_username(self, username: str) -> Usuario | None:
        return self.session.query(Usuario).where(Usuario.usuario == username).first()

    def create(self, usuario: Usuario) -> Usuario:
        self.session.add(usuario)
        self.session.commit()
        self.session.refresh(usuario)
        return usuario