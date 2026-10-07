from sqlalchemy.orm import Session

from app.database.models import Usuario

class UsuarioRepository():
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.query(Usuario).all()

    def create(self, data: dict):
        usuario = Usuario(**data)
        
        self.session.add(usuario)
        self.session.commit()

        self.session.refresh(usuario)

        return usuario